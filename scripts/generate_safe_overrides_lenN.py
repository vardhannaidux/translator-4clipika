from pathlib import Path
import ast

SRC = Path(__file__).resolve().parents[1] / 'sandbox' / 'hello_imported_overrides.py'
OUT = Path(__file__).resolve().parents[1] / 'sandbox' / 'hello_imported_overrides_safe.py'

def load_overrides(path):
    ns = {}
    src = path.read_text(encoding='utf-8')
    exec(src, ns)
    return ns.get('HELLO_IMPORTED_OVERRIDES', {})

def is_telugu(s):
    return all('\u0c00' <= ch <= '\u0c7f' for ch in s)

def main(max_len=3):
    ov = load_overrides(SRC)
    safe = {}
    for k, v in ov.items():
        if not isinstance(k, tuple):
            continue
        if len(k) > max_len:
            continue
        if not isinstance(v, str):
            continue
        v2 = v.strip()
        if not v2:
            continue
        # require Telugu-only (allowing typical combining marks in range)
        if not is_telugu(v2):
            continue
        safe[k] = v2

    with open(OUT, 'w', encoding='utf-8') as f:
        f.write('# Safe subset of imported overrides (1..%d bytes, Telugu-only)\n' % max_len)
        f.write('HELLO_IMPORTED_OVERRIDES_SAFE = {\n')
        for k, v in sorted(safe.items()):
            f.write(f'    {k}: {v!r},\n')
        f.write('}\n')

    print('wrote', OUT, 'entries=', len(safe))

if __name__ == '__main__':
    main(3)
