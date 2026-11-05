#!/usr/bin/env python3
"""Convert the canonical Mihomo EmbyDirect YAML list into sing-box source JSON."""
import json
import re
from pathlib import Path

source = Path("Rules/EmbyDirect.yaml")
output = Path("Rules/EmbyDirect.json")

domains = []
for line_number, line in enumerate(source.read_text(encoding="utf-8").splitlines(), 1):
    stripped = line.strip()
    if not stripped or stripped.startswith("#") or stripped == "payload:":
        continue
    match = re.fullmatch(r"\s*-\s*'DOMAIN,([^']+)'\s*(?:#.*)?", line)
    if not match:
        raise SystemExit(f"{source}:{line_number}: unsupported rule format: {line}")
    domain = match.group(1).strip().lower()
    if not re.fullmatch(r"[a-z0-9.-]+", domain) or domain.startswith(".") or domain.endswith(".") or ".." in domain:
        raise SystemExit(f"{source}:{line_number}: invalid domain: {domain}")
    if domain in domains:
        raise SystemExit(f"{source}:{line_number}: duplicate domain: {domain}")
    domains.append(domain)

if not domains:
    raise SystemExit("No domains found; refusing to generate an empty rule set.")

data = {
    "version": 1,
    "rules": [
        {
            "domain": domains
        }
    ]
}
output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Generated {output} with {len(domains)} exact-match domains.")
