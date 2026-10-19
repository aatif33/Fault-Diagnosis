"""Vortiq direct FANUC FOCAS alarm monitor. Read-only API calls only.

Requires the OEM FANUC FOCAS library DLL matching Python architecture and CNC series.
No serial/Arduino input and no CNC write/control functions are called.
"""
import argparse
import ctypes
from ctypes import wintypes
import json
import platform
import time
from datetime import datetime
from pathlib import Path
import requests

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "cnc_config.json"
DEFAULT_CONFIG = {
    "machine_id": "CNC-FOCAS-01",
    "ip_address": "192.168.1.100",
    "port": 8193,
    "timeout_seconds": 3,
    "poll_interval_seconds": 1.0,
    "controller_model": "Unknown",
    "focas_dll_path": "",
    "max_alarm_messages": 50
}
API_BASE = "http://127.0.0.1:8000"
ALARM_TYPES = {0:"SW",1:"PW",2:"IO",3:"PS",4:"OT",5:"OH",6:"SV",7:"SR",8:"MC",9:"SP",10:"DS",11:"IE",12:"BG",13:"SN",15:"EX",19:"PC"}

class ODBALMMSG2(ctypes.Structure):
    # FOCAS fwlib32.h/fwlib64.h: long (32-bit), short fields, char[64]
    _pack_ = 4
    _fields_ = [("alm_no", ctypes.c_int32), ("type", ctypes.c_int16), ("axis", ctypes.c_int16),
                ("dummy", ctypes.c_int16), ("msg_len", ctypes.c_int16), ("alm_msg", ctypes.c_char * 64)]

def load_config():
    if not CONFIG_PATH.exists():
        CONFIG_PATH.write_text(json.dumps(DEFAULT_CONFIG, indent=2), encoding="utf-8")
        print(f"[SETUP] Created {CONFIG_PATH}. Edit ip_address before connecting.")
    cfg = DEFAULT_CONFIG.copy()
    cfg.update(json.loads(CONFIG_PATH.read_text(encoding="utf-8")))
    return cfg

def load_library(cfg):
    if platform.system() != "Windows":
        raise RuntimeError("This FOCAS DLL monitor currently requires Windows. Use the matching OEM FOCAS library for your OS.")
    candidates = []
    if cfg.get("focas_dll_path"):
        candidates.append(Path(cfg["focas_dll_path"]))
    candidates += [BASE_DIR / "Fwlib64.dll", BASE_DIR / "fwlib64.dll", BASE_DIR / "Fwlib32.dll", BASE_DIR / "fwlib32.dll"]
    dll_path = next((p for p in candidates if p.exists()), None)
    if not dll_path:
        raise FileNotFoundError("FANUC FOCAS DLL not found. Install/copy the licensed OEM FOCAS library matching your CNC and Python architecture, then set focas_dll_path in cnc_config.json.")
    loader = ctypes.WinDLL if hasattr(ctypes, "WinDLL") else ctypes.CDLL
    lib = loader(str(dll_path))
    lib.cnc_allclibhndl3.argtypes = [ctypes.c_char_p, ctypes.c_ushort, ctypes.c_int32, ctypes.POINTER(ctypes.c_ushort)]
    lib.cnc_allclibhndl3.restype = ctypes.c_int16
    lib.cnc_freelibhndl.argtypes = [ctypes.c_ushort]
    lib.cnc_freelibhndl.restype = ctypes.c_int16
    lib.cnc_rdalmmsg2.argtypes = [ctypes.c_ushort, ctypes.c_int16, ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ODBALMMSG2)]
    lib.cnc_rdalmmsg2.restype = ctypes.c_int16
    return lib, dll_path

def decode_alarm_text(raw):
    raw = raw.split(b"\\0", 1)[0]
    for encoding in ("ascii", "shift_jis", "cp1252"):
        try: return raw.decode(encoding).strip()
        except UnicodeDecodeError: pass
    return raw.decode("ascii", errors="replace").strip()

def read_alarms(lib, handle, max_count=50):
    # type=-1 asks FOCAS for all supported active alarm types. This is a read-only call.
    count = ctypes.c_int16(max(1, min(int(max_count), 50)))
    rows = (ODBALMMSG2 * count.value)()
    rc = lib.cnc_rdalmmsg2(handle, -1, ctypes.byref(count), rows)
    if rc != 0:
        raise RuntimeError(f"cnc_rdalmmsg2 failed with FOCAS return code {rc}")
    alarms = []
    for i in range(max(0, min(count.value, len(rows)))):
        row = rows[i]
        kind = ALARM_TYPES.get(int(row.type), f"TYPE{int(row.type)}")
        number = int(row.alm_no)
        message = decode_alarm_text(bytes(row.alm_msg))
        alarms.append({"alarm_number": number, "alarm_type": kind, "axis": int(row.axis) or None, "message": message, "alarm_code": f"{kind}{number:04d}"})
    # stable unique key; retain different types/axes even when alarm number matches
    unique = {}
    for a in alarms:
        key = (a["alarm_type"], a["alarm_number"], a["axis"], a["message"])
        unique[key] = a
    return list(unique.values())

def post_snapshot(session, payload):
    response = session.post(f"{API_BASE}/api/cnc-snapshot", json=payload, timeout=5)
    response.raise_for_status()
    return response.json()

def main():
    global CONFIG_PATH
    parser = argparse.ArgumentParser(description="Direct, read-only FANUC FOCAS alarm monitor")
    parser.add_argument("--config", default=str(CONFIG_PATH), help="Path to cnc_config.json")
    args = parser.parse_args()
    CONFIG_PATH = Path(args.config)
    cfg = load_config()
    print("Vortiq direct CNC alarm monitor — READ ONLY; no Arduino; no simulated alarms")
    print(f"Target: {cfg['ip_address']}:{cfg['port']} | controller model: {cfg.get('controller_model') or 'Unknown'}")
    lib = None; dll_path = None; handle = ctypes.c_ushort(0); connected = False
    session = requests.Session(); last_alarm_signature = None
    try:
        lib, dll_path = load_library(cfg)
        print(f"[FOCAS] Loaded OEM library: {dll_path}")
        while True:
            try:
                if not connected:
                    rc = lib.cnc_allclibhndl3(str(cfg["ip_address"]).encode("ascii"), int(cfg["port"]), int(cfg["timeout_seconds"]), ctypes.byref(handle))
                    if rc != 0:
                        raise RuntimeError(f"FOCAS connect failed with return code {rc}; check IP, port, FOCAS option, DLL and network.")
                    connected = True
                    print(f"[FOCAS] Connected read-only. Handle={handle.value}")
                alarms = read_alarms(lib, handle.value, cfg.get("max_alarm_messages", 50))
                payload = {"source":"FANUC_FOCAS_READ_ONLY", "connected":True, "machine_id":cfg["machine_id"],
                           "controller_model":cfg.get("controller_model") or "Unknown", "alarms":alarms,
                           "observed_at":datetime.now().astimezone().isoformat(timespec="seconds")}
                result = post_snapshot(session, payload)
                signature = tuple(sorted((a["alarm_type"], a["alarm_number"], a["axis"], a["message"]) for a in alarms))
                if signature != last_alarm_signature:
                    if alarms:
                        for a in alarms: print(f"[CNC ALARM] {a['alarm_code']} axis={a['axis'] or '-'} — {a['message'] or '(no message from controller)'}")
                    else: print("[CNC] Connected; controller reports no active alarm messages.")
                    print(f"[HISTORY] added={result.get('history_added',0)} closed={result.get('history_closed',0)}")
                    last_alarm_signature = signature
            except KeyboardInterrupt:
                break
            except Exception as exc:
                print(f"[FOCAS] DISCONNECTED / UNAVAILABLE: {exc}")
                try:
                    post_snapshot(session, {"source":"FANUC_FOCAS_READ_ONLY", "connected":False, "connection_error":str(exc), "machine_id":cfg.get("machine_id","CNC-FOCAS-01")})
                except Exception as post_exc:
                    print(f"[BACKEND] Could not report connection failure: {post_exc}")
                if connected and lib is not None:
                    try: lib.cnc_freelibhndl(handle.value)
                    except Exception: pass
                connected = False; last_alarm_signature = None
            time.sleep(max(0.25, float(cfg.get("poll_interval_seconds", 1.0))))
    except KeyboardInterrupt:
        pass
    except Exception as exc:
        print(f"[STARTUP ERROR] {exc}")
        try: post_snapshot(session, {"source":"FANUC_FOCAS_READ_ONLY", "connected":False, "connection_error":str(exc), "machine_id":cfg.get("machine_id","CNC-FOCAS-01")})
        except Exception: pass
    finally:
        if connected and lib is not None:
            try: lib.cnc_freelibhndl(handle.value)
            except Exception: pass
        print("Monitor stopped. No CNC write/control functions were called.")

if __name__ == "__main__":
    main()
