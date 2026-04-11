import os
import shutil

containers = {
    "ranger-dispatch": 'import os\nprint(f"[ACTION] Dispatching {os.getenv(\"DISPATCH_COUNT\", os.getenv(\"VEHICLE_COUNT\", 1)) * 2} Rangers.")',
    "vehicle-alert": 'import os\nprint(f"[ACTION] Notifying ranger station: {os.getenv(\"VEHICLE_COUNT\", 1)} vehicle(s) detected.")',
    "perimeter-lockdown": 'import os\nprint(f"[ACTION] Locking perimeter gates in zone: {os.getenv(\"ZONE\", \"unknown\")}")',
    "weapon-alert": 'import os\nprint(f"[ACTION] Silent authority uplink initiated for {os.getenv(\"WEAPON\", \"weapon\")}.")',
    "wildlife-deterrent": 'import os\nprint(f"[ACTION] Sonic emitters fired for {os.getenv(\"ANIMAL_COUNT\", 1)} {os.getenv(\"ANIMAL\", \"animal\")}(s).")',
    "fire-suppression": 'import os\nprint(f"[ACTION] Active suppression. Units deployed: {os.getenv(\"SUPPRESSION_UNITS\", 1)}.")',
    "smoke-alert": 'import os\nprint(f"[ACTION] Air sensors pinged. Smoke plumes: {os.getenv(\"SMOKE_COUNT\", 1)}.")',
    "fall-alert": 'import os\nprint(f"[ACTION] Voice verification broadcasted to: {os.getenv(\"ZONE\", \"unknown\")}.")',
    "medical-dispatch": 'import os\nprint(f"[ACTION] Ambulance dispatched. Fall count: {os.getenv(\"FALL_COUNT\", 1)}")',
    "unattended-object": 'import os\nprint(f"[ACTION] Burst snapshot taken for {os.getenv(\"OBJECT\", \"object\")} after {os.getenv(\"TIMER\", 20)}s.")',
    "emergency-log": "import os\nwith open('/tmp/audit_trail.log', 'a') as f:\n    f.write(f'LOG: {os.getenv(\"EVENT\", \"Unknown\")}\\n')\nprint('[ACTION] Event appended to audit trail.')",
    "status-update": 'import os\nprint(f"[ACTION] Health Ping -> FPS:{os.getenv(\"FPS\", 30)} TEMP:{os.getenv(\"TEMP\", 40)} LORA:{os.getenv(\"LORA\", \"nominal\")}")'
}

base_dir = "e:/CC_MP/layer3"

# Clear existing contents
if os.path.exists(base_dir):
    shutil.rmtree(base_dir, ignore_errors=True)
os.makedirs(base_dir, exist_ok=True)

for c_name, script_content in containers.items():
    c_path = os.path.join(base_dir, c_name)
    os.makedirs(c_path, exist_ok=True)
    
    # Write python script
    with open(os.path.join(c_path, "action.py"), "w") as f:
        f.write(script_content)
        
    # Write Docksmithfile
    with open(os.path.join(c_path, "Docksmithfile"), "w") as f:
        f.write('FROM alpine:latest\n')
        f.write('COPY action.py /app/action.py\n')
        f.write('WORKDIR /app\n')
        # We need python to run the script. For alpine, it might not have python. 
        # But we previously used alpine and python in the prompt: "use alpine, PIP install out of scope but we can use base". Let's run just sh echo if we want strictly zero deps, but wait, python base was listed in docksmith images previously.
        # Let's use python:3.9-slim which exists according to `docksmith images` output.
        f.write('FROM python:3.9-slim\n')
        f.write('COPY action.py /app/action.py\n')
        f.write('WORKDIR /app\n')
        f.write('CMD ["python", "action.py"]\n')

print("12 Layer3 containers successfully scaffolded.")
