import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'hello_mappings.json'
KEYMAP = ROOT / 'sandbox' / 'ini_key_to_char.json'
OUT = ROOT / 'sandbox' / 'hello_imported_overrides.py'

def load_json(p):
    return json.loads(p.read_text(encoding='utf-8'))

def split_keycode(s, keyset):
    # DP: return list of ints if possible, else None
    n = len(s)
    dp = [None] * (n + 1)
    dp[0] = []
    for i in range(n):
        if dp[i] is None: continue
        # try 3,2,1 digit pieces
        for l in (3,2,1):
            if i + l <= n:
                piece = s[i:i+l]
                if piece in keyset:
                    dp[i+l] = dp[i] + [int(piece)]
    return dp[n]

def is_telugu(s):
    return any('\u0c00' <= ch <= '\u0c7f' for ch in s)

def main():
    data = load_json(DATA)
    keymap = load_json(KEYMAP)
    keyset = set(keymap.keys())

    # attempt to import translation_mappings.REVERSE_MAP to avoid duplicates
    try:
        sys.path.insert(0, str(ROOT))
        import translation_mappings
        existing = set(translation_mappings.REVERSE_MAP.keys())
    except Exception:
        existing = set()

    overrides = {}
    for r in data:
        fb = tuple(r.get('FontBytes') or [])
        if not fb: continue
        keycode = str(r.get('KeyCode','')).strip()
        if not keycode: continue
        parts = split_keycode(keycode, keyset)
        if not parts:
            continue
        unicode_chars = []
        for p in parts:
            v = keymap.get(str(p))
            if not v:
                unicode_chars = []
                break
            unicode_chars.append(v)
        if not unicode_chars:
            continue
        uni = ''.join(unicode_chars)
        if not is_telugu(uni):
            # still include if contains halant or other combining marks
            pass
        if fb in existing:
            continue
        overrides[fb] = uni

    # write out Python module
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write('# Auto-generated overrides from hello_mappings.json\n')
        f.write('HELLO_IMPORTED_OVERRIDES = {\n')
        for k, v in sorted(overrides.items()):
            f.write(f'    {k}: {v!r},\n')
        f.write('}\n')

    print('wrote', OUT, 'entries=', len(overrides))

if __name__ == '__main__':
    main()
