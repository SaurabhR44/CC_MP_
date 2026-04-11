import os
status = os.getenv("MEDIC_TEAM")
count = os.getenv("FALL_COUNT", "Unknown")
if status == "1":
    print(f"[CRITICAL] No response. MEDIC TEAM DEPLOYED. Sending {count} reinforcements.")
else:
    print("[INFO] SOS confirmed. Medic team not required.")