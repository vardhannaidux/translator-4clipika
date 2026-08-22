import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.stdout.reconfigure(encoding='utf-8')
from translation_engine import translate_text

telugu_raw = """చైతన్య 
స్కూల్ 
కలర్స్ 
ఇంఛార్జి 
లక్ష్యం 
ల్స్ 
స్వీకరణ 
పరిషత్ 
బాబ్జి 
నాయుడు 
కట్ 
అవుట్ 
శుభాకాంక్షలు 
కాల్చి 
స్వీట్లు 
చెప్పారు 
ఫ్రెండ్స్ 
స్టోర్స్ 
త్ 
ఆర్థోపెడిక్ 
కృష్ణారావు 
కార్యాలయం 
రమేష్ రాజు 
అభివృద్ధి 
ఫ్లాష్ 
ఉపాధ్యాయులు 
 ఫిట్ నెస్"""

result_raw = """àµjêŸìu 
ú£«\\öËÀ 
ÚÛõôÂq 
ÏÙàÅ¦Jb 
õ¤ÛuÙ 
öËqÀ 
úˆyÚÛô¢é 
í£Jù£êÂ 
ò°Gb 
û¦óŸ³è[ª 
ÚÛæÀ 
Í÷±æÀ 
øŒ‰òÅ°Ú¥Ù¤Ûõª 
Ú¥La 
úˆyåªx 
àµð§pô¢ª 
všíÆÙèqÂ 
›ú¥dôÂq 
êÂ 
ÎôÂëÇÁšíè…ÚÂ 
ÚÛ”ú°gô¦÷± 
Ú¥ô¢uõóŸªÙ 
ô¢î¶ªù£ ô¦V 
ÍGÅ÷”CÌÄ 
ðÆ§xùÃ 
Ñð§ë¯uóŸ³õª 
 íÆ‡æÀ ûµúÃ"""

expected_raw = """àµjêŸìu
ú£«\\öËÀ 
ÚÛõôÂq
ÏÙàÅ¦Jb
õ¤ÛuÙ
öËÀq 
úˆyÚÛô¢é
í£Jù£êÂ
ò°Gb
û¦óŸ³è[ª
ÚÛæÀ
ÚÛæ®æÀ
øŒ‰òÅ°Ú¥Ù¤Ûõª
Ú¥La
úˆyåªx
àµð§pô¢ª
všíÆÙèÂq
þ¼dôÂq
êÂ
ÎôÁ–šíè…ÚÂ
ÚÛ”ÿ§gô¦÷±
Ú¥ô¦uõóŸªÙ
ô¢î¶ªùÃô¦V
ÍGÅ÷”CÌÄ
ð§xùÃ
Ñð§ëÅ¯uóŸ³õª
íÆ‡æÀûµúÃ"""

t_lines = [line.strip() for line in telugu_raw.strip().split('\n') if line.strip()]
r_lines = [line.strip() for line in result_raw.strip().split('\n') if line.strip()]
e_lines = [line.strip() for line in expected_raw.strip().split('\n') if line.strip()]

print(f"Telugu count: {len(t_lines)}")
print(f"Result count: {len(r_lines)}")
print(f"Expected count: {len(e_lines)}")

print("\n--- Detailed Comparison ---")
for i in range(max(len(t_lines), len(r_lines), len(e_lines))):
    t = t_lines[i] if i < len(t_lines) else "<NONE>"
    r = r_lines[i] if i < len(r_lines) else "<NONE>"
    e = e_lines[i] if i < len(e_lines) else "<NONE>"
    actual = translate_text(t) if t != "<NONE>" else "<NONE>"
    
    match_engine_exp = (actual == e)
    match_result_exp = (r == e)
    
    status = "OK" if match_engine_exp else "MISMATCH"
    print(f"[{i+1:02d}] Status: {status}")
    print(f"     Telugu:   {t}")
    print(f"     Engine:   {repr(actual)}")
    print(f"     Expected: {repr(e)}")
    print(f"     User Got: {repr(r)}")
