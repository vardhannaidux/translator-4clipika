"""
Pre-fix verification: run GROUND_TRUTH baseline, check scope of ఉ vowel change,
and confirm all expected bytes are correct before applying any changes.
"""
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.stdout.reconfigure(encoding='utf-8')
import translation_mappings as tm
from translation_engine import translate_text

print("=== GROUND_TRUTH BASELINE (must all pass BEFORE changes) ===")
all_pass = True
for w, expected in tm.GROUND_TRUTH:
    result = translate_text(w)
    res_bytes = [ord(c) for c in result]
    match = res_bytes == list(expected)
    status = 'PASS' if match else 'FAIL'
    if not match:
        all_pass = False
        print(f"  [{status}] {w!r}")
        print(f"    Expected: {list(expected)}")
        print(f"    Got:      {res_bytes}")
    else:
        print(f"  [PASS] {w!r}")

print()
print("All GROUND_TRUTH pass:", all_pass)

print()
print("=== ఉ VOWEL SCOPE CHECK ===")
# Check words that use standalone ఉ vowel
# If VOWELS['ఉ'] = [105, 209] that would affect all words starting with ఉ
test_u_words = ['ఉంటుంది', 'ఉద్దేశం', 'ఉత్సవం', 'ఉగాది']
for w in test_u_words:
    result = translate_text(w)
    res_bytes = [ord(c) for c in result]
    print(f"  {w}: {res_bytes}")
# Check GROUND_TRUTH for ఉంటుంది
for w, exp in tm.GROUND_TRUTH:
    if 'ఉ' in w:
        print(f"  GROUND_TRUTH {w!r}: expected={list(exp)}")

print()
print("=== PHRASE KEY SEARCH for స్వ family ===")
for k, v in sorted(tm.PHRASE_MAPPINGS.items(), key=lambda x: len(x[0]), reverse=True):
    if k.startswith('స్వ'):
        vbytes = [ord(c) for c in v]
        print(f"  PHRASE[{k!r}] = {vbytes}")

print()
print("=== PHRASE KEY SEARCH for లక్ష family ===")
for k, v in sorted(tm.PHRASE_MAPPINGS.items(), key=lambda x: len(x[0]), reverse=True):
    if k.startswith('లక్ష'):
        vbytes = [ord(c) for c in v]
        print(f"  PHRASE[{k!r}] = {vbytes}")

print()
print("=== CHECK పరిషత్ tail halant ===")
# పరిషత్ last bytes: expected 194, got 195
# 195 = tail_halant of స; what we want forత is 194
# tail halant of త in CONSONANTS:
ta = tm.U_TA
print("CONSONANTS[త].tail_halant:", tm.CONSONANTS.get(ta, {}).get('tail_halant', 'MISSING'))
# 194 is the tail_halant of cluster consonants
# The issue is the engine uses sa's tail_halant (195) instead of the right one
# Let's check what halant is applied for త్
from linguistic_utils import segmentize
from translation_engine import assemble_syllable
for w in ['పరిషత్', 'ప్రత్యేక', 'అత్యుత్తమ']:
    syls = segmentize(w)
    for s in syls:
        if 'త' in s.get('raw', '') and s.get('halant'):
            b = assemble_syllable(s)
            print(f"  {w}: {s.get('raw','?')} halant syl bytes: {b}")
