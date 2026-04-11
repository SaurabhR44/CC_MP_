import sys
from pathlib import Path

# Add the docksmith module to path
sys.path.insert(0, str(Path.cwd() / "docksmith"))

from docksmith import DOCKSMITH_HOME, setup_docksmith_home
from builder import BuildEngine
from parser import DocksmithfileParser

# Ensure directories exist
setup_docksmith_home()

layer3_root = Path.cwd() / "layer3"
images_dir = DOCKSMITH_HOME / "images"

containers = [
    "jeep-alert", "person-escort", "gun-alert", "knife-alert",
    "elephant-quarantine", "gunfire-sos", "medic-dispatch",
    "fire-dispatch", "smoke-dispatch", "clean-logger"
]

print("--- BUILDING FINAL 10 ML CONTAINERS ---")
for folder_name in containers:
    image_tag = f"{folder_name}:latest"
    print(f"Building {image_tag} from layer3/{folder_name}...")
    
    context_path = layer3_root / folder_name
    docksmithfile = context_path / "Docksmithfile"
    
    if not docksmithfile.exists():
        print(f"  [ERROR] {docksmithfile} missing!")
        continue

    parser = DocksmithfileParser(docksmithfile)
    instructions = parser.parse()
    
    builder = BuildEngine(DOCKSMITH_HOME, context_path)
    try:
        builder.build(image_tag, instructions)
        print(f"  [SUCCESS] Built {image_tag}")
    except Exception as e:
        print(f"  [FAIL] {e}")

print("--- BUILD COMPLETE ---")
