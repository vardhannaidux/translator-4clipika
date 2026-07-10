import re
import json
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / 'hello.txt'
OUT = Path(__file__).resolve().parents[1] / 'data' / 'hello_mappings_txt.json'
OUT.parent.mkdir(exist_ok=True)

re_section = re.compile(r"SECTION:\s*\[(.*?)\]")
re_index = re.compile(r"^\s*#\s*(\d+)\b")
re_keycode = re.compile(r"KeyCode=(\d+)")
re_bytes = re.compile(r"Bytes=\[(.*?)\]")

def find_ints(s):
    return [int(m.group()) for m in re.finditer(r"\b(\d+)\b", s)]

def main():
    rows = []
    section = None
    index = None
    keycode = ''
    with open(SRC, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            m = re_section.search(line)
            if m:
                section = m.group(1).strip()
                continue
            m = re_index.search(line)
            if m:
                index = m.group(1)
            m = re_keycode.search(line)
            if m:
                keycode = m.group(1)
            m = re_bytes.search(line)
            if m:
                inner = m.group(1)
                fb_list = find_ints(inner)
                rows.append({
                    'Section': section,
                    'SubGroup': '',
                    'Index': index or '',
                    'KeyCode': keycode or '',
                    'Keys': '',
                    'FontBytes': fb_list,
                    'FontHex': '',
                    'BackspaceCount': '',
                })
                # reset per-entry fields
                index = None
                keycode = ''

    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

    print('wrote', OUT, 'entries=', len(rows))

if __name__ == '__main__':
    main()
