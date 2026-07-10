import json
from pathlib import Path

IN = Path(__file__).resolve().parents[1] / 'sandbox' / 'ini_mismatches.json'
OUT = Path(__file__).resolve().parents[1] / 'sandbox' / 'ini_mismatch_proposals.py'

def main(n=50):
    data = json.loads(IN.read_text(encoding='utf-8'))
    proposals = []
    for item in data:
        gen = item.get('gen') or []
        decoded = item.get('decoded') or ''
        if not gen:
            continue
        proposals.append((tuple(gen), decoded))
        if len(proposals) >= n:
            break

    with open(OUT, 'w', encoding='utf-8') as f:
        f.write('# Auto-generated mismatch proposals: map engine-generated legacy bytes -> decoded Unicode\n')
        f.write('INI_MISMATCH_PROPOSALS = {\n')
        for k, v in proposals:
            f.write(f'    {k}: {v!r},\n')
        f.write('}\n')

    print('wrote', OUT, 'entries=', len(proposals))

if __name__ == "__main__":
    main()
