import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.stdout.reconfigure(encoding='utf-8')

from translation_engine import translate_text

words_5 = [
    ("ఎమ్మెల్సీ", "ÓîµªtMq"),
    ("ప్రశ్నలకు", "ví£øŒoõÚÛª"),
    ("స్పీకర్", "úˆyÚÛôÂ"),
    ("పక్షాలు", "í£¤¥õª"),
    ("ఘాటుగా", "íÆ£«åªÞ¥"),
]

print("Testing all 5 words against codebase directly:")
all_pass = True
for tw, exp in words_5:
    res = translate_text(tw, editorial_mode=False)
    ok = (res == exp)
    if not ok:
        all_pass = False
        print(f"FAIL: {tw}")
        print(f"  Got:      {repr(res)}")
        print(f"  Expected: {repr(exp)}")
    else:
        print(f"PASS: {tw} -> {res}")

if all_pass:
    print("\nALL 5 WORDS PASSED 100%!")
