import subprocess
import time

test_samples = [
    '{"detections":[{"label":"jeep","count":2,"confidence":"88, 83"}]}',
    '{"detections":[{"label":"gun","count":1,"confidence":"88"},{"label":"jeep","count":1,"confidence":"83"}]}',
    '{"detections":[{"label":"gunfire","count":1,"confidence":"90"}]}',
    '{"detections":[{"label":"elephant","count":2,"confidence":"78, 82"}]}',
    '{"detections":[{"label":"fire","count":1,"confidence":"83"},{"label":"smoke","count":1,"confidence":"83"}]}',
    '{"detections":[{"label":"gun","count":1,"confidence":"83"},{"label":"fire","count":1,"confidence":"83"},{"label":"knife","count":1,"confidence":"69"},{"label":"jeep","count":1,"confidence":"83"}]}'
]

print("--- FINAL SYSTEM VERIFICATION (6 SCENARIOS) ---")

for sample in test_samples:
    print(f"\n[INPUT]: {sample}")
    process = subprocess.Popen(
        ["python", "receiver_format.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(input=sample + "\n", timeout=15)
    
    # Filter output for actions and logs
    for line in stdout.split('\n'):
        if "[ACTION]" in line or "[DISPATCH]" in line or "[SYSTEM]" in line or "[SOS]" in line or "[ESCALE]" in line or "--> [LOGGED]" in line:
            print("  " + line.strip())
            
    if stderr:
        print("  [ERROR]:", stderr.strip())

print("\n--- VERIFICATION COMPLETE ---")
