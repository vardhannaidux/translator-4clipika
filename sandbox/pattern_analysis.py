"""
Targeted analysis of specific patterns to find root causes.
"""
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.stdout.reconfigure(encoding='utf-8')
from translation_engine import translate_text, assemble_syllable
from linguistic_utils import segmentize
from translation_mappings import CONSONANTS, CONJUNCT_RULES, PHRASE_MAPPINGS

# ─────────────────────────────────────────────────────────────────────────────
# GROUP 1: స్ (sa + halant) head glyph issue — 'స్వ' variants
# Expected 250 (ú), Got 254 (þ) at start
# స్వీకరణ and స్వీట్లు both have this same diff at pos0,1
# Expected: 250 (ú), 710 (ˆ)   Got: 254 (þ), 167 (§)
print("=== GROUP 1: స్వ start glyph (250+710 vs 254+167) ===")
for w in ['స్వీకరణ', 'స్వీట్లు', 'స్వాగతం']:
    r = translate_text(w)
    b = [ord(c) for c in r]
    print(f"  {w}: {b[:3]}")

# ─────────────────────────────────────────────────────────────────────────────
# GROUP 2: కట్ and కటౌట్ — ta vattu glyph
# Expected 230 (æ), Got 229 (å) for కట్ at pos 2
# కట్ expected: [218, 219, 230, 192], got: [218, 219, 229, 195]
print()
print("=== GROUP 2: కట్ ta halant glyph (230 vs 229) ===")
for w in ['కట్', 'కటౌట్', 'కట్టు']:
    r = translate_text(w)
    b = [ord(c) for c in r]
    print(f"  {w}: {b}")

# ─────────────────────────────────────────────────────────────────────────────
# GROUP 3: పరిషత్ halant 194 vs 195
# Expected pos6=194 (Â), Got pos6=195 (Ã)
print()
print("=== GROUP 3: హల్ గుర్తు 194 (Â) vs 195 (Ã) ===")
for w in ['పరిషత్', 'కట్', 'కటౌట్']:
    r = translate_text(w)
    b = [ord(c) for c in r]
    print(f"  {w}: last bytes = {b[-3:]}")

# ─────────────────────────────────────────────────────────────────────────────
# GROUP 4: కలర్స్ byte order swap — 194 and 113 swapped
# Expected: [218, 219, 245, 244, 194, 113]
# Got:      [218, 219, 245, 244, 113, 194]
print()
print("=== GROUP 4: కలర్స్ order issue ===")
syls = segmentize('కలర్స్')
for s in syls:
    b = assemble_syllable(s)
    print(f"  syllable={s.get('raw','?')}: bytes={b}")

# ─────────────────────────────────────────────────────────────────────────────
# GROUP 5: ఇంఛార్జి — huge difference (4 bytes vs 7)
# Expected: [207, 217, 224, 197, 166, 74, 98], Got: [207, 217, 77, 113]
print()
print("=== GROUP 5: ఇంఛార్జి (cha+reph+ji) ===")
syls = segmentize('ఇంఛార్జి')
for s in syls:
    b = assemble_syllable(s)
    print(f"  syllable={s.get('raw','?')} type={list(s.keys())}: bytes={b}")

# ─────────────────────────────────────────────────────────────────────────────
# GROUP 6: లక్ష్యం — huge difference
# Expected: [245, 164, 219, 117, 217], Got: [245, 203, 182, 194, 243, 376, 170, 217]
print()
print("=== GROUP 6: లక్ష్యం ===")
syls = segmentize('లక్ష్యం')
for s in syls:
    b = assemble_syllable(s)
    print(f"  syllable={s.get('raw','?')} base={s.get('base','?')} matra={s.get('matra','?')} post_subs={s.get('post_subs',[])} post_mods={s.get('post_mods',[])} : bytes={b}")

# ─────────────────────────────────────────────────────────────────────────────
# GROUP 7: రెడ్డి — " vs " (34 vs 8220)
print()
print("=== GROUP 7: రెడ్డి ===")
syls = segmentize('రెడ్డి')
for s in syls:
    b = assemble_syllable(s)
    print(f"  syllable={s.get('raw','?')}: bytes={b}")

# ─────────────────────────────────────────────────────────────────────────────
# GROUP 8: ఫ్లాష్ — missing byte 198 (Æ) at pos 1
# Expected: [240, 198, 167, 120, 249, 195]
# Got:      [240, 167, 120, 249, 195]
print()
print("=== GROUP 8: ఫ్లాష్ ===")
syls = segmentize('ఫ్లాష్')
for s in syls:
    b = assemble_syllable(s)
    print(f"  syllable={s.get('raw','?')} base={s.get('base','?')} post_subs={s.get('post_subs',[])} matra={s.get('matra','?')}: bytes={b}")

# ─────────────────────────────────────────────────────────────────────────────
# GROUP 9: కాల్చి — 76 (L) expected at pos 2, got 245
# Expected: [218, 165, 76, 97]    = కా + ల్ + చి
print()
print("=== GROUP 9: కాల్చి ===")
syls = segmentize('కాల్చి')
for s in syls:
    b = assemble_syllable(s)
    print(f"  syllable={s.get('raw','?')}: bytes={b}")

# ─────────────────────────────────────────────────────────────────────────────
# GROUP 10: శుభాకాంక్షలు — missing bytes 165, 217, 164
# Expected: [248,338,8240,242,197,176,218,165,217,164,219,245,170]
# Got:      [248,338,8240,242,197,176,218,219,245,170]
print()
print("=== GROUP 10: శుభాకాంక్షలు ===")
syls = segmentize('శుభాకాంక్షలు')
for s in syls:
    b = assemble_syllable(s)
    print(f"  syllable={s.get('raw','?')}: bytes={b}")

print()
print("=== PHRASE_MAPPINGS coverage ===")
check_words = ['కాల్చి', 'ఇంఛార్జి', 'శుభాకాంక్షలు', 'కట్', 'కటౌట్']
for w in check_words:
    matched = [k for k in PHRASE_MAPPINGS if w.startswith(k) or k.startswith(w[:3])]
    print(f"  {w}: PHRASE matches => {matched[:5]}")
