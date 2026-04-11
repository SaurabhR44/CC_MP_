import subprocess
import time
import json
import sys
from pathlib import Path

def run_demo():
    print("=== DOCKSMITH SMART EMERGENCY SYSTEM DEMO ===")
    print("Scenario: A person falls and an ambulance is dispatched automatically.")
    print("------------------------------------------------------------\n")

    # Step 1: Simulate ML Cam detecting a fall
    fall_event = {"detections": [{"label": "fall", "confidence": 92}]}
    print(f"[ML CAM] Sending LoRa signal: {json.dumps(fall_event)}")
    
    # We'll use subprocess to run receiver_format.py and pipe the JSON to it
    # But since receiver_format.py is a loop, we'll simulate the orchestrator directly for the demo
    
    sys.path.insert(0, str(Path.cwd() / "docksmith"))
    from receiver_format import orchestrator

    print("\n--- Phase 1: Fall Detection ---")
    orchestrator.handle_detection("fall", 92)
    
    time.sleep(2)
    
    print("\n--- Phase 2: Automatic Ambulance Request ---")
    # In a real story, the 'fall' container might trigger this, 
    # but for the demo we simulate the 'ambulance' detection arriving
    ambulance_event = {"detections": [{"label": "ambulance", "confidence": 100}]}
    orchestrator.handle_detection("ambulance", 100)
    
    time.sleep(2)
    
    print("\n--- Phase 3: System Logging ---")
    orchestrator.handle_detection("log", 100)

    print("\n------------------------------------------------------------")
    print("DEMO COMPLETE: All response containers executed in isolation.")

if __name__ == "__main__":
    run_demo()
