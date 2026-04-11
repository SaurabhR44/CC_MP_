import os
from pathlib import Path

# The carefully formatted Python code for each container, avoiding multi-quote f-string errors
containers = {
    "ranger-dispatch": "import os\nprint(f\"[ACTION] Dispatching {os.getenv('DISPATCH_COUNT', os.getenv('VEHICLE_COUNT', 1))} Rangers.\")",
    
    "vehicle-alert": "import os\nprint(f\"[ACTION] Notifying ranger station: {os.getenv('VEHICLE_COUNT', 1)} vehicle(s) detected.\")",
    
    "perimeter-lockdown": "import os\nprint(f\"[ACTION] Locking perimeter gates in zone: {os.getenv('ZONE', 'unknown')}\")",
    
    "weapon-alert": "import os\nprint(f\"[ACTION] Silent authority uplink initiated for {os.getenv('WEAPON', 'weapon')}.\")",
    
    "wildlife-deterrent": "import os\nprint(f\"[ACTION] Sonic emitters fired for {os.getenv('ANIMAL_COUNT', 1)} {os.getenv('ANIMAL', 'animal')}(s).\")",
    
    "fire-suppression": "import os\nprint(f\"[ACTION] Active suppression. Units deployed: {os.getenv('SUPPRESSION_UNITS', 1)}.\")",
    
    "smoke-alert": "import os\nprint(f\"[ACTION] Air sensors pinged. Smoke plumes: {os.getenv('SMOKE_COUNT', 1)}.\")",
    
    "fall-alert": "import os\nprint(f\"[ACTION] Voice verification broadcasted to: {os.getenv('ZONE', 'unknown')}.\")",
    
    "medical-dispatch": "import os\nprint(f\"[ACTION] Ambulance dispatched. Fall count: {os.getenv('FALL_COUNT', 1)}\")",
    
    "unattended-object": "import os\nprint(f\"[ACTION] Burst snapshot taken for {os.getenv('OBJECT', 'object')} after {os.getenv('TIMER', 20)}s.\")",
    
    "emergency-log": "import os\nfrom pathlib import Path\nlog_file = Path.home() / '.docksmith' / 'audit_trail.log'\nwith open(log_file, 'a') as f:\n    f.write(f\"LOG: {os.getenv('EVENT', 'Unknown')}\\n\")\nprint(f\"[ACTION] Event appended to audit trail at {log_file}\")",
    
    "status-update": "import os\nprint(f\"[ACTION] Health Ping -> FPS:{os.getenv('FPS', 30)} TEMP:{os.getenv('TEMP', 40)} LORA:{os.getenv('LORA', 'nominal')}\")"
}

base_dir = Path("e:/CC_MP/layer3")

# Ensure all files are rewritten perfectly
for c_name, script_content in containers.items():
    action_path = base_dir / c_name / "action.py"
    if action_path.parent.exists():
        action_path.write_text(script_content)

print("[SUCCESS] All 12 action.py files rewritten with correct string syntax.")
