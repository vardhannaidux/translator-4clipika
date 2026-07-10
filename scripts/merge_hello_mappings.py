import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_JSON = ROOT / 'data' / 'hello_mappings.json'
TXT_JSON = ROOT / 'data' / 'hello_mappings_txt.json'
OUT = CSV_JSON

def load(path):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return []

def key_of(r):
    return (r.get('KeyCode',''), tuple(r.get('FontBytes') or []))

def main():
    a = load(CSV_JSON)
    b = load(TXT_JSON)
    merged = []
    seen = set()
    for r in a + b:
        k = key_of(r)
        if k in seen:
            continue
        seen.add(k)
        merged.append(r)
    OUT.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding='utf-8')
    print('wrote', OUT, 'entries=', len(merged))

if __name__ == '__main__':
    main()
