"""
Vortiq PC Process Layer — Stage 1
Safe event normalization and alarm occurrence tracking.

This module does NOT connect to a CNC controller or send machine commands.
All demo events are explicitly SIMULATED. Real-controller events are blocked
until a verified, read-only adapter is implemented for the identified controller.
"""
from __future__ import annotations
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

EVENT_LOG = Path(__file__).with_name("events.jsonl")
ALLOWED_SOURCES = {"SIMULATED", "CONTROLLER"}
ALLOWED_MACHINE_STATES = {"RUNNING", "STOPPED", "IDLE", "UNKNOWN"}
ALLOWED_POWER_STATES = {"ON", "OFF", "UNKNOWN"}
ALLOWED_EVENT_TYPES = {"ALARM_RAISED", "ALARM_CLEARED", "STATUS_OBSERVED"}

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")

def normalize_event(raw: dict[str, Any], *, source: str) -> dict[str, Any]:
    source = source.strip().upper()
    if source not in ALLOWED_SOURCES:
        raise ValueError("source must be SIMULATED or CONTROLLER")
    if source == "CONTROLLER":
        raise ValueError(
            "Controller-origin events are disabled until a verified, read-only "
            "controller adapter is implemented."
        )

    event_type = str(raw.get("event_type", "")).strip().upper()
    if event_type not in ALLOWED_EVENT_TYPES:
        raise ValueError(f"Unsupported event_type: {event_type or '(empty)'}")
    machine_id = str(raw.get("machine_id", "")).strip()
    if not machine_id:
        raise ValueError("machine_id is required")

    alarm_code = str(raw.get("alarm_code", "")).strip() or None
    if event_type in {"ALARM_RAISED", "ALARM_CLEARED"} and not alarm_code:
        raise ValueError(f"alarm_code is required for {event_type}")

    machine_state = str(raw.get("machine_state", "UNKNOWN")).strip().upper()
    if machine_state not in ALLOWED_MACHINE_STATES:
        machine_state = "UNKNOWN"
    power_state = str(raw.get("power_state", "UNKNOWN")).strip().upper()
    if power_state not in ALLOWED_POWER_STATES:
        power_state = "UNKNOWN"

    return {
        "event_id": str(uuid.uuid4()),
        "machine_id": machine_id,
        "source": "SIMULATED",
        "is_real_controller_data": False,
        "event_type": event_type,
        "alarm_code": alarm_code,
        "machine_state": machine_state,
        "power_state": power_state,
        "controller_timestamp": None,
        "observed_at_utc": utc_now(),
        "timestamp_kind": "APPLICATION_OBSERVED",
        "payload": raw.get("payload", {}),
    }

def append_event(event: dict[str, Any], log_path: Path = EVENT_LOG) -> None:
    """Append-only history; never overwrites existing event records."""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

def process_event(raw: dict[str, Any], *, source: str = "SIMULATED",
                  log_path: Path = EVENT_LOG) -> dict[str, Any]:
    event = normalize_event(raw, source=source)
    append_event(event, log_path)
    return event

def read_events(log_path: Path = EVENT_LOG) -> list[dict[str, Any]]:
    if not log_path.exists():
        return []
    events = []
    with log_path.open("r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            if not line.strip():
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on line {line_number}: {exc}") from exc
    return events

def active_alarms(log_path: Path = EVENT_LOG) -> list[dict[str, Any]]:
    """Derive active alarms from history without mutating past events."""
    active = {}
    for event in read_events(log_path):
        code = (event.get("alarm_code") or "").upper()
        if not code:
            continue
        key = (event["machine_id"], code)
        if event["event_type"] == "ALARM_RAISED":
            active[key] = event
        elif event["event_type"] == "ALARM_CLEARED":
            active.pop(key, None)
    return list(active.values())

if __name__ == "__main__":
    demo_log = Path(__file__).with_name("demo_events.jsonl")
    demo = {
        "machine_id": "SIM-CNC-01",
        "event_type": "ALARM_RAISED",
        "alarm_code": "DEMO-0001",
        "machine_state": "UNKNOWN",
        "power_state": "UNKNOWN",
        "payload": {"note": "Demo only; not read from a CNC controller."},
    }
    saved = process_event(demo, source="SIMULATED", log_path=demo_log)
    print("Vortiq Stage 1 demo")
    print("Data source:", saved["source"])
    print("Real controller data:", saved["is_real_controller_data"])
    print("Event:", json.dumps(saved, indent=2))
    print("Demo log:", demo_log)
