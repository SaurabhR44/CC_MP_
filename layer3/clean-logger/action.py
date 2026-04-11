import os
from pathlib import Path
log_file = Path.home() / ".docksmith" / "audit_trail.log"
with open(log_file, "a") as f:
    f.write(f"[{os.getenv('TIMESTAMP')}] {os.getenv('LOG_MESSAGE')}\n")