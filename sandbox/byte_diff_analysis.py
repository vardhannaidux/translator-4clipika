"""
Byte-level diff analysis to find patterns in expected vs got translations.
"""
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.stdout.reconfigure(encoding='utf-8')
from translation_engine import translate_text

# Each entry: (Telugu word, expected output string, description of what's wrong)
cases = [
    # BAD_GOT cases (our engine matches old-bad output, not correct)
    ('ఉద్దేశం',     'iÑë¶ÌÄøŒÙ'),
    ('చైతన్య',      'àµjêŸìu'),
    ('స్కూల్',      'ú£«\x5CöËÀ'),   # backslash = \x5C
    ('కలర్స్',      'ÚÛõôÂq'),
    ('ఇంఛార్జి',    'ÏÙàÅ¦Jb'),
    ('లక్ష్యం',     'õ¤ÛuÙ'),
    # DIFFERENT cases (our engine gives yet a 3rd different output)
    ('మొక్కులు',    'îµ³ÚÛª\x5Cõª'),  # backslash
    ('స్వీకరణ',     'úˆyÚÛô¢é'),
    ('పరిషత్',      'í£Jù£êÂ'),
    ('బాబ్జి',       'ò°Gb'),
    ('నాయుడు',       'û¦óŸ³è[ª'),
    ('కటౌట్',        'ÚÛæ®æÀ'),
    ('కట్',          'ÚÛæÀ'),
    ('శుభాకాంక్షలు', 'øŒ‰òÅ°Ú¥Ù¤Ûõª'),
    ('కాల్చి',       'Ú¥La'),
    ('స్వీట్లు',     'úˆyåªx'),
    ('చెప్పారు',     'àµð§pô¢ª'),
    ('రెడ్డి',       '·ôè…"'),
    ('ఫ్లాష్',       'ðÆ§xùÃ'),
]

print("=" * 80)
print("Byte-diff analysis: Expected vs Our Output")
print("=" * 80)

for word, expected in cases:
    result = translate_text(word)
    if result == expected:
        print(f"[OK] {word}")
        continue

    exp_bytes = [ord(c) for c in expected]
    got_bytes = [ord(c) for c in result]
    
    print(f"\n[FAIL] {word}")
    print(f"  Expected bytes: {exp_bytes}")
    print(f"  Got bytes:      {got_bytes}")
    
    # Find first differing position
    max_len = max(len(exp_bytes), len(got_bytes))
    for i in range(max_len):
        e = exp_bytes[i] if i < len(exp_bytes) else None
        g = got_bytes[i] if i < len(got_bytes) else None
        if e != g:
            print(f"  First diff at pos {i}: expected={e} ({chr(e) if e and e > 31 else '?'}), got={g} ({chr(g) if g and g > 31 else '?'})")
            break
    
    print(f"  Len diff: expected={len(exp_bytes)}, got={len(got_bytes)}")

print()
print("=" * 80)
print("Pattern grouping:")
print("=" * 80)

# For each word, show what byte positions differ and what they differ by
for word, expected in cases:
    result = translate_text(word)
    if result == expected:
        continue
    
    exp_bytes = [ord(c) for c in expected]
    got_bytes = [ord(c) for c in result]
    
    diffs = []
    for i in range(min(len(exp_bytes), len(got_bytes))):
        if exp_bytes[i] != got_bytes[i]:
            diffs.append(f"pos{i}: exp={exp_bytes[i]}, got={got_bytes[i]}")
    
    if len(exp_bytes) != len(got_bytes):
        diffs.append(f"length: exp={len(exp_bytes)}, got={len(got_bytes)}")
    
    print(f"{word}: {'; '.join(diffs[:3])}")
