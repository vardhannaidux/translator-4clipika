# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from translation_engine import translate_text

words = [
    "చైతన్య", "స్కూల్", "కలర్స్", "ఇంఛార్జి", "లక్ష్యం",
    "ల్స్", "స్వీకరణ", "పరిషత్", "బాబ్జి", "నాయుడు",
    "కట్", "అవుట్", "శుభాకాంక్షలు", "కాల్చి", "స్వీట్లు",
    "చెప్పారు", "ఫ్రెండ్స్", "స్టోర్స్", "త్", "ఆర్థోపెడిక్",
    "కృష్ణారావు", "కార్యాలయం", "రమేష్ రాజు", "అభివృద్ధి", "ఫ్లాష్",
    "ఉపాధ్యాయులు", "ఫిట్ నెస్"
]

getting = [
    "àµjêŸìu", "ú£«\\öËÀ", "ÚÛõôÂq", "ÏÙàÅ¦Jb", "õ¤ÛuÙ",
    "öËqÀ", "úˆyÚÛô¢é", "í£Jù£êÂ", "ò°Gb", "û¦óŸ³è[ª",
    "ÚÛæÀ", "Í÷±æÀ", "øŒ‰òÅ°Ú¥Ù¤Ûõª", "Ú¥La", "úˆyåªx",
    "àµð§pô¢ª", "všíÆÙèqÂ", "›ú¥dôÂq", "êÂ", "ÎôÂëÇÁšíè…ÚÂ",
    "ÚÛ”ú°gô¦÷±", "Ú¥ô¢uõóŸªÙ", "ô¢î¶ªù£ ô¦V", "ÍGÅ÷”CÌÄ", "ðÆ§xùÃ",
    "Ñð§ë¯uóŸ³õª", "íÆ‡æÀ ûµúÃ"
]

correct = [
    "àµjêŸìu", "ú£«\\öËÀ", "ÚÛõôÂq", "ÏÙàÅ¦Jb", "õ¤ÛuÙ",
    "öËÀq", "úˆyÚÛô¢é", "í£Jù£êÂ", "ò°Gb", "û¦óŸ³è[ª",
    "ÚÛæÀ", "Í÷±æÀ", "øŒ‰òÅ°Ú¥Ù¤Ûõª", "Ú¥La", "úˆyåªx",
    "àµð§pô¢ª", "všíÆÙèÂq", "þ¼dôÂq", "êÂ", "ÎôÁ–šíè…ÚÂ",
    "ÚÛ”ÿ§gô¦÷±", "Ú¥ô¦uõóŸªÙ", "ô¢î¶ªùÃô¦V", "ÍGÅ÷”CÌÄ", "ð§xùÃ",
    "Ñð§ëÅ¯uóŸ³õª", "íÆ‡æÀûµúÃ"
]

with open("sandbox/summary_report.txt", "w", encoding="utf-8") as f:
    f.write(f"{'Idx':<4} | {'Telugu Input':<15} | {'Getting in Prompt':<20} | {'Correct in Prompt':<20} | {'Engine Output (Ed)':<20} | Status\n")
    f.write("-" * 105 + "\n")
    for i, (w, g, c) in enumerate(zip(words, getting, correct)):
        cur_ed = translate_text(w, editorial_mode=True)
        status = "MATCHES CORRECT" if cur_ed == c else ("MATCHES GETTING" if cur_ed == g else "DIFFERENT")
        f.write(f"{i+1:<4} | {w:<15} | {g:<20} | {c:<20} | {cur_ed:<20} | {status}\n")

print("Report generated in sandbox/summary_report.txt")
