"""
Deep diagnostic: compare correct vs got bytes from user's Step 541 report.
Also run idempotency tests (same input 100x must produce same output).
"""
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from translation_engine import translate_text

para_user = "వేగుళ్ల స్వాగతం కార్యక్రమం నిర్విగ్నంగా ప్రత్యేక ప్రార్థనలు నిర్వహించారు కార్యకర్తలు వర్షం వర్గ సందర్భంగా వే ళ్ల స్వా ర్య ర్వి గ్న త్యే క ర్థ ర్వ ర్య ర్త ర్ష ర్గ ధ్యే ర్భ"

# From user Step 541 - what they GOT (wrong)
got_str = (
    "\xee\xb6\xde\u0153\xaa\xfc\u0152x \xfa\xa7y\xde\u0153\xea\u0178\xd9 \xda\xa5\xf4\xc2\xf3\u0178\xaav\xda\xdb\xf7\xaa\xd9 E\xf4\xc2N\xde\u0153o\xd9\xde\xa5 v\xed\xa3\xb8\xeau\xda\xdb v\xf0\xa7\xf4\xc2\xeb\xc7]\xec\xf5\xaa E\xf4\xc2\xf7\xef\u2021\xb0\xd9\xe0\xa6\xf4\xa2\xaa \xda\xa5\xf4\xc2\xf3\u0178\xaa\xda\xdb\xf4\xc2\xea\u0178\xf5\xaa \xf7\xf4\xc2\xf9\xa3\xd9 \xf7\xf4\xc2\xde\u0153 \xfa\xa3\xd9\xeb]\xf4\xc2\xf2\xc5\xa1\xd9\xde\xa5"
)

# From user Step 541 - what they EXPECTED (correct)
correct_str = (
    "\xee\xb6\xde\u0153\xaa\xfc\u0152x \xfe\xa7y\xde\u0153\xea\u0178\xd9 \xda\xa5\xf4\xa2uv\xda\xdb\xf7\xaa\xd9 EJy\xde\u0153o\xd9\xde\xa5 v\xed\xa3\xea\xb6u\xda\xdb v\xf0\xa7\xf4\xa2\u2013\xec\xf5\xaa E\xf4\xa2y\xef\u2021\xb0\xd9\xe0\xa6\xf4\xa2\xaa \xda\xa5\xf4\xa2u\xda\xdb\xf4\xa2h\xf5\xaa \xf7\xf4\xa2{\xd9 \xf7\xf4\xa2_ \xfa\xa3\xd9\xeb]\xf4\xa2(\xc4\xd9\xde\xa5"
)

# What our engine produces NOW
our_output = translate_text(para_user)

print("=== COMPARISON (first 11 words only) ===")
got_words    = got_str.split(" ")
correct_words = correct_str.split(" ")
our_words    = our_output.split(" ")

word_names = [
    "వేగుళ్ల","స్వాగతం","కార్యక్రమం","నిర్విగ్నంగా",
    "ప్రత్యేక","ప్రార్థనలు","నిర్వహించారు","కార్యకర్తలు",
    "వర్షం","వర్గ","సందర్భంగా"
]

def safe(s):
    return s.encode("ascii", errors="backslashreplace").decode("ascii")

for i, name in enumerate(word_names):
    got_b    = [ord(c) for c in got_words[i]]    if i < len(got_words)     else []
    corr_b   = [ord(c) for c in correct_words[i]] if i < len(correct_words) else []
    our_b    = [ord(c) for c in our_words[i]]    if i < len(our_words)     else []
    match_corr = our_b == corr_b
    match_got  = our_b == got_b
    status = "CORRECT" if match_corr else ("GOT_BAD" if match_got else "DIFFERENT")
    nm_safe = name.encode("ascii","backslashreplace").decode("ascii")
    print(f"[{i}] {nm_safe}: {status}")
    if not match_corr:
        print(f"  GOT     : {got_b}")
        print(f"  EXPECTED: {corr_b}")
        print(f"  OURS    : {our_b}")

print()
print("=== IDEMPOTENCY TEST (100 translations) ===")
first_result = translate_text(para_user)
all_same = True
for run in range(100):
    result = translate_text(para_user)
    if result != first_result:
        print(f"FAIL at run {run+1}: output differs!")
        print(f"  First : {safe(first_result[:60])}")
        print(f"  Run {run+1}: {safe(result[:60])}")
        all_same = False
        break
if all_same:
    print("PASS: All 100 runs produced identical output.")

print()
print("=== IDEMPOTENCY TEST - Translate output again (double-conversion check) ===")
output1 = translate_text(para_user)
output2 = translate_text(output1)  # translating the translated output!
if output1 == output2:
    print("PASS: translate_text(output) == output (idempotent)")
else:
    print("FAIL: Double conversion changes the output!")
    print(f"  output1: {safe(output1[:80])}")
    print(f"  output2: {safe(output2[:80])}")

print()
print("=== STATE LEAK TEST (alternate inputs) ===")
inputs = [
    "వేగుళ్ల",
    "కార్యక్రమం",
    "నిర్విగ్నంగా",
    "స్వాగతం",
    "నిర్వహించారు",
]
# First run baseline
baseline = {inp: translate_text(inp) for inp in inputs}
# Alternate run
for cycle in range(5):
    for inp in inputs:
        result = translate_text(inp)
        if result != baseline[inp]:
            nm_safe = inp.encode("ascii","backslashreplace").decode("ascii")
            print(f"FAIL cycle={cycle} input={nm_safe}: state leak detected!")
            print(f"  Expected: {safe(baseline[inp])}")
            print(f"  Got     : {safe(result)}")
            break
    else:
        continue
    break
else:
    print("PASS: No state leakage detected over 5 alternating cycles.")
