"""
Diagnostic: Compare engine output vs user's got vs user's expected
for each word in the sentence.
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

# Correct expected output (from user's report) — one per line
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

# Bad (got) output from user's report
got_words = [
    'ÑëÃë¶øŒÙ',     # ఉద్దేశం  (wrong)
    'šàjêŸìu',       # చైతన్య   (wrong)
    'ú£´eöËÀ',       # స్కూల్   (wrong)
    'ÚÛõôqÂ',        # కలర్స్   (wrong)
    'ÏÙMq',          # ఇంఛార్జి (wrong)
    'õË¶ÂóŸªÙ',     # లక్ష్యం  (wrong)
    'î¶ÞœªüŒx',     # వేగుళ్ల  (correct in bad!)
    'öËqÀ',          # మొక్కులు (wrong)
    'îµ³ÚÛªeõª',    # స్వీకరణ  (wrong)
    'þ§yÚÛô¢é',      # పరిషత్   (wrong)
    'í£Jù£êÃ',       # బాబ్జి   (wrong)
    'ñ°òËÀ>',        # నాయుడు   (wrong)
    'û¦óŸªè[ª',       # కటౌట్    (wrong)
    'ÚÛæ®åÃ',         # కట్      (wrong)
    'ÚÛåÃ',           # శుభాకాంక్షలు (wrong)
    'øŒ‰òÅ°ÚÛõª',   # కాల్చి   (wrong)
    'Ú¥õ‡a',         # స్వీట్లు (wrong)
    'þ§yåªx',         # అక్కడ    (wrong)
    'ÍÚÛ\\è[',        # చెప్పారు  (same)
    'àµí§pô¢ª',       # రెడ్డి   (wrong)
    '·ôè…"',          # ఫ్లాష్   (same)
    'ð§xùÃ',          # extra in bad?
]

print("=" * 70)
print("Word-by-word diagnostic")
print("=" * 70)

failures = []
for i, w in enumerate(words):
    result = translate_text(w)
    corr = correct_words[i] if i < len(correct_words) else '?'
    got = got_words[i] if i < len(got_words) else '?'
    match_correct = result == corr
    match_got = result == got
    status = 'CORRECT' if match_correct else ('BAD_GOT' if match_got else 'DIFFERENT')
    print(f'[{status}] {w}')
    if not match_correct:
        failures.append(w)
        print(f'  Expected: {repr(corr)}')
        print(f'  Got:      {repr(result)}')
        if not match_got:
            print(f'  OLD_BAD:  {repr(got)}')

print()
print(f"Total failures: {len(failures)}/{len(words)}")
print("Failing words:", failures)
