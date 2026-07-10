import json
from sandbox.analyze_ini import parse_ini_keycodes
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / 'sandbox' / 'ini_key_to_char.json'
OUT.parent.mkdir(exist_ok=True)

def main():
    km = parse_ini_keycodes()
    # Normalize to string repr of unicode
    out = {str(k): v for k, v in km.items()}
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
    print('wrote', OUT)

if __name__ == '__main__':
    main()
