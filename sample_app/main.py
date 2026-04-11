import os

app_name = os.getenv("APP_NAME", "Unknown")
print(f"Hello from Docksmith! (APP_NAME={app_name})")
print("Files in current directory:")
for f in os.listdir("."):
    print(f" - {f}")

# Example of writing a file to test isolation
with open("test_internal.txt", "w") as f:
    f.write("This file should only exist inside the container root.")
print("Wrote test_internal.txt inside the container.")
