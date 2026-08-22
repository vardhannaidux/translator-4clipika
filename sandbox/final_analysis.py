"""
Final root cause confirmation - verifying each issue with expected values.
"""
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.stdout.reconfigure(encoding='utf-8')
import translation_mappings as tm
from translation_engine import assemble_syllable, translate_text
from linguistic_utils import segmentize

ka = tm.U_KA; ta = tm.U_TA; la = tm.U_LA; sa = tm.U_SA; va = tm.U_VA
ba = tm.U_BA; ya = tm.U_YA; sha = tm.U_SSA; pa = tm.U_PA; na = tm.U_NA
da = tm.U_DA; ja = tm.U_JA; dda = tm.U_DDA; ra = tm.U_RA; pha = 'ఫ'
ca = 'చ'; ma = tm.U_MA; lla = tm.U_LLA

print("=" * 70)
print("CONFIRMED ROOT CAUSE SUMMARY")
print("=" * 70)

# 1. కట్ / కటౌట్ — ట with halant
# Expected: ట+halant = [230, 192]   Got: [229, 195]
# CONSONANTS[ట] has no 'tail_halant', no special halant entry
# Looking at halant consonants: స has tail_halant=195, బ has tail_halant=192, ల has tail_halant=192
# కట్ expected ends with [230, 192] — 230 should be ట tail_halant, 192 = halant marker
# FIX: Add CONSONANTS[ట]['tail_halant'] = 230  (and use halant marker from బ/ల = 192)
print()
print("1. కట్ — ట tail_halant missing")
print("   Current CONSONANTS[ట]:", tm.CONSONANTS.get(ta, {}))
print("   Expected [230, 192] = tail_halant(230) + halant_mark(192)")
print("   FIX: CONSONANTS[ట]['tail_halant'] = 230")
print("   Compare: బ.tail_halant=192, ల.tail_halant=192, స.tail_halant=195")
# But wait - also need to check what generates 195 for our current output
# Our output [229,195]: 229 comes from head=234? No... let me check
# Actually with halant=True and no 'tail_halant': the engine uses cinfo['head'] = 234? No, 229 != 234
# Let me trace the engine's halant path:

# 2. స్వ — sa+va vattu
# Expected [250, 136, 121]   Got [250, 163, 121]
# 250=sa head, 163=sa tail, 121=va vattu
# 136 = sa's matra_ii_post (ˆ circumflex)
# This is a special ligature: sa + va vattu needs sa-'no-tail' form + circumflex + va
# FIX: Add CONJUNCT_RULES entry: (sa, None, (va,)) -> [250, 136, 121]
# Check existing similar: (స,ీ,(ర,త)) = [118,250,136,104] — 136 appears here too! 
# So 136 = sa special mark (like sa+II form without tail)
print()
print("2. స్వ — missing CONJUNCT_RULE for (స, None, (వ,))")
print("   Expected: [250, 136, 121]")  
print("   FIX: CONJUNCT_RULES[(స, None, (వ,))] = [250, 136, 121]")
# Verify: does స్వాగతం work with this?
# స్వ + ా + గ + తం
# [250,136,121] + [165] + [222,156] + [234,159] + [217] = స్వాగతం
# Let's also check స్వీకరణ
# Expected: [250, 710, 121, ...] -- 710=ˆ which is ord 710 in Python but byte 136 in CP1252
# So it's the same: 136 CP1252 = ˆ Unicode 710
# (sa, M_II, (va,)): need [250, 136, 121] too? No wait —
# స్వీ: expected starts 250+710+121 
# 710 is still ˆ = CP1252 byte 136 = same byte!
# So for both స్వ (no matra) and స్వీ (M_II matra), the first part is [250, 136, 121]
# Then the matra_ii_post 136 already handles the II after sa, so for M_II+va vattu: [250, 136, 121, 136?] ... no
# Let's check: expected for స్వీకరణ = [250, 710, 121, 218, 219, 244, 162, 233]
# 250+710+121 = [250, 136, 121] = sa ligature + va vattu
# then కరణ starts with [218, 219, ...]
# So the II matra on స్వీ — does it add another post byte?
# Actually from CONSONANTS[స]: head_ii=250, matra_ii_post=136
# So II form of sa: head(250) + matra_ii_post(136) = [250, 136]
# Then va vattu = [121]
# So (sa, M_II, (va,)) -> [250, 136, 121] same as (sa, None, (va,))!
# Makes sense: the sa-special-ligature looks same for II-matra vs no-matra when va follows
# FIX: Both (sa, None, (va,)) and (sa, M_II, (va,)) = [250, 136, 121]

# 3. నాయుడు — యు bytes
# CONSONANTS[య]: tail=159, tail2=170, u_no_tail2=True, matra_i_post=179
# Expected [243, 376, 179] for యు  (376 = ˆˆ in CP1252? no...)
# Wait: expected bytes for నాయుడు = [251, 166, 243, 376, 179, 232, 91, 170]
# 376 = ˆ (CP1252 136) -- again the ˆ character!
# Actually 376 = Unicode 0x178 = Ÿ — but CP1252 byte 159 = Ÿ
# 376 = Unicode Ÿ? Let's check: ord('Ÿ') = 376? No: ord('Ÿ') = 159 + ... 
# Actually in Python, 376 means it's stored as the Unicode codepoint 376
# But when encoded to CP1252, 376=Ÿ maps to byte 159
# So 376 = Unicode Ÿ (Latin Capital Letter Y with Diaeresis) = CP1252 byte 159
# So [243, 376, 179] in Unicode = bytes [243, 159, 179] in CP1252
# But we're getting [243, 376, 170] = [243, 159, 170]
# CONSONANTS[య]: tail=159, tail2=170, u_no_tail2=True, matra_i_post=179
# For M_U matra: standard is M_U post = 170, but expected 179
# 179 = matra_i_post of య!
# So for M_U matra on య, the post should be matra_i_post (179) not M_U post (170)
# But why? matra_i_post is normally for M_I...
# Actually: looking at CONSONANTS[య]:
# u_no_tail2=True means when u matra applied, don't add tail2
# matra_i_post=179 — this is a special marker that applies in certain contexts
# The u matra on ya usually produces: head(243) + tail(159) + u_post(170)
# But expected: 243 + 159 + 179
# 179 = matra_i_post for ya. Maybe for ya+u it should use matra_i_post?
print()
print("3. నాయుడు — యు: expected [243, 159(Ÿ), 179] got [243, 159(Ÿ), 170]")
print("   CONSONANTS[య].matra_i_post =", tm.CONSONANTS.get(ya, {}).get('matra_i_post'))
print("   Standard M_U post = 170, but expected 179")
print("   FIX: Need special ya+u handling or matra_u_post for ya")

# 4. ష్ halant  
# Expected [249, 195] for ష్, got [249, 163]
# CONSONANTS[ష]: head=250, tail=163, vattu=None
# 249 = ? ... head of ష is 250, not 249. So 249 is special...
# Actually let me check CONJUNCT_RULES or SPECIAL form for ష with halant
print()
print("4. ష halant")
sha_rules = [(k,v) for k,v in tm.CONJUNCT_RULES.items() if k[0] == sha]
print("   CONJUNCT_RULES with ష base:", sha_rules[:5])
# Check tail_halant of ష
print("   CONSONANTS[ష].tail_halant:", tm.CONSONANTS.get(sha, {}).get('tail_halant'))
# Expected: [249, 195] — 249=ù, 195=Ã
# 195 appears as tail_halant of స!  
# 249 could be a special halant glyph for ష
# FIX: Add tail_halant for ష = 195 (or change halant rendering)
# But wait our output gives [249, 163] where 249 is already correct head
# and 163 = tail of ష... so the halant marker is wrong (163=tail vs 195=halant marker)

# 5. చైతన్య — CONJUNCT_RULES[(చ,ై,None)] = [154, 224, 106]
# 154 = š (CP1252) = Unicode 353
# Expected [224, 181, 106]
# 224=cha pre, 181=e_post, 106=ai_hook
# So the ai matra on cha should produce: pre-hook(224) + ai_hook(181+106) not via CONJUNCT_RULE?
# Actually for ై on చ: pre=183 (M_E pre), post=106 (M_AI post)
# But expected is 224+181+106... 
# 224 = CONSONANTS[చ].head, 181 = e_post of చ... 
# So: head(224) + e_post(181) + ai_post_hook(106) = [224, 181, 106]
# But CONJUNCT_RULES has [154, 224, 106] which gives wrong result!
# FIX: Fix CONJUNCT_RULES[(చ,ై,None)] = [224, 181, 106]
print()
print("5. చైతన్య — CONJUNCT_RULES[(చ,ై,None)] wrong")
print("   Current:", tm.CONJUNCT_RULES.get((ca, tm.M_AI, None), 'NOT FOUND'))
print("   Expected: [224, 181, 106]")
print("   FIX: CONJUNCT_RULES[(చ, M_AI, None)] = [224, 181, 106]")

# 6. బాబ్జి — బా gives [241, 176] expected [242, 176]  
# CONSONANTS[బ]: head=241, head_halant=[242,203], tail_halant=192
# So ba head = 241, but when ba has aa matra: expected 242+176
# 242 = ba special aa head? head_halant=[242,203]... no
# But CONJUNCT_RULES[(బ,ి,None)] = [71] — this is head_i!
# For M_AA on బ: no CONJUNCT_RULE exists
# So engine uses: head(241) + aa_post(176) = [241, 176] but expected [242, 176]
# 242 = ò vs 241 = ñ 
# Looking at CONJUNCT_RULES for బ: (బ,ా,య) = [242, 176, 117] — 242 appears here!
# So when ba has aa matra, some cases use 242 as the head
# Maybe: CONSONANTS[బ] needs head_aa=242?
print()
print("6. బాబ్జి — బా head byte")
print("   head(241) + aa_post(176) = [241,176] but expected [242,176]")
print("   FIX: CONSONANTS[బ]['head_aa'] = 242  or add CONJUNCT_RULE [(బ,ా,None)]=[242,176]")

# 7. ఉద్దేశం — ద్దే segmentation  
# Got: ఉ=[209], ద్దే=[184,235,204], శం=[248,140,217]
# Expected: [105, 209, 235, 182, 204, 196, 248, 338, 217]
# 105=i, 209=U, 235=u, 182=dha_body?, 204=cha_form?, ...
# This is a very complex case. Let me check segmentation.
print()
print("7. ఉద్దేశం analysis")
syls = segmentize('ఉద్దేశం')
for s in syls:
    b = assemble_syllable(s)
    print(f"  {s.get('raw','?')}: {b}")
# Expected [105, 209, 235, 182, 204, 196, 248, 338, 217]
# Word breakdown: ఉ+ద్+దే+శం (?)  or ఉ+ద్+దే+శ+ం?
# 105=i (ASCII), 209=ఉ, 235=U(da), 182=head_ee_post?, 204=Ì, 196=Ä, 248=శ, 338=ˆˆ, 217=anusvara
# Let's check CONSONANTS[ద]:
da_info = tm.CONSONANTS.get(da, {})
print(f"  CONSONANTS[ద]: {da_info}")

# 8. కాల్చి — ల్చి
# Got [245, 135, 97]  expected [76, 97]
# 245=ల head, 135=matra_i_post?, 97=a(ascii)
# 76=L, 97=a 
# కాల్చి = కా+ల్చి, where ల్చి is la+halant+cha+i_matra
# Expected: ల్చి = [76, 97] — just 2 bytes! 76=L, 97=a
# This must be a CONJUNCT_RULE for (చ, M_I, (ల,)) = [76, 97]?
# or a direct vattu form for la?
print()
print("8. కాల్చి — ల్చి")
syls = segmentize('ల్చి')
for s in syls:
    b = assemble_syllable(s)
    print(f"  {s.get('raw','?')} base={s.get('base','?')} subs={s.get('post_subs',[])} matra={s.get('matra','?')}: bytes={b}")
# expected [76, 97] = 'L' + 'a'
# 'L' = ASCII 76, 'a' = ASCII 97
# So ల్చి maps to 'La' as ASCII!
# This must be a specific glyph combination in 4C Lipika font
print(f"  Expected bytes [76, 97] = ['L', 'a']")
print(f"  FIX: Add CONJUNCT_RULES[(చ, M_I, (ల,))] = [76, 97]")
# Or maybe it's rendered as a precomposed ligature?
print()

# 9. చెప్పారు — ప్పా: expected first byte 240 (head_aa?) got 237 (head?)
# Our output: ప్పా=[240, 167, 112] — wait this IS correct already!
# Expected pos2=240, got=237 — BUT wait the output from investigate2 shows bytes=[240, 167, 112]!
# Let me re-run this:
r = translate_text('చెప్పారు')
b = [ord(c) for c in r]
print("9. చెప్పారు actual output bytes:", b)
print("   Expected:", [224, 181, 240, 167, 112, 244, 162, 170])
# Hmm our output for ప్పా WAS [240, 167, 112] from segmentize test
# But the full word output differs at pos 2...
# Let me check: segmentize gives ప్పా bytes [240, 167, 112]
# But in the full translate_text the result is different?
# Possible: PHRASE_MAPPINGS or other override affects it

# 10. కలర్స్ byte order
print()
print("10. కలర్స్ byte order")
syls = segmentize('కలర్స్')
for s in syls:
    b = assemble_syllable(s)
    print(f"  {s.get('raw','?')} base={s.get('base','?')} subs={s.get('post_subs',[])} matra={s.get('matra','?')}: bytes={b}")
# ర్స్: expected [244, 194, 113] vs got [244, 113, 194]  
# 244=ra head, 194=ta-halant?, 113=sa vattu
# Actually: ర్స్ = ra + halant + sa + halant
# Expected: ra_head(244) + halant_mark(194) + sa_vattu(113)
# Got: ra_head(244) + sa_vattu(113) + halant_mark(194) — WRONG ORDER!
# FIX: In ర్స్ rendering, halant comes before vattu

# 11. లక్ష్యం re-check  
r = translate_text('లక్ష్యం')
b = [ord(c) for c in r]
print()
print("11. లక్ష్యం actual output:", b)
print("    Expected:            [245, 164, 219, 117, 217]")
# From earlier: got [245, 203, 182, 194, 243, 376, 170, 217] — 8 bytes vs 5 expected
# But from assemble test: [245] + [164, 219, 117, 217] = [245, 164, 219, 117, 217] = CORRECT!
# So why does translate_text give wrong output? Must be PHRASE_MAPPINGS interference

print()
print("12. Phrase mapping interference check")
for w in ['లక్ష్యం', 'చెప్పారు', 'స్వాగతం']:
    for k, v in tm.PHRASE_MAPPINGS.items():
        if w.startswith(k) or k in w:
            print(f"  {w} matches PHRASE[{k!r}]")
