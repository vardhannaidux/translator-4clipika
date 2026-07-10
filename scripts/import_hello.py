import csv
import json
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / 'hello.csv'
OUT = Path(__file__).resolve().parents[1] / 'data' / 'hello_mappings.json'
OUT.parent.mkdir(exist_ok=True)

def parse_bytes_field(s):
    # FontBytes field like '225 145' or '32'
    parts = s.strip().split()
    out = []
    for p in parts:
        try:
            out.append(int(p))
        except Exception:
            # try comma-separated
            for q in p.split(','):
                try:
                    out.append(int(q))
                except Exception:
                    pass
    return out

def main():
    rows = []
    with open(SRC, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            fb = r.get('FontBytes','').strip()
            if not fb:
                fb_list = []
            else:
                fb_list = parse_bytes_field(fb)
            rows.append({
                'Section': r.get('Section'),
                'SubGroup': r.get('SubGroup'),
                'Index': r.get('Index'),
                'KeyCode': r.get('KeyCode'),
                'Keys': r.get('Keys'),
                'FontBytes': fb_list,
                'FontHex': r.get('FontHex'),
                'BackspaceCount': r.get('BackspaceCount'),
            })
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
    print('wrote', OUT)

if __name__ == '__main__':
    main()
