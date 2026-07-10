import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IN_FILE = ROOT / 'sandbox' / 'hello_candidates.json'
OUT_FILE = ROOT / 'sandbox' / 'hello_mappings_patch.py'

MAX_ENTRIES = 1000

def format_tuple(t):
    return '(' + ', '.join(str(x) for x in t) + ',)'

def main():
    data = json.loads(IN_FILE.read_text(encoding='utf-8'))
    # select candidate entries with small byte-length (1 or 2)
    small = [d for d in data if len(d.get('FontBytes', [])) in (1,2)]
    small = small[:MAX_ENTRIES]

    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        f.write('# Candidate mappings patch generated from hello_candidates.json\n')
        f.write('# Review each tuple and replace the placeholder string with the correct Unicode character.\n')
        f.write('CANDIDATE_OVERRIDES = {\n')
        for d in small:
            fb = tuple(d.get('FontBytes', []))
            if not fb:
                continue
            # write as Python tuple key
            key = tuple(fb)
            comment = f"# Keys={d.get('Keys')} KeyCode={d.get('KeyCode')} FontHex={d.get('FontHex')}"
            f.write(f"    {key}: 'REPLACE_WITH_CHAR', {comment}\n")
        f.write('}\n')

    print('wrote', OUT_FILE)

if __name__ == '__main__':
    main()
