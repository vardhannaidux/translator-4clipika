import ast
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / 'sandbox' / 'hello_imported_overrides.py'

def load_overrides(path):
    src = path.read_text(encoding='utf-8')
    # exec in a restricted namespace
    ns = {}
    exec(src, ns)
    return ns.get('HELLO_IMPORTED_OVERRIDES', {})

def is_telugu(s):
    return any('\u0c00' <= ch <= '\u0c7f' for ch in s)

def clean_value(v):
    if not isinstance(v, str):
        return None
    # strip surrounding whitespace
    v2 = v.strip()
    if not v2:
        return None
    if not is_telugu(v2):
        return None
    return v2

def main():
    ov = load_overrides(SRC)
    cleaned = {}
    for k, v in ov.items():
        v2 = clean_value(v)
        if v2:
            cleaned[k] = v2

    # write back overwriting the original file
    with open(SRC, 'w', encoding='utf-8') as f:
        f.write('# Auto-generated cleaned overrides from hello_imported_overrides.py\n')
        f.write('HELLO_IMPORTED_OVERRIDES = {\n')
        for k, v in sorted(cleaned.items()):
            f.write(f'    {k}: {v!r},\n')
        f.write('}\n')

    print('wrote cleaned', SRC, 'entries=', len(cleaned))

if __name__ == '__main__':
    main()
