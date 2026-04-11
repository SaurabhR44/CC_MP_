import os
import shutil
from pathlib import Path

containers = {
    "jeep-alert": 'import os\nprint(f"[ACTION] Jeep Detected (Count: {os.getenv(\'JEEP_COUNT\')}). Total Rangers: {os.getenv(\'JEEP_RANGERS\')}")',
    
    "person-escort": 'import os\nprint(f"[ACTION] Person Detected (Count: {os.getenv(\'PERSON_COUNT\')}). Total Escorts: {os.getenv(\'PERSON_ESCORTS\')}")',
    
    "gun-alert": 'import os\nprint(f"[ACTION] Gun Detected (Count: {os.getenv(\'GUN_COUNT\')}). Alerting rangers.")',
    
    "knife-alert": 'import os\nprint(f"[ACTION] Knife Detected (Count: {os.getenv(\'KNIFE_COUNT\')}). Alerting rangers.")',
    
    "elephant-quarantine": 'import os\nprint(f"[ACTION] Elephant Detected (Count: {os.getenv(\'ELEPHANT_COUNT\')}). Quarantine initiated.")\nprint("[INFO] Sanctuary alert sent. Floodlights active. Rangers diverted.")',
    
    "gunfire-sos": 'import os\nprint(f"[ACTION] Exchange of gunfire/Fall detected (Count: {os.getenv(\'IN_SOS_COUNT\')}). Alarms active.")\nprint("[INFO] 10s SOS window open.")',
    
    "medic-dispatch": 'import os\nstatus = os.getenv("MEDIC_TEAM")\ncount = os.getenv("FALL_COUNT", "Unknown")\nif status == "1":\n    print(f"[CRITICAL] No response. MEDIC TEAM DEPLOYED. Sending {count} reinforcements.")\nelse:\n    print("[INFO] SOS confirmed. Medic team not required.")',
    
    "fire-dispatch": 'import os\nprint(f"[ACTION] Fire detected (Count: {os.getenv(\'FIRE_COUNT\')}). Sending Fire Unit Team.")',
    
    "smoke-dispatch": 'import os\nprint(f"[ACTION] Smoke detected (Count: {os.getenv(\'SMOKE_COUNT\')}). Sending Fire Unit Team.")',
    
    "clean-logger": 'import os\nfrom pathlib import Path\nlog_file = Path.home() / ".docksmith" / "audit_trail.log"\nwith open(log_file, "a") as f:\n    f.write(f"[{os.getenv(\'TIMESTAMP\')}] {os.getenv(\'LOG_MESSAGE\')}\\n")'
}

base_dir = Path("e:/CC_MP/layer3")

if base_dir.exists():
    shutil.rmtree(base_dir, ignore_errors=True)
base_dir.mkdir(parents=True, exist_ok=True)

for c_name, script_content in containers.items():
    c_path = base_dir / c_name
    c_path.mkdir(parents=True, exist_ok=True)
    
    with open(c_path / "action.py", "w") as f:
        f.write(script_content)
        
    with open(c_path / "Docksmithfile", "w") as f:
        f.write('FROM alpine:latest\nCOPY action.py /app/\nWORKDIR /app\nCMD ["python3", "action.py"]\n')

print("Refined containers with count-logging scaffolded.")


