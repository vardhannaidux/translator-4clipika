import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.stdout.reconfigure(encoding='utf-8')

import translation_mappings as tm
from translation_engine import translate_text, render

words_5 = [
    ("ఎమ్మెల్సీ", "ÓîµªöËÀúˆ", "ÓîµªtMq"),
    ("ప్రశ్నలకు", "ví£ù£oõÚÛª", "ví£øŒoõÚÛª"),
    ("స్పీకర్", "úpÚÛôÂ", "úˆyÚÛôÂ"),
    ("పక్షాలు", "í£Ú¥qõª", "í£¤¥õª"),
    ("ఘాటుగా", "ß°åªÞ¥", "íÆ£«åªÞ¥"),
]

for tw, got, exp in words_5:
    res = translate_text(tw, editorial_mode=False)
    print("=" * 60)
    print(f"Telugu Word: {tw}")
    print(f"  Got (Engine): {repr(res)}")
    print(f"  Got (User):   {repr(got)}")
    print(f"  Expected:     {repr(exp)}")
    
    # Trace codepoints of expected vs got
    print("  Exp ords: ", [ord(c) for c in exp])
    print("  Got ords: ", [ord(c) for c in res])
