import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.stdout.reconfigure(encoding='utf-8')

from translation_engine import translate_text

test_conjunct_words = [
    ("లక్ష్యం", "õ¤ÛuÙ"),
    ("పక్షాలు", "í£¤¥õª"),
    ("స్వచ్ఛమైన", "ú£yàµaîµªjûÂ"),
    ("స్వాగతం", "ú£yÞœêŸÙ"),
    ("శ్రామిక", "vø‹vNªÚÛ"),
    ("కార్యక్రమంలో", "Ú¥ô¢uvÚÛ÷ªÙöËº"),
    ("ప్రశ్నలకు", "ví£øŒoõÚÛª"),
    ("కృత్రిమ", "ÚÛ”vA÷ª"),
    ("ప్రారంభించి", "vð§ô¢ÙGÅÙ#"),
]

print("Verifying conjunct test words:")
all_ok = True
for tw, exp in test_conjunct_words:
    res = translate_text(tw)
    match = (res == exp)
    if not match:
        all_ok = False
        print(f"FAIL: {tw} -> Got {repr(res)}, Expected {repr(exp)}")
    else:
        print(f"PASS: {tw} -> {res}")

if all_ok:
    print("\nALL SPECIFIED CONJUNCTS & TEST WORDS PASSED SUCCESSFULLY!")
