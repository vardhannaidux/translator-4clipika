# -*- coding: utf-8 -*-
"""Generate review artifacts from proposals and committed proposals."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
PROPOSALS = ROOT / 'sandbox' / 'ini_mismatch_proposals.py'
COMMITTED = ROOT / 'sandbox' / 'committed_proposals.py'
OUT_CSV = ROOT / 'sandbox' / 'proposals_review.csv'
OUT_MD = ROOT / 'CHANGES_COMMITTED_PROPOSALS.md'

ns = {}
if PROPOSALS.exists():
    exec(PROPOSALS.read_text(encoding='utf-8'), ns)
proposals = ns.get('INI_MISMATCH_PROPOSALS', {})
ns = {}
if COMMITTED.exists():
    exec(COMMITTED.read_text(encoding='utf-8'), ns)
committed = ns.get('COMMITTED_PROPOSALS', {})

# Build CSV
lines = ["key,proposed_unicode,accepted"]
for k, v in proposals.items():
    key_str = ' '.join(str(x) for x in k)
    accepted = 'yes' if k in committed else 'no'
    # escape commas in v
    v_safe = v.replace(',', '\\,') if isinstance(v, str) else str(v)
    lines.append(f'"{key_str}","{v_safe}",{accepted}')

OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
OUT_CSV.write_text('\n'.join(lines), encoding='utf-8')

# Write changelog for committed proposals
ch_lines = ["# Committed proposals integrated into translation_mappings.py", "", "The following proposals were accepted by the conservative batch tester and have been embedded into `translation_mappings.py` (EMBEDDED_COMMITTED_PROPOSALS).", "", "Entries:", ""]
for k, v in committed.items():
    ch_lines.append(f'- {tuple(k)} => {v}')

OUT_MD.write_text('\n'.join(ch_lines), encoding='utf-8')
print('Wrote', OUT_CSV, 'and', OUT_MD)
