import sqlite3
import csv
import os

DB_FILE = "vortiq.db"
DATA_FOLDER = "data"


def get_connection():
    return sqlite3.connect(DB_FILE)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Alarm knowledge
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alarm_knowledge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT,
            machine_type TEXT,
            controller_model TEXT,
            alarm_code TEXT,
            alarm_message TEXT,
            description TEXT,
            possible_causes TEXT,
            corrective_action TEXT,
            affected_component TEXT,
            severity TEXT,
            source_manual TEXT,
            source_url TEXT,
            UNIQUE(brand, controller_model, alarm_code)
        )
    """)

    # Machines
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS machines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_id TEXT UNIQUE,
            machine_name TEXT,
            brand TEXT,
            controller_model TEXT,
            machine_type TEXT,
            connection_type TEXT,
            last_seen TEXT
        )
    """)

    # Machine events
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS machine_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_id TEXT,
            timestamp TEXT,
            event_type TEXT,
            machine_state TEXT,
            alarm_code TEXT,
            spindle_state TEXT,
            program_state TEXT
        )
    """)

    # Alarm history
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alarm_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_id TEXT,
            alarm_code TEXT,
            raised_at TEXT,
            cleared_at TEXT,
            duration_seconds INTEGER,
            state_before_alarm TEXT,
            state_during_alarm TEXT,
            state_after_alarm TEXT
        )
    """)

    conn.commit()
    conn.close()


def clean(value):
    if value is None:
        return ""
    return str(value).strip()


def import_alarm_csv(filename):
    path = os.path.join(DATA_FOLDER, filename)

    if not os.path.exists(path):
        print(f"File not found: {path}")
        return

    conn = get_connection()
    cursor = conn.cursor()

    with open(path, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:

            brand = clean(row.get("brand"))
            machine_type = clean(row.get("machine_type"))
            controller_model = clean(row.get("controller_model"))
            alarm_code = clean(row.get("alarm_code"))

            alarm_message = clean(row.get("alarm_message"))

            description = clean(
                row.get("official_description")
                or row.get("description")
            )

            possible_causes = clean(
                row.get("documented_possible_causes")
                or row.get("possible_causes")
            )

            corrective_action = clean(
                row.get("documented_troubleshooting_direction")
                or row.get("corrective_action")
            )

            affected_component = clean(
                row.get("affected_component")
            )

            severity = clean(
                row.get("severity")
            )

            source_manual = clean(
                row.get("source_manual")
                or row.get("source_document")
            )

            source_url = clean(
                row.get("source_url")
            )

            if not alarm_code:
                continue

            cursor.execute("""
                INSERT OR REPLACE INTO alarm_knowledge (
                    brand,
                    machine_type,
                    controller_model,
                    alarm_code,
                    alarm_message,
                    description,
                    possible_causes,
                    corrective_action,
                    affected_component,
                    severity,
                    source_manual,
                    source_url
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                brand,
                machine_type,
                controller_model,
                alarm_code,
                alarm_message,
                description,
                possible_causes,
                corrective_action,
                affected_component,
                severity,
                source_manual,
                source_url
            ))

    conn.commit()
    conn.close()

    print(f"Imported: {filename}")


def initialize_database():

    create_tables()

    import_alarm_csv("alarm.csv")
    import_alarm_csv("alarm2.csv")
    import_alarm_csv("alarm3.csv")

    print("\nVortiq database created successfully.")


if __name__ == "__main__":
    initialize_database()