"""
Verify translation engine directly with modified translation_mappings.py.
"""
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.stdout.reconfigure(encoding='utf-8')

from translation_engine import translate_text

words = [
    'ఉద్దేశం', 'చైతన్య', 'స్కూల్', 'కలర్స్', 'ఇంఛార్జి', 'లక్ష్యం',
    'వేగుళ్ల', 'మొక్కులు', 'స్వీకరణ', 'పరిషత్', 'బాబ్జి', 'నాయుడు',
    'కటౌట్', 'కట్', 'శుభాకాంక్షలు', 'కాల్చి', 'స్వీట్లు', 'అక్కడ',
    'చెప్పారు', 'రెడ్డి', 'ఫ్లాష్'
]

correct_words = [
    'iÑë¶ÌÄøŒÙ',    # ఉద్దేశం
    'àµjêŸìu',       # చైతన్య
    'ú£«\\öËÀ',      # స్కూల్
    'ÚÛõôÂq',        # కలర్స్
    'ÏÙàÅ¦Jb',       # ఇంఛార్జి
    'õ¤ÛuÙ',         # లక్ష్యం
    'î¶ÞœªüŒx',      # వేగుళ్ల
    'îµ³ÚÛª\\õª',    # మొక్కులు
    'úˆyÚÛô¢é',      # స్వీకరణ
    'í£Jù£êÂ',       # పరిషత్
    'ò°Gb',           # బాబ్జి
    'û¦óŸ³è[ª',       # నాయుడు
    'ÚÛæ®æÀ',         # కటౌట్
    'ÚÛæÀ',           # కట్
    'øŒ‰òÅ°Ú¥Ù¤Ûõª',  # శుభాకాంక్షలు
    'Ú¥La',           # కాల్చి
    'úˆyåªx',         # స్వీట్లు
    'ÍÚÛ\\è[',        # అక్కడ
    'àµð§pô¢ª',       # చెప్పారు
    '·ôè…"',          # రెడ్డి
    'ðÆ§xùÃ',         # ఫ్లాష్
]

print("=" * 70)
print("TESTING DIRECTLY FROM TRANSLATION_ENGINE.PY")
print("=" * 70)

passed = 0
for i, w in enumerate(words):
    result = translate_text(w)
    expected = correct_words[i]
    match = result == expected
    status = 'PASS' if match else 'FAIL'
    if match:
        passed += 1
        print(f"[{status}] {w}")
    else:
        print(f"[{status}] {w}")
        print(f"  Expected: {repr(expected)}")
        print(f"  Got:      {repr(result)}")

print()
print(f"Word-by-word result: {passed}/{len(words)} passed!")

full_input = 'ఉద్దేశం చైతన్య స్కూల్ కలర్స్ ఇంఛార్జి లక్ష్యం వేగుళ్ల మొక్కులు స్వీకరణ పరిషత్ బాబ్జి నాయుడు కటౌట్ కట్ శుభాకాంక్షలు కాల్చి స్వీట్లు అక్కడ చెప్పారు రెడ్డి ఫ్లాష్'
full_expected = 'iÑë¶ÌÄøŒÙ àµjêŸìu ú£«\\öËÀ ÚÛõôÂq ÏÙàÅ¦Jb õ¤ÛuÙ î¶ÞœªüŒx îµ³ÚÛª\\õª úˆyÚÛô¢é í£Jù£êÂ ò°Gb û¦óŸ³è[ª ÚÛæ®æÀ ÚÛæÀ øŒ‰òÅ°Ú¥Ù¤Ûõª Ú¥La úˆyåªx ÍÚÛ\\è[ àµð§pô¢ª ·ôè…\" ðÆ§xùÃ'

full_got = translate_text(full_input)
print()
print("Full Sentence Test:")
print("MATCH:", full_got == full_expected)
if full_got != full_expected:
    print("Expected:", repr(full_expected))
    print("Got:     ", repr(full_got))
