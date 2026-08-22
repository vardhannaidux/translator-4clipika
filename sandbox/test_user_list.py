# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from translation_engine import translate_text

words = [
    "చైతన్య",
    "స్కూల్",
    "కలర్స్",
    "ఇంఛార్జి",
    "లక్ష్యం",
    "ల్స్",
    "స్వీకరణ",
    "పరిషత్",
    "బాబ్జి",
    "నాయుడు",
    "కట్",
    "అవుట్",
    "శుభాకాంక్షలు",
    "కాల్చి",
    "స్వీట్లు",
    "చెప్పారు",
    "ఫ్రెండ్స్",
    "స్టోర్స్",
    "త్",
    "ఆర్థోపెడిక్",
    "కృష్ణారావు",
    "కార్యాలయం",
    "రమేష్ రాజు",
    "అభివృద్ధి",
    "ఫ్లాష్",
    "ఉపాధ్యాయులు",
    "ఫిట్ నెస్"
]

getting = [
    "àµjêŸìu",
    "ú£«\\öËÀ",
    "ÚÛõôÂq",
    "ÏÙàÅ¦Jb",
    "õ¤ÛuÙ",
    "öËqÀ",
    "úˆyÚÛô¢é",
    "í£Jù£êÂ",
    "ò°Gb",
    "û¦óŸ³è[ª",
    "ÚÛæÀ",
    "Í÷±æÀ",
    "øŒ‰òÅ°Ú¥Ù¤Ûõª",
    "Ú¥La",
    "úˆyåªx",
    "àµð§pô¢ª",
    "všíÆÙèqÂ",
    "›ú¥dôÂq",
    "êÂ",
    "ÎôÂëÇÁšíè…ÚÂ",
    "ÚÛ”ú°gô¦÷±",
    "Ú¥ô¢uõóŸªÙ",
    "ô¢î¶ªù£ ô¦V",
    "ÍGÅ÷”CÌÄ",
    "ðÆ§xùÃ",
    "Ñð§ë¯uóŸ³õª",
    "íÆ‡æÀ ûµúÃ"
]

correct = [
    "àµjêŸìu",
    "ú£«\\öËÀ",
    "ÚÛõôÂq",
    "ÏÙàÅ¦Jb",
    "õ¤ÛuÙ",
    "öËÀq",
    "úˆyÚÛô¢é",
    "í£Jù£êÂ",
    "ò°Gb",
    "û¦óŸ³è[ª",
    "ÚÛæÀ",
    "Í÷±æÀ",
    "øŒ‰òÅ°Ú¥Ù¤Ûõª",
    "Ú¥La",
    "úˆyåªx",
    "àµð§pô¢ª",
    "všíÆÙèÂq",
    "þ¼dôÂq",
    "êÂ",
    "ÎôÁ–šíè…ÚÂ",
    "ÚÛ”ÿ§gô¦÷±",
    "Ú¥ô¦uõóŸªÙ",
    "ô¢î¶ªùÃô¦V",
    "ÍGÅ÷”CÌÄ",
    "ð§xùÃ",
    "Ñð§ëÅ¯uóŸ³õª",
    "íÆ‡æÀûµúÃ"
]

with open("sandbox/user_list_results.txt", "w", encoding="utf-8") as f:
    for i, (w, g, c) in enumerate(zip(words, getting, correct)):
        act_ed = translate_text(w, editorial_mode=True)
        act_no_ed = translate_text(w, editorial_mode=False)
        m_ed = (act_ed == c)
        m_no_ed = (act_no_ed == c)
        f.write(f"{i+1:2d}. {w:<15} | Act(ed): {act_ed:<20} | Act(no_ed): {act_no_ed:<20} | Correct: {c:<20} | Ed Match: {m_ed} | NoEd Match: {m_no_ed}\n")
        if not m_ed:
            f.write(f"    DIFF (Ed vs Correct): Act_ords={[ord(x) for x in act_ed]} vs Cor_ords={[ord(x) for x in c]}\n")
            f.write(f"    Getting ords: {[ord(x) for x in g]}\n")

print("Done running user list script.")
