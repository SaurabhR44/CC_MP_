import time
import json
import re
import os
import sys
import threading
import serial
from datetime import datetime
from pathlib import Path

# Add docksmith module to path
sys.path.insert(0, str(Path.cwd() / "docksmith"))

from docksmith import DOCKSMITH_HOME
from manifest import Manifest
from runtime import ContainerRuntime

# ── 100% Precise ML State Initialization ─────────────────────────────────
state = {
    "jeep_count": 0,
    "jeep_rangers": 0,
    "person_count": 0,
    "person_escorts": 0,
    "gun_count": 0,
    "knife_count": 0,
    "elephant_count": 0,
    "fire_count": 0,
    "smoke_count": 0,
    "in_sos_count": 0,
    "fall_count": 0
}

images_dir = DOCKSMITH_HOME / "images"

def run_container(image_name, env_vars={}):
    image_tag = f"{image_name}:latest"
    safe_tag = image_tag.replace(":", "_")
    manifest_path = images_dir / f"{safe_tag}.json"
    
    if not manifest_path.exists():
        return

    manifest = Manifest.load(manifest_path)
    runtime = ContainerRuntime(DOCKSMITH_HOME, manifest)
    env = {str(k): str(v) for k, v in env_vars.items()}
    
    try:
        runtime.run(cmd_override=None, extra_env=env)
    except Exception as e:
        pass

def log_event(message, console=True):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if console:
        print(f"[{timestamp}] [LOG] {message}")
    run_container("clean-logger", {"TIMESTAMP": timestamp, "LOG_MESSAGE": message})

# ── Business Math Logic ──────────────────────────────────────────────

def sync_jeep_state(count):
    state["jeep_count"] = count # Absolute assignment for SX1261 frame sync
    needed = state["jeep_count"] * 2
    delta = needed - state["jeep_rangers"]
    if delta > 0:
        state["jeep_rangers"] += delta
        run_container("jeep-alert", {"JEEP_COUNT": state["jeep_count"], "JEEP_RANGERS": state["jeep_rangers"]})
        log_event(f"Action: Jeep Alert. Count: {state['jeep_count']}. New Deployment: {delta}. Total: {state['jeep_rangers']}.")

def sync_person_state(count):
    state["person_count"] = count # Absolute assignment
    needed = state["person_count"] + 1
    delta = needed - state["person_escorts"]
    if delta > 0:
        state["person_escorts"] += delta
        run_container("person-escort", {"PERSON_COUNT": state["person_count"], "PERSON_ESCORTS": state["person_escorts"]})
        log_event(f"Action: Person Escort. Count: {state['person_count']}. New Deployment: {delta}. Total: {state['person_escorts']}.")

sos_timer = None

def medic_escalation_logic(x):
    run_container("medic-dispatch", {"MEDIC_TEAM": "1", "FALL_COUNT": str(x)})
    log_event(f"Action: Medical Escalation. Fall Count: {x}. Result: Sending reinforcements: {x}.")

def handle_gunfire_or_sos(count, label):
    global sos_timer
    state["in_sos_count"] = count
    
    if "fall" in label or "detected" in label:
        state["fall_count"] = count
        run_container("gunfire-sos", {"IN_SOS_COUNT": state["fall_count"]})
        log_event(f"Action: Fall Detected. Fall Count: {state['fall_count']}. Opening 10s SOS window.")
    else:
        run_container("gunfire-sos", {"IN_SOS_COUNT": state["in_sos_count"]})
        log_event(f"Action: Exchange of Gunfire. Count: {state['in_sos_count']}. Opening 10s SOS window.")
    
    if sos_timer: sos_timer.cancel()
    sos_timer = threading.Timer(10.0, medic_escalation_logic, args=[count])
    sos_timer.start()

# ── ML Handler ────────────────────────────────────────────────────────────

def process_detections(detections):
    if detections:
        print("=== Parsed Detections ===")
    for det in detections:
        label = str(det.get("label", "unknown")).lower()
        count = int(det.get("count", 1))
        conf_raw = det.get("confidence", "0")
        
        # Format confidence display for console
        conf_list = [c.strip() for c in conf_raw.split(",")] if isinstance(conf_raw, str) else [str(conf_raw)]
        print(f"Label: {label}")
        print(f"Count: {count}")
        print(f"Confidence(s): {', '.join(conf_list)}%")
        print("-------------------------")
        
        if label == "jeep":
            sync_jeep_state(count)
        elif label == "person":
            sync_person_state(count)
        elif label == "gun":
            state["gun_count"] = count
            run_container("gun-alert", {"GUN_COUNT": count})
            log_event(f"Action: Gun Detected. Count: {count}. Alerting rangers.")
        elif label == "knife":
            state["knife_count"] = count
            run_container("knife-alert", {"KNIFE_COUNT": count})
            log_event(f"Action: Knife Detected. Count: {count}. Alerting rangers.")
        elif label == "elephant":
            state["elephant_count"] = count
            run_container("elephant-quarantine", {"ELEPHANT_COUNT": count})
            log_event(f"Action: Elephant Alert. Count: {count}. Quarantine active.")
        elif label in ["gunfire", "sos", "fall", "fall-detected", "person-fall"]:
            handle_gunfire_or_sos(count, label)
        elif label == "fire":
            state["fire_count"] = count
            run_container("fire-dispatch", {"FIRE_COUNT": count})
            log_event(f"Action: Fire Alert. Count: {count}. Dispatching fire unit.")
        elif label == "smoke":
            state["smoke_count"] = count
            run_container("smoke-dispatch", {"SMOKE_COUNT": count})
            log_event(f"Action: Smoke Alert. Count: {count}. Dispatching fire unit.")

# ── Main Serial Loop ──────────────────────────────────────────────────────

# Adjust to your COM port and baud rate
PORT = "COM8"
BAUD = 115200

print(f"\n--- LoRa Surveillance System (SX1262 Logic) ---")
print(f"Opening Serial Port: {PORT} at {BAUD} baud...")

try:
    ser = serial.Serial(PORT, BAUD, timeout=1)
except Exception as e:
    print(f"[CRITICAL ERROR] Could not open {PORT}: {e}")
    sys.exit(1)

print("Awaiting LoRa Packets...")

while True:
    try:
        raw_line = ser.readline().decode("utf-8", errors="ignore").strip()
        if not raw_line:
            continue

        # Look for JSON in the line
        match = re.search(r'(\{.*\})', raw_line)
        if match:
            try:
                data = json.loads(match.group(1))
                detections = data.get("detections", [])
                process_detections(detections)
            except json.JSONDecodeError:
                print(f"Invalid JSON in frame: {match.group(1)}")
        else:
            # Print radio stats lines (RSSI, SNR, Freq error) as requested
            if "SX1262" in raw_line or "RSSI" in raw_line or "SNR" in raw_line or "Freq error" in raw_line:
                print(f"[LORA STATS] {raw_line}")

    except (EOFError, KeyboardInterrupt):
        print("\nExiting...")
        if sos_timer: sos_timer.cancel()
        ser.close()
        break
    except Exception as e:
        print(f"[RUNTIME ERROR] {e}")




