from flask import Flask, request, jsonify
from flask_cors import CORS
from pathlib import Path
import sqlite3
import re
from datetime import datetime

# =====================================================
# VORTIQ CONFIGURATION
# =====================================================

app = Flask(__name__)
CORS(app)

# Direct CNC connection state. Alarm snapshots are supplied by cnc_monitor.py using
# FANUC FOCAS read-only functions; no Arduino data or synthetic alarm rules are used.
CNC_STATE = {
    "connected": False, "last_seen": None, "alarms": [], "source": "FANUC_FOCAS_READ_ONLY",
    "controller_model": "Unknown", "machine_id": "CNC-FOCAS-01", "connection_error": "Monitor has not connected yet."
}
# Retain legacy state only for backward compatibility with unrelated endpoints. It is not used by the CNC dashboard.
HARDWARE_STATE = {"connected": False, "last_seen": None, "telemetry": None, "active_alarm": None, "diagnosis": None, "source": "DISABLED_NOT_CNC"}

BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "vortiq.db"
RAG_DOCUMENT = BASE_DIR / "rag_documents" / "Vortiq_RAG_Knowledge_Base.md"


# =====================================================
# DATABASE HELPERS
# =====================================================

def get_db():
    conn = sqlite3.connect(str(DB_FILE))
    conn.row_factory = sqlite3.Row
    return conn


def normalize_code(value):
    return re.sub(r"\s+", "", str(value or "")).upper()


def find_alarm(controller, alarm_code):
    """Find an exact alarm-code record, matching controller when ambiguous."""
    if not alarm_code:
        return None

    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute('PRAGMA table_info("alarm_knowledge")')
        columns = {row["name"] for row in cursor.fetchall()}
        if "alarm_code" not in columns:
            raise RuntimeError("alarm_knowledge table has no alarm_code column")

        controller_columns = [
            name for name in ("controller_model", "controller_scope")
            if name in columns
        ]
        cursor.execute(
            'SELECT * FROM "alarm_knowledge" '
            'WHERE UPPER(TRIM(alarm_code)) = ?',
            (normalize_code(alarm_code),),
        )
        rows = [dict(row) for row in cursor.fetchall()]
        if not rows:
            return None
        if len(rows) == 1:
            return rows[0]

        requested = str(controller or "").strip().upper()
        if not requested:
            return None

        matches = []
        for row in rows:
            values = [str(row.get(col) or "").strip().upper() for col in controller_columns]
            if any(value and (requested == value or requested in value or value in requested)
                   for value in values):
                matches.append(row)

        # Deduplicate a row that matched more than one controller column.
        unique = {row["id"]: row for row in matches} if all("id" in r for r in matches) else {}
        if unique:
            matches = list(unique.values())
        return matches[0] if len(matches) == 1 else None
    finally:
        conn.close()


# =====================================================
# LOCAL RAG INITIALIZATION — NO EMBEDDING MODEL REQUIRED
# =====================================================

rag_init_error = None
rag_documents = []

def load_rag_documents():
    """Load the existing Markdown RAG source without changing its format."""
    global rag_documents, rag_init_error
    try:
        if not RAG_DOCUMENT.exists():
            raise FileNotFoundError(f"RAG source not found: {RAG_DOCUMENT}")
        text = RAG_DOCUMENT.read_text(encoding="utf-8")
        # Preserve existing Markdown format; split only at record headings.
        sections = re.split(r"(?=^### Record \d+:)", text, flags=re.MULTILINE)
        rag_documents = [section.strip() for section in sections if section.strip()]
        if not rag_documents:
            # Keep the whole document searchable if it does not use record headings.
            rag_documents = [text.strip()] if text.strip() else []
        print(f"RAG source loaded: {len(rag_documents)} sections")
    except Exception as exc:
        rag_init_error = str(exc)
        rag_documents = []
        print("RAG initialization warning:", rag_init_error)

load_rag_documents()


def retrieve_alarm_document(alarm_code):
    """Return only RAG sections with an explicit exact Alarm code field."""
    expected_code = normalize_code(alarm_code)
    if not expected_code:
        return None
    matches = []
    for document in rag_documents:
        match = re.search(
            r"(?im)^\s*(?:[-*]\s*)?(?:\*\*)?Alarm code:(?:\*\*)?\s*([^\s`*]+)",
            document or "",
        )
        if not match:
            continue
        found_code = normalize_code(match.group(1).strip("*` "))
        if found_code == expected_code:
            heading = next((line.strip("# ").strip() for line in document.splitlines()
                            if line.strip().startswith("#")), "")
            matches.append({
                "document": document,
                "source": RAG_DOCUMENT.name,
                "section": heading,
            })
    if not matches:
        return None
    return {
        "document": "\n\n".join(item["document"] for item in matches),
        "source": matches[0]["source"],
        "section": matches[0]["section"],
    }


# =====================================================
# CONTROLLER-INDEPENDENT EXACT ALARM SEARCH
# =====================================================

@app.route("/api/search-alarm", methods=["POST"])
def search_alarm():
    """
    Search by exact alarm code without requiring a machine model.
    If multiple controller records use the code, return all matches so
    the operator can choose the correct controller family.
    """
    data = request.get_json(silent=True) or {}
    alarm_code = str(data.get("alarm_code", "")).strip()
    if not alarm_code:
        return jsonify({"success": False, "message": "Alarm code is required."}), 400

    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute('PRAGMA table_info("alarm_knowledge")')
        columns = {row["name"] for row in cursor.fetchall()}
        if "alarm_code" not in columns:
            return jsonify({"success": False, "message": "Alarm knowledge table has no alarm_code column."}), 500

        cursor.execute(
            'SELECT * FROM alarm_knowledge WHERE UPPER(TRIM(alarm_code)) = ? ORDER BY brand, controller_model',
            (normalize_code(alarm_code),)
        )
        matches = [dict(row) for row in cursor.fetchall()]

        if not matches:
            return jsonify({
                "success": True,
                "found": False,
                "count": 0,
                "matches": [],
                "message": "No exact local database match. A semantic search may help locate related documentation, but it cannot confirm the alarm identity."
            })

        # Add a stable display label without changing the stored records.
        for item in matches:
            item["match_label"] = " — ".join(
                str(item.get(key, "")).strip()
                for key in ("brand", "controller_model", "machine_type")
                if item.get(key)
            ) or "Controller scope not recorded"

        return jsonify({
            "success": True,
            "found": True,
            "count": len(matches),
            "matches": matches,
            "message": "One exact record found." if len(matches) == 1 else "Multiple exact-code records found. Select the controller family that matches your machine."
        })
    except sqlite3.Error:
        app.logger.exception("Controller-independent alarm search failed")
        return jsonify({"success": False, "message": "Database search failed."}), 500
    finally:
        conn.close()


# =====================================================
# CHECK ALARM API
# =====================================================

@app.route("/api/check-alarm", methods=["POST"])
def check_alarm():
    data = request.get_json(silent=True) or {}
    controller = str(data.get("controller", "")).strip()
    alarm_code = str(data.get("alarm_code", "")).strip()

    if not alarm_code:
        return jsonify({"success": False, "message": "Alarm code is required."}), 400

    try:
        alarm = find_alarm(controller, alarm_code)
    except Exception:
        app.logger.exception("Database alarm lookup failed")
        return jsonify({"success": False, "message": "Database lookup failed. Check the backend terminal."}), 500

    if not alarm:
        return jsonify({
            "success": False,
            "message": "No unambiguous matching alarm was found. Check the controller model and alarm code.",
        }), 404

    return jsonify({"success": True, "alarm": alarm})


# =====================================================
# EVIDENCE-BASED EXPLANATION API — NO LOCAL LLM REQUIRED
# =====================================================

def clean_field(value, fallback="Not recorded"):
    text = str(value or "").strip()
    return text if text else fallback


@app.route("/api/ask-ai", methods=["POST"])
def ask_ai():
    """
    Produce a deterministic explanation from the exact SQLite record and,
    where available, an exact-code RAG section. No generative model is used.
    """
    data = request.get_json(silent=True) or {}
    question = str(data.get("question", "")).strip()
    alarm = data.get("alarm") or {}
    alarm_code = str(alarm.get("alarm_code", "")).strip()
    controller = str(
        alarm.get("controller_model") or alarm.get("controller_scope") or ""
    ).strip()

    if not question:
        return jsonify({"success": False, "message": "Question is required."}), 400
    if not alarm_code:
        return jsonify({"success": False, "message": "Check an alarm before asking a question."}), 400

    # Simulated prototype alarms must never be presented as real CNC alarms.
    if normalize_code(alarm_code) in {"SIM-POS-MISMATCH", "SP0001"} and alarm.get("simulation", True):
        condition = str(alarm.get("condition") or "No condition details supplied.")
        telemetry = alarm.get("telemetry") or {}
        answer = (
            "Meaning:\nThis is a simulated prototype event, not an alarm received from a CNC controller.\n\n"
            "Documented information:\n"
            f"Simulated code: {alarm_code}\n"
            f"Simulated condition: {condition}\n"
            f"Potentiometer: {telemetry.get('pot', 'unknown')}; reported servo command: "
            f"{telemetry.get('servo_angle', 'unknown')} degrees.\n\n"
            "Safe next steps:\nUse this event only to test Vortiq's event-processing workflow. "
            "Do not use it as evidence of a real machine fault.\n\n"
            "What remains unverified:\nNo CNC controller, spindle-temperature measurement, or real alarm signal "
            "was used to generate this event."
        )
        return jsonify({
            "success": True, "answer": answer, "alarm_code": alarm_code,
            "source": "Vortiq simulated test event", "source_url": "",
            "section": "", "database_used": False, "rag_used": False,
            "simulation": True, "generator": "template"
        })

    try:
        db_alarm = find_alarm(controller, alarm_code)
    except Exception:
        app.logger.exception("Database lookup for Ask AI failed")
        return jsonify({"success": False, "message": "Could not read the alarm record from SQLite."}), 500

    if not db_alarm:
        return jsonify({
            "success": False,
            "message": "No unambiguous SQLite record matches this controller and alarm code. Re-check the alarm first."
        }), 404

    exact_record = retrieve_alarm_document(alarm_code)
    db_message = clean_field(db_alarm.get("alarm_message"))
    description = clean_field(db_alarm.get("description"))
    causes = clean_field(db_alarm.get("possible_causes"))
    action = clean_field(db_alarm.get("corrective_action"))
    source_manual = clean_field(db_alarm.get("source_manual"))
    severity = clean_field(db_alarm.get("severity"), "Not specified in the database")
    affected = clean_field(db_alarm.get("affected_component"))
    rag_text = exact_record["document"] if exact_record else ""

    # Surface conflicts rather than allowing a model to choose one silently.
    conflict = False
    if exact_record:
        for field_value in (db_message, description):
            if field_value != "Not recorded" and field_value.lower() not in rag_text.lower():
                conflict = True
                break

    meaning = description if description != "Not recorded" else (
        db_message if db_message != "Not recorded" else "No description is recorded."
    )
    documented = (
        f"Alarm message: {db_message}\n"
        f"Description: {description}\n"
        f"Possible causes (not confirmed): {causes}\n"
        f"Affected component: {affected}\n"
        f"Severity: {severity}"
    )
    if conflict:
        documented += "\nWarning: The SQLite record and exact-code RAG text may conflict. Verify against the applicable OEM manual."

    safe_steps = (
        action if action != "Not recorded"
        else "No corrective action is recorded. Consult the applicable OEM manual or a qualified CNC technician."
    )
    verification = (
        "An exact-code RAG section was found, but the source and its applicability still require verification."
        if exact_record else
        "No exact-code RAG section was found. The explanation uses the SQLite record only."
    )
    answer = (
        f"Meaning:\n{meaning}\n\n"
        f"Documented information:\n{documented}\n\n"
        f"Safe next steps:\n{safe_steps}\n"
        "Do not treat possible causes as a confirmed diagnosis or bypass safety procedures.\n\n"
        f"What remains unverified:\n{verification}"
    )

    return jsonify({
        "success": True,
        "answer": answer,
        "alarm_code": alarm_code,
        "source": db_alarm.get("source_manual") or (exact_record or {}).get("source", "Not recorded"),
        "source_url": db_alarm.get("source_url") or "",
        "section": (exact_record or {}).get("section", ""),
        "rag_used": exact_record is not None,
        "database_used": True,
        "generator": "template",
        "warning": "This is an evidence-based template, not a generative AI answer."
    })


# =====================================================
# ALARM HISTORY API (READ-ONLY)
# =====================================================

@app.route("/api/alarm-history", methods=["GET"])
def alarm_history():
    """Return recent records already stored in alarm_history; does not create events."""
    limit_raw = request.args.get("limit", "50")
    try:
        limit = max(1, min(int(limit_raw), 200))
    except (TypeError, ValueError):
        limit = 50

    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute('PRAGMA table_info("alarm_history")')
        columns = {row["name"] for row in cursor.fetchall()}
        required = {"id", "alarm_code", "raised_at", "cleared_at", "duration_seconds"}
        if not required.issubset(columns):
            return jsonify({
                "success": False,
                "message": "alarm_history table is missing required columns."
            }), 500

        optional = [
            "machine_id", "state_before_alarm", "state_during_alarm", "state_after_alarm"
        ]
        selected = ["id", "alarm_code", "raised_at", "cleared_at", "duration_seconds"]
        selected.extend(name for name in optional if name in columns)
        sql_columns = ", ".join(f'"{name}"' for name in selected)
        cursor.execute(
            f'SELECT {sql_columns} FROM "alarm_history" '
            f'ORDER BY raised_at DESC LIMIT ?',
            (limit,)
        )
        rows = [dict(row) for row in cursor.fetchall()]
        return jsonify({"success": True, "count": len(rows), "records": rows})
    except sqlite3.Error:
        app.logger.exception("Alarm history query failed")
        return jsonify({"success": False, "message": "Could not read alarm history."}), 500
    finally:
        conn.close()


# =====================================================
# HEALTH CHECK
# =====================================================

@app.route("/")
def home():
    return jsonify({
        "status": "running",
        "application": "Vortiq",
        "generator": "template",
        "database_available": DB_FILE.exists(),
        "rag_available": bool(rag_documents),
        "rag_sections": len(rag_documents),
        "rag_error": rag_init_error,
    })


# =====================================================
# START SERVER
# =====================================================

if __name__ == "__main__":
    print("=" * 50)
    print("Starting Vortiq backend")
    print("Database:", DB_FILE)
    print("Explanation generator: deterministic templates (no LLM required)")
    print("RAG source available:", bool(rag_documents))
    print("RAG sections:", len(rag_documents))
    print("Server: http://127.0.0.1:8000")
    print("=" * 50)
    app.run(host="127.0.0.1", port=8000, debug=False)
