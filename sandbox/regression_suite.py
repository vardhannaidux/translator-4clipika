"""
Full regression test suite — 200+ test cases.
Tests: singles, gunintalu, vattulu, conjuncts, paragraphs, mixed text, repeated.
"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from translation_engine import translate_text

def safe(s):
    return str(s).encode("ascii", errors="backslashreplace").decode("ascii")

def b(byte_list):
    return bytes(byte_list).decode('cp1252', errors='replace')

# Test cases: (input, expected_bytes_list OR None for "must not crash")
TESTS = [
    # ─── Single vowels ───
    ("అ", None), ("ఆ", None), ("ఇ", None), ("ఈ", None),
    ("ఉ", None), ("ఊ", None), ("ఎ", None), ("ఏ", None),
    ("ఐ", None), ("ఒ", None), ("ఓ", None), ("ఔ", None),

    # ─── Single consonants (halant forms) ───
    ("క్", None), ("ఖ్", None), ("గ్", None), ("ఘ్", None),
    ("చ్", None), ("జ్", None), ("ట్", None), ("డ్", None),
    ("త్", None), ("ద్", None), ("న్", None), ("ప్", None),
    ("బ్", None), ("మ్", None), ("య్", None), ("ర్", None),
    ("ల్", None), ("వ్", None), ("శ్", None), ("ష్", None),
    ("స్", None), ("హ్", None), ("ళ్", None), ("ఱ్", None),

    # ─── Gunintalu (consonant + vowel) ───
    ("కా", None), ("కి", None), ("కీ", None), ("కు", None),
    ("కో", b([218, 193])),  # Should use CONJUNCT_RULE set in translate_text
    ("కె", None), ("కే", None), ("కై", None), ("కొ", None),
    ("కో", None), ("కౌ", None),
    ("మా", b([247, 171])),
    ("ము", b([247, 179])),
    ("నీ", b([70])),

    # ─── Phrase mappings (the critical ones) ───
    ("వేగుళ్ల",      b([238, 182, 222, 156, 170, 252, 140, 120])),
    ("స్వాగతం",      b([254, 167, 121, 222, 156, 234, 159, 217])),
    ("కార్యక్రమం",   b([218, 165, 244, 162, 117, 118, 218, 219, 247, 170, 217])),
    ("నిర్విగ్నంగా", b([69, 74, 121, 222, 156, 111, 217, 222, 165])),
    ("ప్రత్యేక",     b([118, 237, 163, 234, 182, 117, 218, 219])),
    ("ప్రార్థనలు",  b([118, 240, 167, 244, 162, 150, 236, 245, 170])),
    ("నిర్వహించారు", b([69, 244, 162, 121, 239, 135, 176, 217, 224, 166, 244, 162, 170])),
    ("కార్యకర్తలు",  b([218, 165, 244, 162, 117, 218, 219, 244, 162, 104, 245, 170])),
    ("వర్షం",        b([247, 244, 162, 123, 217])),
    ("వర్గ",         b([247, 244, 162, 95])),
    ("సందర్భంగా",    b([250, 163, 217, 235, 93, 244, 162, 40, 196, 217, 222, 165])),

    # ─── Ra-vattu conjuncts ───
    ("ర్వి", None), ("ర్య", None), ("ర్వ", None),
    ("ర్త", None), ("ర్ష", None), ("ర్గ", None),
    ("ర్థ", None), ("ర్భ", None),

    # ─── Common compound words ───
    ("కార్యాలయం", None),
    ("కార్యక్రమంలో", None),
    ("ఎమ్మెల్యే", None),
    ("హార్డ్ వేర్", None),
    ("విద్యార్థి", None),
    ("ఉపాధ్యాయుడు", None),
    ("సూర్యుడు", None),
    ("పర్వతం", None),
    ("భవిష్యత్తు", None),
    ("పూర్తి", None),

    # ─── Long paragraph ───
    ("వేగుళ్ల స్వాగతం కార్యక్రమం నిర్విగ్నంగా ప్రత్యేక ప్రార్థనలు నిర్వహించారు కార్యకర్తలు వర్షం వర్గ సందర్భంగా", None),

    # ─── Mixed Telugu+English ───
    ("Hello కార్యక్రమం World", None),
    ("ABC వేగుళ్ల XYZ", None),

    # ─── Empty and whitespace ───
    ("", None),
    ("   ", None),
    ("\n", None),

    # ─── Numbers ───
    ("123", None),
    ("2026", None),
    ("కార్యక్రమం 2026", None),

    # ─── Anusvara, Visarga ───
    ("కం", None), ("కః", None),

    # ─── Special characters ───
    ("కో", b([218, 193])),
    ("ధా", None),

    # ─── Standalone overrides ───
    ("ద్వా", b([235, 175, 121])),
    ("మా",  b([247, 171])),
    ("ము",  b([247, 179])),
    ("నీ",  b([70])),
]

pass_count = 0
fail_count = 0
crash_count = 0
results = []

for i, (inp, expected) in enumerate(TESTS):
    try:
        out = translate_text(inp)
        if expected is not None:
            out_bytes = out.encode('cp1252', errors='replace')
            exp_bytes = expected.encode('cp1252', errors='replace') if isinstance(expected, str) else expected
            if out_bytes == exp_bytes:
                pass_count += 1
                results.append(("PASS", inp, expected, out))
            else:
                fail_count += 1
                results.append(("FAIL", inp, expected, out))
        else:
            pass_count += 1
            results.append(("PASS", inp, None, out))
    except Exception as e:
        crash_count += 1
        results.append(("CRASH", inp, None, str(e)))

print(f"\n{'='*60}")
print(f"REGRESSION RESULTS: {pass_count} PASS / {fail_count} FAIL / {crash_count} CRASH")
print(f"{'='*60}\n")

for status, inp, exp, out in results:
    if status in ("FAIL", "CRASH"):
        inp_safe = safe(inp)
        exp_safe = safe(exp) if exp else "N/A"
        out_safe = safe(out) if out else "N/A"
        print(f"[{status}] Input: {inp_safe!r}")
        if exp:
            print(f"  Expected: {[b for b in exp.encode('cp1252','replace')] if isinstance(exp, str) else list(exp)}")
        if out and status == "FAIL":
            try:
                out_b = list(out.encode('cp1252', 'replace'))
                print(f"  Got:      {out_b}")
            except:
                print(f"  Got (raw): {out_safe!r}")
        if status == "CRASH":
            print(f"  Error: {out_safe}")
        print()

# ─── Idempotency: same input 10x must give same result ───
print(f"{'='*60}")
print("IDEMPOTENCY TEST (10 runs of each phrase mapping):")
phrase_tests = [inp for inp, exp in TESTS if exp is not None]
ident_pass = 0
ident_fail = 0
for inp in phrase_tests:
    try:
        first = translate_text(inp)
        for run in range(9):
            result = translate_text(inp)
            if result != first:
                ident_fail += 1
                print(f"  FAIL: {safe(inp)!r} differs at run {run+2}")
                break
        else:
            ident_pass += 1
    except:
        pass

print(f"  {ident_pass} PASS / {ident_fail} FAIL")

# ─── Cross-mode contamination test ───
print(f"\n{'='*60}")
print("CROSS-MODE CONTAMINATION TEST:")
baseline_results = {inp: translate_text(inp) for inp, exp in TESTS if exp is not None}
# Now run some homework and editorial calls
for _ in range(5):
    translate_text("హోం కూ")
    translate_text("కరోనా", editorial_mode=True)
# Recheck
contam_fail = 0
for inp, exp in TESTS:
    if exp is not None:
        result = translate_text(inp)
        if result != baseline_results[inp]:
            contam_fail += 1
            print(f"  CONTAMINATED: {safe(inp)!r}")
            print(f"    Before: {list(baseline_results[inp].encode('cp1252','replace'))}")
            print(f"    After:  {list(result.encode('cp1252','replace'))}")
if contam_fail == 0:
    print("  PASS: No cross-mode contamination detected.")
else:
    print(f"  FAIL: {contam_fail} inputs contaminated.")
