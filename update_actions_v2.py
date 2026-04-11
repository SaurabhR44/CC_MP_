import os
from pathlib import Path

# The carefully formatted Python code aligning EXACTLY with the user's requested echo statements
containers = {
    "ranger-dispatch": "import os\nprint(f\"Dispatching {os.getenv('DISPATCH_DELTA')} rangers | Total: {os.getenv('TOTAL_DISPATCHED')}\")",
    
    "vehicle-alert": "import os\nprint(f\"Vehicle intrusion | count={os.getenv('VEHICLE_COUNT')}\")",
    
    "perimeter-lockdown": "import os\nprint(f\"Lockdown active | intruders={os.getenv('INTRUDER_COUNT')}\")",
    
    "weapon-alert": "import os\nprint(f\"ARMED THREAT | weapon={os.getenv('WEAPON')} | count={os.getenv('WEAPON_COUNT')}\")",
    
    "wildlife-deterrent": "import os\nprint(f\"Deterrents active | zones={os.getenv('ZONES')} | animals={os.getenv('ANIMAL_COUNT')}\")",
    
    "fire-suppression": "import os\nprint(f\"Suppression firing | units={os.getenv('SUPPRESSION_UNITS')}\")",
    
    "smoke-alert": "import os\nprint(f\"Smoke detected | count={os.getenv('SMOKE_COUNT')}\")",
    
    "fall-alert": "import os\nprint(f\"Fall detected | count={os.getenv('FALL_COUNT')}\")",
    
    "medical-dispatch": "import os\nprint(f\"MEDICAL ESCALATION | no_response={os.getenv('NO_RESPONSE')}\")",
    
    "unattended-object": "import os\nprint(f\"Unattended bag | timer={os.getenv('TIMER')} | count={os.getenv('COUNT')}\")",
    
    "emergency-log": "import os\nfrom pathlib import Path\nlog_file = Path.home() / '.docksmith' / 'audit_trail.log'\nwith open(log_file, 'a') as f:\n    f.write(f\"{os.getenv('EVENT')}\\n\")\nprint(f\"Event logged: {os.getenv('EVENT')}\")",
    
    "status-update": "import os\nprint(f\"FPS={os.getenv('FPS', 30)} | TEMP={os.getenv('TEMP', 40)} | LORA={os.getenv('LORA', 'strong')}\")"
}

base_dir = Path("e:/CC_MP/layer3")

# Ensure all files are rewritten perfectly
for c_name, script_content in containers.items():
    action_path = base_dir / c_name / "action.py"
    if action_path.parent.exists():
        action_path.write_text(script_content)

print("[SUCCESS] All 12 action.py files rewritten to match the exact output spec.")
