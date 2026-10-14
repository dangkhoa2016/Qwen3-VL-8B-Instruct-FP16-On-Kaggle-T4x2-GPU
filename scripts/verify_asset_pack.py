#!/usr/bin/env python3
from pathlib import Path
import json, hashlib, sys

root=Path(sys.argv[1] if len(sys.argv)>1 else ".")
manifest=json.loads((root/"ASSET_MANIFEST.json").read_text())
errors=[]
for a in manifest["generated_assets"]:
    p=root/a["path"]
    if not p.exists():
        errors.append(f"MISSING synthetic asset: {a['path']}")
        continue
    h=hashlib.sha256(p.read_bytes()).hexdigest()
    if h != a["sha256"]:
        errors.append(f"HASH MISMATCH: {a['path']}")

cases=json.loads((root/"ground_truth/cases.json").read_text())
for c in cases:
    p=root/c["asset"]
    if not p.exists() and not c.get("requires_fetch",False):
        errors.append(f"CASE ASSET MISSING: {c['case_id']} -> {c['asset']}")

if errors:
    print("\n".join(errors))
    raise SystemExit(1)
print(f"ASSET_PACK_STATIC_VERIFY=PASS generated={len(manifest['generated_assets'])} cases={len(cases)}")
