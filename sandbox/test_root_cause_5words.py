import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.stdout.reconfigure(encoding='utf-8')

import translation_mappings as tm
from translation_engine import translate_text

# Apply root-cause CONJUNCT_RULES fixes

# 1. ఎమ్మెల్సీ:
# మ్మె = మ + ె + మ vattu
tm.CONJUNCT_RULES[(tm.U_MA, tm.M_E, (tm.U_MA,))] = [238, 181, 170, 116]
# ల్సీ = ల + ీ + స vattu
tm.CONJUNCT_RULES[(tm.U_LA, tm.M_II, (tm.U_SA,))] = [77, 113]

# 2. ప్రశ్నలకు:
# శ్న = శ + న vattu
tm.CONJUNCT_RULES[(tm.U_SHA, None, (tm.U_NA,))] = [248, 140, 111]

# 3. స్పీకర్:
# స్పీ = స + ీ + ప vattu
tm.CONJUNCT_RULES[(tm.U_SA, tm.M_II, (tm.U_PA,))] = [250, 136, 121]

# 4. పక్షాలు:
# క్ష = 164, క్షా = 164, 165
tm.CONJUNCT_RULES[(tm.U_KA, None, (tm.U_SSA,))] = [164]
tm.CONJUNCT_RULES[(tm.U_KA, tm.M_AA, (tm.U_SSA,))] = [164, 165]
tm.CONJUNCT_RULES[(tm.U_KA, tm.M_U, (tm.U_SSA,))] = [164, 170]

# 5. ఘాటుగా:
# ఘా = 237, 198, 163, 171
tm.CONJUNCT_RULES[(tm.U_GHA, tm.M_AA, None)] = [237, 198, 163, 171]

words_5 = [
    ("ఎమ్మెల్సీ", "ÓîµªtMq"),
    ("ప్రశ్నలకు", "ví£øŒoõÚÛª"),
    ("స్పీకర్", "úˆyÚÛôÂ"),
    ("పక్షాలు", "í£¤¥õª"),
    ("ఘాటుగా", "íÆ£«åªÞ¥"),
]

print("Testing root-cause fixes for the 5 words:")
all_pass = True
for tw, exp in words_5:
    res = translate_text(tw, editorial_mode=False)
    ok = (res == exp)
    if not ok:
        all_pass = False
        print(f"FAIL: {tw}")
        print(f"  Got:      {repr(res)} (ords: {[ord(c) for c in res]})")
        print(f"  Expected: {repr(exp)} (ords: {[ord(c) for c in exp]})")
    else:
        print(f"PASS: {tw} -> {res}")

if all_pass:
    print("\nALL 5 WORDS PASSED VIA ROOT CAUSE CONJUNCT_RULES!")
