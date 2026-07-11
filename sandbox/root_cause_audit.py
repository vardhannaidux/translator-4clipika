"""
Root cause analyzer — tests every identified bug systematically.
"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import translation_mappings

def safe(s):
    if isinstance(s, (list, set)):
        return str(s)
    return str(s).encode("ascii", errors="backslashreplace").decode("ascii")

# ─────────────────────────────────────────────────────────────
# BUG 1: Duplicate keys in PHRASE_MAPPINGS
# ─────────────────────────────────────────────────────────────
print("=== BUG 1: DUPLICATE KEYS IN PHRASE_MAPPINGS ===")
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "translation_mappings.py"))
with open(src_path, "r", encoding="utf-8") as f:
    src = f.read()

phrase_start = src.find("PHRASE_MAPPINGS = {")
phrase_end = src.find("\n}", phrase_start) + 2
phrase_section = src[phrase_start:phrase_end]

import re
key_pattern = re.compile(r'^\s*"([^"]+)"\s*:', re.MULTILINE)
found_keys = key_pattern.findall(phrase_section)

key_counts = {}
for k in found_keys:
    key_counts[k] = key_counts.get(k, 0) + 1

dup_keys = {k: v for k, v in key_counts.items() if v > 1}
if dup_keys:
    print(f"  FOUND {len(dup_keys)} duplicate keys:")
    for k, cnt in dup_keys.items():
        print(f"    [{cnt}x] {safe(k)}")
else:
    print("  No duplicate keys found.")

print()

# ─────────────────────────────────────────────────────────────
# BUG 2: GLOBAL MUTABLE STATE MUTATIONS
# ─────────────────────────────────────────────────────────────
print("=== BUG 2: GLOBAL MUTABLE STATE MUTATIONS ===")
from translation_engine import translate_text
import copy

conjunct_before = dict(translation_mappings.CONJUNCT_RULES)
consonants_before = {k: dict(v) for k, v in translation_mappings.CONSONANTS.items()}
fvbp = translation_mappings.FORCE_VATTU_BEFORE_POST
force_vattu_before = set(fvbp) if isinstance(fvbp, (set, frozenset)) else dict(fvbp)

translate_text("కూ")

conjunct_after = dict(translation_mappings.CONJUNCT_RULES)
consonants_after = dict(translation_mappings.CONSONANTS)
fvbp2 = translation_mappings.FORCE_VATTU_BEFORE_POST
force_vattu_after = set(fvbp2) if isinstance(fvbp2, (set, frozenset)) else dict(fvbp2)

conjunct_mutations = {}
for k in conjunct_after:
    if k not in conjunct_before:
        conjunct_mutations[k] = ('NEW', conjunct_after[k])
    elif conjunct_before[k] != conjunct_after[k]:
        conjunct_mutations[k] = (conjunct_before[k], conjunct_after[k])

consonant_mutations = []
for k in consonants_after:
    if k in consonants_before:
        for field in consonants_after[k]:
            if field not in consonants_before[k] or consonants_before[k][field] != consonants_after[k][field]:
                consonant_mutations.append((safe(k), field, consonants_before[k].get(field), consonants_after[k][field]))

print(f"  CONJUNCT_RULES mutations after translate_text: {len(conjunct_mutations)}")
for k, (old, new) in conjunct_mutations.items():
    ks = tuple(safe(c) if c else 'None' for c in k)
    print(f"    {ks}: {old} -> {new}")

print(f"  CONSONANTS mutations after translate_text: {len(consonant_mutations)}")
for cchar, field, old_val, new_val in consonant_mutations:
    print(f"    {safe(cchar)} [{field}]: {old_val} -> {new_val}")

if isinstance(force_vattu_after, set) and isinstance(force_vattu_before, set):
    new_fvbp = force_vattu_after - force_vattu_before
    print(f"  FORCE_VATTU_BEFORE_POST new entries: {len(new_fvbp)}")
    for entry in new_fvbp:
        print(f"    {entry}")

print()

# ─────────────────────────────────────────────────────────────
# BUG 3: normalize_telugu_input CORRUPTION TEST
# ─────────────────────────────────────────────────────────────
print("=== BUG 3: normalize_telugu_input CORRUPTION TEST ===")
from translation_engine import normalize_telugu_input

test_inputs = [
    "కార్యక్రమం",
    "నిర్వహించారు",
    "ప్రత్యేక",
    "నిర్విగ్నంగా",
    "స్వాగతం",
    "వేగుళ్ల",
]
for inp in test_inputs:
    out = normalize_telugu_input(inp)
    if inp != out:
        print(f"  CORRUPTION: {safe(inp)!r} -> {safe(out)!r}")
        diff_idx = next((i for i, (a, b) in enumerate(zip(inp, out)) if a != b), len(inp))
        if diff_idx < len(inp):
            print(f"    First diff at pos {diff_idx}: {safe(inp[diff_idx])} vs {safe(out[diff_idx])}")
    else:
        print(f"  OK: {safe(inp)!r} unchanged")

print()

# ─────────────────────────────────────────────────────────────
# BUG 4: IS_SEVEN_PARAGRAPH global flag leak
# ─────────────────────────────────────────────────────────────
print("=== BUG 4: IS_SEVEN_PARAGRAPH GLOBAL STATE LEAK ===")
import translation_engine

translate_text("కరోనా పరిరక్షణ", editorial_mode=True)
flag_after_editorial = translation_engine.IS_SEVEN_PARAGRAPH
print(f"  IS_SEVEN_PARAGRAPH after editorial+keyword call: {flag_after_editorial}")

translate_text("కార్యక్రమం")
flag_after_normal = translation_engine.IS_SEVEN_PARAGRAPH
print(f"  IS_SEVEN_PARAGRAPH after normal call: {flag_after_normal}")

print()

# ─────────────────────────────────────────────────────────────
# BUG 5: homework mode permanently deletes CONJUNCT_RULES
# ─────────────────────────────────────────────────────────────
print("=== BUG 5: homework mode permanently DELETES CONJUNCT_RULES ===")
from translation_mappings import U_KA, U_DHA, U_SA, M_OO, M_AA, M_O, M_AU
target_keys = [
    (U_KA, M_OO, None),
    (U_DHA, M_AA, None),
    (U_SA, M_OO, None),
    (U_SA, M_O, None),
    (U_SA, M_AU, None),
]

print("  Before homework call:")
for k in target_keys:
    present = k in translation_mappings.CONJUNCT_RULES
    chars = [safe(c) for c in k if c is not None]
    print(f"    {chars}: {'EXISTS' if present else 'ABSENT'}")

# simulate homework mode call by forcing keyword
translate_text("హోం కార్యక్రమం")

print("  After homework call:")
for k in target_keys:
    present = k in translation_mappings.CONJUNCT_RULES
    chars = [safe(c) for c in k if c is not None]
    print(f"    {chars}: {'EXISTS' if present else 'DELETED!'}")

# Now call normally
translate_text("కూ")
print("  After normal call (should they be restored?):")
for k in target_keys:
    present = k in translation_mappings.CONJUNCT_RULES
    chars = [safe(c) for c in k if c is not None]
    print(f"    {chars}: {'EXISTS' if present else 'STILL DELETED!'}")

print()

# ─────────────────────────────────────────────────────────────
# BUG 6: Verify that same input always gives same output
# ─────────────────────────────────────────────────────────────
print("=== BUG 6: DETERMINISM CHECK AFTER MIXED CALLS ===")
# do some homework and editorial calls first to pollute state
for _ in range(3):
    translate_text("హోం కార్యక్రమం")  # homework
    translate_text("కరోనా పరిరక్షణ", editorial_mode=True)  # editorial + seven-paragraph

test_para = "వేగుళ్ల స్వాగతం కార్యక్రమం నిర్విగ్నంగా ప్రత్యేక ప్రార్థనలు"
baseline = translate_text(test_para)
mismatches = 0
for i in range(20):
    translate_text("హోం కార్యక్రమం")  # inject homework mode
    translate_text("కరోనా పరిరక్షణ", editorial_mode=True)
    result = translate_text(test_para)
    if result != baseline:
        mismatches += 1
        print(f"  MISMATCH at run {i+1}!")
        print(f"    Expected: {safe(baseline[:60])}")
        print(f"    Got:      {safe(result[:60])}")

if mismatches == 0:
    print("  PASS: All 20 runs after state pollution gave same output.")
else:
    print(f"  FAIL: {mismatches}/20 runs gave different output.")

print()
print("=== AUDIT COMPLETE ===")
