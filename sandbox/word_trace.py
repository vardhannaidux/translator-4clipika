"""
Trace all failing words including PHRASE interference.
"""
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.stdout.reconfigure(encoding='utf-8')
import translation_mappings as tm
from translation_engine import assemble_syllable, translate_text
from linguistic_utils import segmentize

def word_trace(word, expected=None):
    """Trace a word through phrase matching then assembly."""
    print(f"\n=== {word} ===")
    
    # Check phrase match
    sorted_phrases = sorted(tm.PHRASE_MAPPINGS.keys(), key=len, reverse=True)
    i = 0
    phrase_consumed = []
    remaining = word
    while remaining:
        matched = False
        for k in sorted_phrases:
            if remaining.startswith(k):
                phrase_consumed.append((k, tm.PHRASE_MAPPINGS[k]))
                remaining = remaining[len(k):]
                matched = True
                break
        if not matched:
            phrase_consumed.append((remaining[0], None))
            remaining = remaining[1:]
    
    print(f"  Phrase matches: {[(k, [ord(c) for c in v] if v else None) for k,v in phrase_consumed]}")
    
    # Show syllable assembly for non-phrase parts
    syls = segmentize(word)
    total_bytes = []
    for s in syls:
        b = assemble_syllable(s)
        total_bytes.extend(b)
        print(f"  syllable {s.get('raw','?')!r}: {b}")
    
    print(f"  Assembly output bytes: {total_bytes}")
    actual = translate_text(word)
    actual_bytes = [ord(c) for c in actual]
    print(f"  translate_text bytes:  {actual_bytes}")
    if expected:
        exp_bytes = [ord(c) for c in expected]
        print(f"  Expected bytes:        {exp_bytes}")
        match = actual_bytes == exp_bytes
        print(f"  Match: {match}")

# Cases with confirmed issues
word_trace('ఉద్దేశం',     'iÑë¶ÌÄøŒÙ')
word_trace('చైతన్య',      'àµjêŸìu')
word_trace('స్కూల్',      'ú£«\x5CöËÀ')  
word_trace('కలర్స్',      'ÚÛõôÂq')
word_trace('ఇంఛార్జి',    'ÏÙàÅ¦Jb')
word_trace('లక్ష్యం',     'õ¤ÛuÙ')
word_trace('మొక్కులు',    'îµ³ÚÛª\x5Cõª')
word_trace('స్వీకరణ',     'úˆyÚÛô¢é')
word_trace('పరిషత్',      'í£Jù£êÂ')
word_trace('బాబ్జి',       'ò°Gb')
word_trace('నాయుడు',       'û¦óŸ³è[ª')
word_trace('కటౌట్',        'ÚÛæ®æÀ')
word_trace('కట్',          'ÚÛæÀ')
word_trace('శుభాకాంక్షలు', 'øŒ‰òÅ°Ú¥Ù¤Ûõª')
word_trace('కాల్చి',       'Ú¥La')
word_trace('స్వీట్లు',     'úˆyåªx')
word_trace('చెప్పారు',     'àµð§pô¢ª')
word_trace('రెడ్డి',       '·ôè…"')
word_trace('ఫ్లాష్',       'ðÆ§xùÃ')
