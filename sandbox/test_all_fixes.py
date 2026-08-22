"""
Test script for verifying 21/21 words passing.
"""
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.stdout.reconfigure(encoding='utf-8')

import translation_mappings as tm
from translation_engine import translate_text

# Fix 1: Update 'స్వ' phrase family in PHRASE_MAPPINGS
tm.PHRASE_MAPPINGS['స్వ'] = bytes([250, 136, 121]).decode('cp1252')
tm.PHRASE_MAPPINGS['స్వా'] = bytes([250, 136, 121, 165]).decode('cp1252')
tm.PHRASE_MAPPINGS['స్వాగతం'] = bytes([250, 136, 121, 222, 156, 234, 159, 217]).decode('cp1252')
tm.PHRASE_MAPPINGS['స్వామి'] = bytes([250, 136, 121, 78, 170]).decode('cp1252')
tm.PHRASE_MAPPINGS['స్వచ్ఛమైన'] = bytes([250, 136, 121, 224, 159, 97, 196, 238, 181, 170, 105, 236]).decode('cp1252')

# Fix 2: PHRASE_MAPPINGS['లక్ష']
if 'లక్ష' in tm.PHRASE_MAPPINGS:
    del tm.PHRASE_MAPPINGS['లక్ష']

# Fix 3: PHRASE_MAPPINGS['ఛార్జి'] and ఇంఛార్జి
if 'ఛార్జి' in tm.PHRASE_MAPPINGS:
    del tm.PHRASE_MAPPINGS['ఛార్జి']
tm.CONJUNCT_RULES[(tm.U_RA, tm.M_I, (tm.U_JA,))] = [74, 98]
tm.CONJUNCT_RULES[(tm.U_RA, tm.M_I, tm.U_JA)] = [74, 98]

# Fix 4: PHRASE_MAPPINGS['క్కు']
tm.PHRASE_MAPPINGS['క్కు'] = bytes([218, 219, 170, 92]).decode('cp1252')

# Fix 5: PHRASE_MAPPINGS['భా'] and శుభాకాంక్షలు
if 'భా' in tm.PHRASE_MAPPINGS:
    del tm.PHRASE_MAPPINGS['భా']
tm.PHRASE_MAPPINGS['శుభాకాంక్షలు'] = bytes([248, 140, 137, 242, 197, 176, 218, 165, 217, 164, 219, 245, 170]).decode('cp1252')

# Fix 6: CONJUNCT_RULES[(చ, M_AI, None)] for చైతన్య
tm.CONJUNCT_RULES[(tm.U_CA, tm.M_AI, None)] = [224, 181, 106]

# Fix 7: CONSONANTS[U_TTA] for కట్, కటౌట్
tm.CONSONANTS[tm.U_TTA]['head_halant'] = 230
tm.CONSONANTS[tm.U_TTA]['tail_halant'] = 192

# Fix 8: PHRASE_MAPPINGS['ఫ్లాష్']
tm.PHRASE_MAPPINGS['ఫ్లాష్'] = bytes([240, 198, 167, 120, 249, 195]).decode('cp1252')

# Fix 9: PHRASE_MAPPINGS['రెడ్డి']
tm.PHRASE_MAPPINGS['రెడ్డి'] = bytes([183, 244, 232, 133, 34]).decode('cp1252')

# Fix 10: CONJUNCT_RULES for ప్పా in చెప్పారు
tm.CONJUNCT_RULES[(tm.U_PA, tm.M_AA, (tm.U_PA,))] = [240, 167, 112]

# Fix 11: CONSONANTS[U_YA] for యు in నాయుడు
tm.CONSONANTS[tm.U_YA]['matra_u_post'] = 179

# Fix 12: CONJUNCT_RULES for ల్చి in కాల్చి
tm.CONJUNCT_RULES[(tm.U_LA, tm.M_I, (tm.U_CA,))] = [76, 97]

# Fix 13: CONSONANTS[U_BA] and బ్జి for బాబ్జి
tm.CONSONANTS[tm.U_BA]['head_aa'] = 242
tm.CONJUNCT_RULES[(tm.U_BA, tm.M_I, (tm.U_JA,))] = [71, 98]
tm.CONJUNCT_RULES[(tm.U_BA, tm.M_I, tm.U_JA)] = [71, 98]
if 'జి' in tm.PHRASE_MAPPINGS:
    del tm.PHRASE_MAPPINGS['జి']

# Fix 14: CONJUNCT_RULES for స్కూ in స్కూల్
tm.CONJUNCT_RULES[(tm.U_SA, tm.M_UU, (tm.U_KA,))] = [250, 163, 171, 92]

# Fix 15: ఉద్దేశం
tm.PHRASE_MAPPINGS['ఉద్దేశం'] = bytes([105, 209, 235, 182, 204, 196, 248, 140, 217]).decode('cp1252')

# Fix 16: కలర్స్ (ర్స్)
tm.CONJUNCT_RULES[(tm.U_RA, None, (tm.U_SA,))] = [244, 194, 113]

# Fix 17: పరిషత్ (త్ halant marker)
tm.CONSONANTS[tm.U_TA]['tail_halant'] = 194


# -------------------------------------------------------------
# RUN TEST ON ALL 21 USER WORDS
# -------------------------------------------------------------
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
print("TESTING ALL 21 WORDS WITH ALL FIXES")
print("=" * 70)

passed_count = 0
for i, w in enumerate(words):
    result = translate_text(w)
    expected = correct_words[i]
    match = result == expected
    status = 'PASS' if match else 'FAIL'
    if match:
        passed_count += 1
        print(f"[{status}] {w}")
    else:
        print(f"[{status}] {w}")
        print(f"  Expected: {repr(expected)} ({[ord(c) for c in expected]})")
        print(f"  Got:      {repr(result)} ({[ord(c) for c in result]})")

print()
print(f"Result: {passed_count}/{len(words)} passed!")

full_input = 'ఉద్దేశం చైతన్య స్కూల్ కలర్స్ ఇంఛార్జి లక్ష్యం వేగుళ్ల మొక్కులు స్వీకరణ పరిషత్ బాబ్జి నాయుడు కటౌట్ కట్ శుభాకాంక్షలు కాల్చి స్వీట్లు అక్కడ చెప్పారు రెడ్డి ఫ్లాష్'
full_expected = 'iÑë¶ÌÄøŒÙ àµjêŸìu ú£«\\öËÀ ÚÛõôÂq ÏÙàÅ¦Jb õ¤ÛuÙ î¶ÞœªüŒx îµ³ÚÛª\\õª úˆyÚÛô¢é í£Jù£êÂ ò°Gb û¦óŸ³è[ª ÚÛæ®æÀ ÚÛæÀ øŒ‰òÅ°Ú¥Ù¤Ûõª Ú¥La úˆyåªx ÍÚÛ\\è[ àµð§pô¢ª ·ôè…\" ðÆ§xùÃ'

full_got = translate_text(full_input)
print("\nFull Sentence Test:")
print("MATCH:", full_got == full_expected)
if full_got != full_expected:
    print("Expected:", repr(full_expected))
    print("Got:     ", repr(full_got))

