"""
Deep root-cause tracing for each specific failure.
"""
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.stdout.reconfigure(encoding='utf-8')
from translation_engine import translate_text, assemble_syllable
from linguistic_utils import segmentize
from translation_mappings import CONSONANTS, CONJUNCT_RULES, PHRASE_MAPPINGS, MATRAS, VOWELS
import translation_mappings as tm

# ===================================================================
# ISSUE 1: స్వ → expected 250+710, got 254+167
# 250 = ú, 710 = ˆ (swa ligature?)
# 254 = þ, 167 = § 
# ===================================================================
print("=== ISSUE 1: స్వ glyph ===")
# Check what CONSONANTS has for స (U_SA)
sa = tm.U_SA
print(f"  U_SA = {repr(sa)}")
if sa in CONSONANTS:
    cinfo = CONSONANTS[sa]
    print(f"  CONSONANTS[స]: {cinfo}")
print()

# Trace sa+halant+va syllable
sva_syls = segmentize('స్వ')
for s in sva_syls:
    print(f"  syl: {s}")
    b = assemble_syllable(s)
    print(f"  bytes: {b}")

# What do CONJUNCT_RULES have for (U_SA, None, (U_VA,))?
va = tm.U_VA
rule_key = (sa, None, (va,))
print(f"  CONJUNCT_RULES[(స,None,(వ,))]: {CONJUNCT_RULES.get(rule_key, 'NOT FOUND')}")
# Check with tuple variant
rule_key2 = (sa, None, tm.U_VA)
# check all sa keys
sa_keys = [k for k in CONJUNCT_RULES if k[0] == sa]
print(f"  All CONJUNCT_RULES with base=స: {sa_keys[:10]}")

# What about PRE_BASE_SUBS for sa?
print(f"  PRE_BASE_SUBS[స]: {tm.PRE_BASE_SUBS.get(sa, 'NOT FOUND')}")
print(f"  POST_BASE_SUBS[వ]: {tm.POST_BASE_SUBS.get(va, 'NOT FOUND')}")

print()

# ===================================================================
# ISSUE 2: కట్ → 229+195 (got) vs 230+192 (expected)
# Ta halant: expected 230 (æ), got 229 (å)
# Halant: expected 192 (Â), got 195 (Ã)  -- wait 194 vs 195?
# Actually expected = [218, 219, 230, 192], got = [218, 219, 229, 195]
# ===================================================================
print("=== ISSUE 2: కట్ ta halant ===")
ta = tm.U_TA
print(f"  U_TA = {repr(ta)}")
if ta in CONSONANTS:
    cinfo = CONSONANTS[ta]
    print(f"  CONSONANTS[ట]: {cinfo}")
print()

# Check CONJUNCT_RULES for (ta, None, None) — halant form
rule = CONJUNCT_RULES.get((ta, None, None), 'NOT FOUND')
print(f"  CONJUNCT_RULES[(ట,None,None)]: {rule}")

# Trace కట్
syls = segmentize('కట్')
for s in syls:
    print(f"  syl: {s}")
    b = assemble_syllable(s)
    print(f"  bytes: {b}")

# What's 229 vs 230?
# Check if POST_BASE_SUBS has ta
print(f"  POST_BASE_SUBS[ట]: {tm.POST_BASE_SUBS.get(ta, 'NOT FOUND')}")
print(f"  PRE_BASE_SUBS[ట]: {tm.PRE_BASE_SUBS.get(ta, 'NOT FOUND')}")

print()

# ===================================================================
# ISSUE 3: కాల్చి → ల్చి gives [245,135,97] expected [76,97]=[L,a]
# expected pos2=76 (L), got 245 (õ)
# ===================================================================
print("=== ISSUE 3: కాల్చి ===")
la = tm.U_LA
cha_raw = 'చ'  # cha consonant
print(f"  U_LA = {repr(la)}")
if la in CONSONANTS:
    print(f"  CONSONANTS[ల]: {CONSONANTS[la]}")
# Check POST_BASE_SUBS for la
print(f"  POST_BASE_SUBS[ల]: {tm.POST_BASE_SUBS.get(la, 'NOT FOUND')}")
# la before cha 
syls = segmentize('ల్చి')
for s in syls:
    print(f"  syl: {s}")
    b = assemble_syllable(s)
    print(f"  bytes: {b}")
# Lookup CONJUNCT_RULES for (cha, ii, (la,))
cha = 'చ'
print(f"  CONJUNCT_RULES[(చ,ి,(ల,))]: {CONJUNCT_RULES.get((cha, tm.M_I, (la,)), 'NOT FOUND')}")
print(f"  CONJUNCT_RULES[(చ,ి,ల)]: {CONJUNCT_RULES.get((cha, tm.M_I, la), 'NOT FOUND')}")
print()

# ===================================================================
# ISSUE 4: ఇంఛార్జి — ఛార్జి giving wrong bytes
# ఛా = [224, 197, 166] but expected bytes 2..6 = [224, 197, 166, 74, 98]
# ర్జి = [74, 160] but expected = [74, 98]
# ===================================================================
print("=== ISSUE 4: ఇంఛార్జి ===")
# Check ర్జి
syls = segmentize('ర్జి')
for s in syls:
    print(f"  syl: {s}")
    b = assemble_syllable(s)
    print(f"  bytes: {b}")
ja = tm.U_JA
print(f"  U_JA = {repr(ja)}")
print(f"  CONSONANTS[జ].head_i: {CONSONANTS.get(ja, {}).get('head_i')}")
print(f"  CONSONANTS[జ].head_ii: {CONSONANTS.get(ja, {}).get('head_ii')}")
ra = tm.U_RA
print(f"  PRE_BASE_SUBS[ర]: {tm.PRE_BASE_SUBS.get(ra, 'NOT FOUND')}")
print()

# ===================================================================
# ISSUE 5: రెడ్డి — last byte 34 vs 8220
# డ్డి gives [232, 147, 135]
# Expected: [232, 147, 135] -> but then last char should be 34 (") not 8220 (")
# Wait: Expected = [183, 244, 232, 8230, 34]
# Got     = [183, 244, 232, 8230, 8220]
# ===================================================================
print("=== ISSUE 5: రెడ్డి ===")
syls = segmentize('రెడ్డి')
for s in syls:
    b = assemble_syllable(s)
    print(f"  syl={s.get('raw','?')} bytes={b}")

dda = tm.U_DDA
print(f"  U_DDA = {repr(dda)}")
print(f"  CONSONANTS[డ]: {CONSONANTS.get(dda, {})}")
# Check డ్డి
syls2 = segmentize('డ్డి')
for s in syls2:
    b = assemble_syllable(s)
    print(f"  డ్డి syl={s.get('raw','?')} bytes={b}")

print()

# ===================================================================
# ISSUE 6: ఫ్లాష్ — missing 198 at pos 1
# Expected [240, 198, 167, 120, 249, 195]
# Our engine:  [237, 198, 167, 120, 249, 163]  — wait let me recheck
# ===================================================================
print("=== ISSUE 6: ఫ్లాష్ ===")
syls = segmentize('ఫ్లాష్')
for s in syls:
    b = assemble_syllable(s)
    print(f"  syl={s.get('raw','?')} base={s.get('base','?')} post_subs={s.get('post_subs',[])} bytes={b}")

pha = 'ఫ'
print(f"  CONSONANTS[ఫ]: {CONSONANTS.get(pha, {})}")
print(f"  POST_BASE_SUBS[ల]: {tm.POST_BASE_SUBS.get(la, 'NOT FOUND')}")
print(f"  CONJUNCT_RULES[(ఫ,ా,(ల,))]: {CONJUNCT_RULES.get((pha, tm.M_AA, (la,)), 'NOT FOUND')}")

print()

# ===================================================================
# ISSUE 7: చెప్పారు — expected 240 at pos 2, got 237
# 240=ð, 237=í
# Expected [224, 181, 240, 167, 112, 244, 162, 170]
# Got      [224, 181, 237, 167, 112, 244, 162, 170]
# చె = [224, 181], ప్పారు = [240, 167, 112, 244, 162, 170] expected but got 237...
# ===================================================================
print("=== ISSUE 7: చెప్పారు ===")
syls = segmentize('చెప్పారు')
for s in syls:
    b = assemble_syllable(s)
    print(f"  syl={s.get('raw','?')} base={s.get('base','?')} post_subs={s.get('post_subs',[])} matra={s.get('matra','?')} bytes={b}")
pa = tm.U_PA
print(f"  CONSONANTS[ప]: {CONSONANTS.get(pa, {})}")
print(f"  POST_BASE_SUBS[ప]: {tm.POST_BASE_SUBS.get(pa, 'NOT FOUND')}")
print(f"  CONJUNCT_RULES[(ప,ా,(ప,))]: {CONJUNCT_RULES.get((pa, tm.M_AA, (pa,)), 'NOT FOUND')}")

print()

# ===================================================================
# ISSUE 8: శుభాకాంక్షలు — missing 3 bytes (165, 217, 164)
# Expected: [248,338,8240,242,197,176,218,165,217,164,219,245,170]
# Got:      [248,338,8240,242,197,176,218,219,245,170]  <- missing 165(¥) 217(Ù) 164(¤) 
# Our result: Let's check
print("=== ISSUE 8: శుభాకాంక్షలు ===")
r = translate_text('శుభాకాంక్షలు')
b = [ord(c) for c in r]
print(f"  Our output bytes: {b}")
print(f"  Expected:         [248,338,8240,242,197,176,218,165,217,164,219,245,170]")
syls = segmentize('శుభాకాంక్షలు')
for s in syls:
    b2 = assemble_syllable(s)
    print(f"  syl={s.get('raw','?')} bytes={b2}")

print()

# ===================================================================
# ISSUE 9: లక్ష్యం — expected [245,164,219,117,217], got [245,203,182,194,243,376,170,217]
# ===================================================================
print("=== ISSUE 9: లక్ష్యం ===")
r = translate_text('లక్ష్యం')
b = [ord(c) for c in r]
print(f"  Our output bytes: {b}")
print(f"  Expected:         [245, 164, 219, 117, 217]")
# Check CONJUNCT_RULES for (ka, None, (sha, ya))
ka = tm.U_KA
sha = tm.U_SSA  # ష
ya = tm.U_YA
rule = CONJUNCT_RULES.get((ka, None, (sha, ya)), 'NOT FOUND')
print(f"  CONJUNCT_RULES[(క,None,(ష,య))]: {rule}")

# Trace syllables
syls = segmentize('క్ష్యం')
for s in syls:
    print(f"  syl: {s}")
    b2 = assemble_syllable(s)
    print(f"  bytes: {b2}")

# Check all CONJUNCT_RULES with ka as base that include sha
for k, v in CONJUNCT_RULES.items():
    if k[0] == ka and (sha in str(k) or 'ష' in str(k)):
        print(f"  CONJUNCT_RULES[{k}] = {v}")

print()

# ===================================================================
# ISSUE 10: బాబ్జి — expected [242,176,71,98], got [241,176,242,203,192,62]
# 242=ò (ba?), 241=ñ
# ===================================================================
print("=== ISSUE 10: బాబ్జి ===")
r = translate_text('బాబ్జి')
b = [ord(c) for c in r]
print(f"  Our output bytes: {b}")
print(f"  Expected:         [242, 176, 71, 98]")
ba = tm.U_BA
print(f"  U_BA = {repr(ba)}")
print(f"  CONSONANTS[బ]: {CONSONANTS.get(ba, {})}")
rule = CONJUNCT_RULES.get((ba, tm.M_AA, None), 'NOT FOUND')
print(f"  CONJUNCT_RULES[(బ,ా,None)]: {rule}")
syls = segmentize('బాబ్జి')
for s in syls:
    print(f"  syl: {s}")
    b2 = assemble_syllable(s)
    print(f"  bytes: {b2}")
