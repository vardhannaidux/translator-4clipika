"""
Investigate halant assembly and conjunct rules for failing words.
"""
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.stdout.reconfigure(encoding='utf-8')
import translation_mappings as tm
from translation_engine import assemble_syllable
from linguistic_utils import segmentize

ta = tm.U_TA
ka = tm.U_KA
la = tm.U_LA
sa = tm.U_SA
va = tm.U_VA
ba = tm.U_BA
ya = tm.U_YA
sha = tm.U_SSA
pha = 'ఫ'
pa = tm.U_PA

# --- ISSUE: కట్ halant ---
print("=== కట్ halant ===")
print("CONJUNCT_RULES[(ట,None,None)]:", tm.CONJUNCT_RULES.get((ta, None, None), 'NOT FOUND'))
ta_rules = [(k,v) for k,v in tm.CONJUNCT_RULES.items() if k[0] == ta]
print("All CONJUNCT_RULES with base=ట:", ta_rules[:10])
print("CONSONANTS[ట]:", tm.CONSONANTS.get(ta, {}))
# What bytes produce 230? 
# 230 = ord('æ') — check if it's a tail_halant anywhere
print("Consonants with tail_halant:", {c: cinfo.get('tail_halant') for c,cinfo in tm.CONSONANTS.items() if cinfo.get('tail_halant')})
print("Expected bytes for కట్: [218, 219, 230, 192]")
print("230=æ, 192=À — these must be ta vattu + halant_mark")
# CONSONANTS[ట].vattu = [104]=h. But expected 230...
# Wait — maybe the expected output uses a different rendering path
# Let's check ట్ in the INI file or REVERSE_MAP
# Actually 230 could be 'tail_halant' that needs to be added to CONSONANTS[ట]
print()

# --- ISSUE: లక్ష్యం segmentation ---
print("=== లక్ష్యం segmentation ===")
syls = segmentize('లక్ష్యం')
for s in syls:
    b = assemble_syllable(s)
    print(f"  syl={s.get('raw','?')} base={s.get('base','?')} subs={s.get('post_subs',[])} mods={s.get('post_mods',[])} bytes={b}")
# Issue: does segmentize correctly include both ష and య in post_subs?
# From earlier: post_subs=['ష', 'య'] — YES it does!
# But CONJUNCT_RULES[(క,None,(ష,య))] = [164, 219, 117] — should match!
# Let me check manually
k_test = (ka, None, (sha, ya))
print("Direct CONJUNCT_RULES lookup:", tm.CONJUNCT_RULES.get(k_test, 'NOT FOUND'))
print("ka =", repr(ka), "sha =", repr(sha), "ya =", repr(ya))
# Check if the syl post_subs uses the same unicode chars
for s in syls:
    if s.get('base') == ka:
        subs_tuple = tuple(s.get('post_subs', []))
        print("post_subs tuple:", repr(subs_tuple))
        key = (ka, None, subs_tuple)
        print("Lookup key:", repr(key))
        print("In CONJUNCT_RULES?", key in tm.CONJUNCT_RULES)
        print("Expected key:", repr(k_test))
        print("Keys match?", key == k_test)
print()

# --- ISSUE: స్వ glyph ---
print("=== స్వ glyph ===")
# Expected: 250+136+121, Got: 250+163+121
# 136 = matra_ii_post of స (head_ii+matra prefix)
# Actually 136 appears to be the Circumflex ˆ which is a special sa+va ligature mark
# Check if there's a CONJUNCT_RULE for (sa, None, (va,))
print("CONJUNCT_RULES[(స,None,(వ,))]:", tm.CONJUNCT_RULES.get((sa, None, (va,)), 'NOT FOUND'))
print("CONJUNCT_RULES[(స,None,వ)]:", tm.CONJUNCT_RULES.get((sa, None, va), 'NOT FOUND'))
# All sa rules:
sa_rules = [(k,v) for k,v in tm.CONJUNCT_RULES.items() if k[0] == sa]
print("All CONJUNCT_RULES with base=స:", sa_rules)
print()
# Need to add: (sa, None, (va,)) -> [250, 136, 121]  or similar
# Let's verify: 136 in CP1252 -> ˆ (circumflex)
# But in Unicode, 136 is a control char. The actual char stored in CONJUNCT output is byte value.
# assemble_syllable returns byte values that are then decoded as CP1252.

# --- ISSUE: బాబ్జి ---
print("=== బాబ్జి ===")
syls = segmentize('బాబ్జి')
for s in syls:
    b = assemble_syllable(s)
    print(f"  syl={s.get('raw','?')} bytes={b}")
print("CONJUNCT_RULES[(బ,ా,None)]:", tm.CONJUNCT_RULES.get((ba, tm.M_AA, None), 'NOT FOUND'))
ba_rules = [(k,v) for k,v in tm.CONJUNCT_RULES.items() if k[0] == ba]
print("All CONJUNCT_RULES with base=బ:", ba_rules[:10])
print("CONSONANTS[బ]:", tm.CONSONANTS.get(ba, {}))
print("Expected: [242, 176, 71, 98] = ò + ° + G + b")
# 242=ò is బా glyph, 176=° is aa matra
# 71=G, 98=b — బ్జి must give [71,98]
# 71='G', 98='b'
ja = tm.U_JA
print("CONJUNCT_RULES[(జ,ి,(బ,))]:", tm.CONJUNCT_RULES.get((ja, tm.M_I, (ba,)), 'NOT FOUND'))
# Actually బ్జి means ba is the vattu, ja is the base
# So the syl should be: base=జ, pre_subs=[బ], matra=ి
ja_rules = [(k,v) for k,v in tm.CONJUNCT_RULES.items() if k[0] == ja]
print("All CONJUNCT_RULES with base=జ:", ja_rules[:10])
print("CONSONANTS[జ]:", tm.CONSONANTS.get(ja, {}))
# Expected bytes for బ్జి part: [71, 98] — what's 71? 
# Wait — expected full: [242, 176, 71, 98]
# 242=ò = బా, 176=° = āa matra post, 71=G, 98=b
# So బా = [242, 176], and బ్జి = [71, 98]
# Or maybe బా = [242] + aa post [176], బ్జి = [71, 98]
# Let's check: CONJUNCT_RULES[(జ,ి,(బ,))]:
print()

# --- ISSUE: నాయుడు ya vattu ---
print("=== నాయుడు నా+యు+డు ===")
syls = segmentize('నాయుడు')
for s in syls:
    b = assemble_syllable(s)
    print(f"  syl={s.get('raw','?')} bytes={b}")
na = tm.U_NA
print("Expected: [251, 166, 243, 376, 179, 232, 91, 170]")
print("Our: [251, 166, 243, 376, 170, 232, 91, 170]")
# Diff at pos 4: expected=179 (³), got=170 (ª)
# 170=ª=M_U post, 179=³ 
# So యు is giving byte 170 but expected 179
# Let's check CONSONANTS[య]:
print("CONSONANTS[య]:", tm.CONSONANTS.get(ya, {}))
# Post for matra_u: 170 is standard M_U, but expected 179 (³)
# Need special ya+u matra handling?
print()

# --- ISSUE: ఫ్లాష్ ---
print("=== ఫ్లాష్ ===")
syls = segmentize('ఫ్లాష్')
for s in syls:
    b = assemble_syllable(s)
    print(f"  syl={s.get('raw','?')} base={s.get('base','?')} subs={s.get('post_subs',[])} matra={s.get('matra','?')} bytes={b}")
print("Expected: [240, 198, 167, 120, 249, 195]")
print("Our: ఫ్లా=[237,198,167,120] ష్=[249,163]")
# Issue 1: ఫ్లా gives [237,...] but expected starts with 240
# 237=í, 240=ð
# Issue 2: ష్ gives [249,163] but expected [249,195]
# The sha halant problem — 195=Ã (tail_halant of స), 163=£ (tail of ష)
print("CONSONANTS[ష]:", tm.CONSONANTS.get(sha, {}))
print("CONSONANTS[ఫ]:", tm.CONSONANTS.get(pha, {}))
# SHARED_VATTUS[ఫ] = [112]
print("SHARED_VATTUS[ఫ]:", tm.SHARED_VATTUS.get(pha, 'NOT FOUND'))
print("CONJUNCT_RULES[(ఫ,ా,(ల,))]:", tm.CONJUNCT_RULES.get((pha, tm.M_AA, (la,)), 'NOT FOUND'))
pha_rules = [(k,v) for k,v in tm.CONJUNCT_RULES.items() if k[0] == pha]
print("All CONJUNCT_RULES with base=ఫ:", pha_rules)
print()

# --- ISSUE: చెప్పారు pa+pa ---
print("=== చెప్పారు (ప్పా) ===")
syls = segmentize('చెప్పారు')
for s in syls:
    b = assemble_syllable(s)
    print(f"  syl={s.get('raw','?')} base={s.get('base','?')} subs={s.get('post_subs',[])} matra={s.get('matra','?')} bytes={b}")
print("Expected pos2=240 (ð) for ప్పా, got 237 (í)")
# 240=ð is the expected pa+pa+aa start 
# 237=í is what we got
pa_rules = [(k,v) for k,v in tm.CONJUNCT_RULES.items() if k[0] == pa]
print("All CONJUNCT_RULES with base=ప:", pa_rules[:10])
print("CONSONANTS[ప]:", tm.CONSONANTS.get(pa, {}))
print()

# --- ISSUE: రెడ్డి ---
print("=== రెడ్డి ===")
syls = segmentize('రెడ్డి')
for s in syls:
    b = assemble_syllable(s)
    print(f"  syl={s.get('raw','?')} bytes={b}")
print("Expected: [183, 244, 232, 8230, 34]")
print("Our: [183, 244, 232, 8230, 8220]")
# Diff at pos 4: expected=34 (quote), got=8220 (left double quote ")
# 34 is ASCII double quote, 8220 is Unicode left double quote "
# This is a mapping issue for డ్డి head_i
dda = tm.U_DDA
print("CONSONANTS[డ]:", tm.CONSONANTS.get(dda, {}))
print("CONJUNCT_RULES for డ with ి:", [(k,v) for k,v in tm.CONJUNCT_RULES.items() if k[0]==dda and k[1]==tm.M_I])
print()

# --- ISSUE: ఉద్దేశం ---
print("=== ఉద్దేశం ===")
syls = segmentize('ఉద్దేశం')
for s in syls:
    b = assemble_syllable(s)
    print(f"  syl={s.get('raw','?')} bytes={b}")
print("Expected: [105, 209, 235, 182, 204, 196, 248, 338, 217]")
print("Our: [209, 235, 195, 235, 182, 248, 338, 217]")
# Expected starts with 105 (i = 'i' letter) — ఉ vowel?
# Actually ఉ = independent vowel — VOWELS[ఉ]
print("VOWELS[ఉ]:", tm.VOWELS.get('ఉ', 'NOT FOUND'))
print()

# --- ISSUE: చైతన్య ---
print("=== చైతన్య ===")
syls = segmentize('చైతన్య')
for s in syls:
    b = assemble_syllable(s)
    print(f"  syl={s.get('raw','?')} bytes={b}")
print("Expected: [224, 181, 106, 234, 376, 236, 117]")
print("Our: [353, 224, 106, 234, 376, 236, 117]")
# pos0: expected=224(à), got=353(š)
# 353=š is CP1252 code 154
# 224=à is also CP1252... 224 = pre of చ (cha)?
# చైతన్య: చ+ై+త+న్+య
# Expected: pre_of_cha(224?) + ai_hook(181?) + 106(j) + ...
# Actually 353 (š) is CP1252 154 ≠ 224 (à)
ca = 'చ'
print("CONSONANTS[చ]:", tm.CONSONANTS.get(ca, {}))
print("CONJUNCT_RULES for చ+ై:", [(k,v) for k,v in tm.CONJUNCT_RULES.items() if k[0]==ca and k[1]==tm.M_AI])
print()

# --- ISSUE: స్కూల్ ---
print("=== స్కూల్ ===")
syls = segmentize('స్కూల్')
for s in syls:
    b = assemble_syllable(s)
    print(f"  syl={s.get('raw','?')} base={s.get('base','?')} subs={s.get('post_subs',[])} matra={s.get('matra','?')} bytes={b}")
print("Expected: [250, 163, 171, 92, 246, 203, 192]")
print("Our: [250, 163, 180, 101, 246, 203, 192]")
# pos2: expected=171(«), got=180(´)
# pos3: expected=92(\), got=101(e)
# 171 = M_UU alt_post, 92=\ backslash  
# 180 = M_UU post, 101=e
# స్కూ: should give [250,163,171,92] but gets [250,163,180,101]
# 250=head_sa, 163=tail_sa, then కూ vattu form
# The vattu of క is normally [218,219] pair
# But here as vattu it should give 171,92? 
# 171=alt_post of M_UU («), 92=\ backslash (vattu of క?)
# Let's check CONSONANTS[క] for vattu:
print("CONSONANTS[క]:", tm.CONSONANTS.get(ka, {}))
print("SHARED_VATTUS[క]:", tm.SHARED_VATTUS.get(ka, 'NOT FOUND'))
