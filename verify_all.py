import subprocess

test_inputs = [
    "label=truck | conf=0.91 | count=1",
    "label=person | conf=0.87 | count=2",
    "label=rifle | conf=0.84 | count=1",
    "label=elephant | conf=0.93 | count=3",
    "label=smoke | conf=0.88 | count=1",
    "label=fire | conf=0.91 | count=1",
    "label=fall-detected | conf=0.89 | count=1",
    "label=backpack | conf=0.90 | count=1",
    "label=status-update | conf=1.0 | count=1"
]

print("--- VERIFYING ALL PRESCRIBED CHAINS ---")

for t in test_inputs:
    print(f"\n[TESTING INPUT]: {t}")
    result = subprocess.run(
        ["python", "receiver_format.py"],
        input=t + "\n",
        text=True,
        capture_output=True
    )
    # Print the lines containing '>>' or '[ACTION]' to strictly verify container run outputs
    for line in result.stdout.split('\n'):
        if ">>" in line or "[ACTION]" in line or "ENV:" in line or "[ERROR]" in line or "[TIMER]" in line:
            print("  " + line.strip())
            
    if result.stderr:
         print("  [CRITICAL ERROR]:", result.stderr.strip())

print("\n--- TEST COMPLETE ---")
