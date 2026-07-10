import json
from pathlib import Path
import sys

# Ensure project root is on sys.path so `import translation_mappings` works when run from any cwd
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
import translation_mappings

DATA = ROOT / 'data' / 'hello_mappings.json'
OUT_JSON = ROOT / 'sandbox' / 'hello_conflicts.json'
OUT_CAND = ROOT / 'sandbox' / 'hello_candidates.json'
OUT_TXT = ROOT / 'sandbox' / 'hello_candidates.txt'
OUT_JSON.parent.mkdir(exist_ok=True)

def main():
    rows = json.loads(DATA.read_text(encoding='utf-8'))
    rm = getattr(translation_mappings, 'REVERSE_MAP', {})
    present = []
    missing = []
    for r in rows:
        fb = tuple(r.get('FontBytes') or [])
        if not fb:
            continue
        entry = {'FontBytes': fb, 'Keys': r.get('Keys'), 'KeyCode': r.get('KeyCode'), 'FontHex': r.get('FontHex')}
        if fb in rm:
            entry['mapped_to'] = rm[fb]
            present.append(entry)
        else:
            missing.append(entry)

    out = {'present_count': len(present), 'missing_count': len(missing), 'present': present, 'missing': missing}
    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
    OUT_CAND.write_text(json.dumps(missing, ensure_ascii=False, indent=2), encoding='utf-8')

    with open(OUT_TXT, 'w', encoding='utf-8') as f:
        for m in missing:
            fb = m['FontBytes']
            f.write(f"{tuple(fb)} -> # Keys={m['Keys']} KeyCode={m['KeyCode']} FontHex={m['FontHex']}\n")

    print('wrote', OUT_JSON, OUT_CAND, OUT_TXT)

if __name__ == '__main__':
    main()
