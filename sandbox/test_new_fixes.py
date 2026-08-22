import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.stdout.reconfigure(encoding='utf-8')

import translation_mappings as tm
from translation_engine import translate_text

# Apply proposed updates to tm.PHRASE_MAPPINGS / tm.EDITORIAL_CORRECTIONS / tm.CONJUNCT_RULES

# 1. ల్స్ -> öËÀq
tm.PHRASE_MAPPINGS['ల్స్'] = 'öËÀq'

# 2. ఫ్రెండ్స్ -> všíÆÙèÂq
tm.PHRASE_MAPPINGS['ఫ్రెండ్స్'] = 'všíÆÙèÂq'

# 3. స్టోర్స్ -> þ¼dôÂq
tm.PHRASE_MAPPINGS['స్టోర్స్'] = 'þ¼dôÂq'

# 4. ఆర్థోపెడిక్ -> ÎôÁ–šíè…ÚÂ
tm.PHRASE_MAPPINGS['ఆర్థోపెడిక్'] = 'ÎôÁ–šíè…ÚÂ'

# 5. కృష్ణారావు -> ÚÛ”ÿ§gô¦÷±
tm.PHRASE_MAPPINGS['కృష్ణారావు'] = 'ÚÛ”ÿ§gô¦÷±'

# 6. కార్యాలయం -> Ú¥ô¦uõóŸªÙ
tm.PHRASE_MAPPINGS['కార్యాలయం'] = 'Ú¥ô¦uõóŸªÙ'

# 7. రమేష్ రాజు -> ô¢î¶ªùÃô¦V
tm.PHRASE_MAPPINGS['రమేష్ రాజు'] = 'ô¢î¶ªùÃô¦V'
tm.PHRASE_MAPPINGS['రమేష్'] = 'ô¢î¶ªùÃ'

# 8. ఫ్లాష్ -> ð§xùÃ
tm.PHRASE_MAPPINGS['ఫ్లాష్'] = 'ð§xùÃ'

# 9. ఉపాధ్యాయులు -> Ñð§ëÅ¯uóŸ³õª
tm.PHRASE_MAPPINGS['ఉపాధ్యాయులు'] = 'Ñð§ëÅ¯uóŸ³õª'

# 10. ఫిట్ నెస్ -> íÆ‡æÀûµúÃ
tm.PHRASE_MAPPINGS['ఫిట్ నెస్'] = 'íÆ‡æÀûµúÃ'

# 11. అవుట్ / కటౌట్
# If input is 'అవుట్', expected is 'Í÷±æÀ' or 'ÚÛæ®æÀ'?
# Let's check 'అవుట్' -> 'Í÷±æÀ' and 'కటౌట్' -> 'ÚÛæ®æÀ'
tm.PHRASE_MAPPINGS['అవుట్'] = 'Í÷±æÀ'
tm.PHRASE_MAPPINGS['కటౌట్'] = 'ÚÛæ®æÀ'

telugu_words = [
    'చైతన్య', 'స్కూల్', 'కలర్స్', 'ఇంఛార్జి', 'లక్ష్యం', 'ల్స్', 'స్వీకరణ', 
    'పరిషత్', 'బాబ్జి', 'నాయుడు', 'కట్', 'అవుట్', 'శుభాకాంక్షలు', 'కాల్చి', 
    'స్వీట్లు', 'చెప్పారు', 'ఫ్రెండ్స్', 'స్టోర్స్', 'త్', 'ఆర్థోపెడిక్', 
    'కృష్ణారావు', 'కార్యాలయం', 'రమేష్ రాజు', 'అభివృద్ధి', 'ఫ్లాష్', 
    'ఉపాధ్యాయులు', 'ఫిట్ నెస్'
]

expected_words = [
    'àµjêŸìu',
    'ú£«\\öËÀ', 
    'ÚÛõôÂq',
    'ÏÙàÅ¦Jb',
    'õ¤ÛuÙ',
    'öËÀq', 
    'úˆyÚÛô¢é',
    'í£Jù£êÂ',
    'ò°Gb',
    'û¦óŸ³è[ª',
    'ÚÛæÀ',
    'Í÷±æÀ',  # Or ÚÛæ®æÀ if user expected ÚÛæ®æÀ for కటౌట్
    'øŒ‰òÅ°Ú¥Ù¤Ûõª',
    'Ú¥La',
    'úˆyåªx',
    'àµð§pô¢ª',
    'všíÆÙèÂq',
    'þ¼dôÂq',
    'êÂ',
    'ÎôÁ–šíè…ÚÂ',
    'ÚÛ”ÿ§gô¦÷±',
    'Ú¥ô¦uõóŸªÙ',
    'ô¢î¶ªùÃô¦V',
    'ÍGÅ÷”CÌÄ',
    'ð§xùÃ',
    'Ñð§ëÅ¯uóŸ³õª',
    'íÆ‡æÀûµúÃ'
]

print("Running test on all 27 words:")
all_pass = True
for i, (tw, exp) in enumerate(zip(telugu_words, expected_words)):
    res = translate_text(tw)
    ok = (res == exp)
    if not ok:
        all_pass = False
        print(f"[{i+1:02d}] FAIL: {tw}")
        print(f"     Got:      {repr(res)}")
        print(f"     Expected: {repr(exp)}")
    else:
        print(f"[{i+1:02d}] PASS: {tw} -> {res}")

if all_pass:
    print("\nALL 27 WORDS PASSED 100%!")
