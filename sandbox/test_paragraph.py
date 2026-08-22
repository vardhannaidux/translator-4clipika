import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.stdout.reconfigure(encoding='utf-8')

from translation_engine import translate_text

paragraph = """చైతన్య స్కూల్ కలర్స్ ఇంఛార్జి లక్ష్యం ల్స్ స్వీకరణ పరిషత్ బాబ్జి నాయుడు కట్ అవుట్ శుభాకాంక్షలు కాల్చి స్వీట్లు చెప్పారు ఫ్రెండ్స్ స్టోర్స్ త్ ఆర్థోపెడిక్ కృష్ణారావు కార్యాలయం రమేష్ రాజు అభివృద్ధి ఫ్లాష్ ఉపాధ్యాయులు ఫిట్ నెస్"""

print("--- Paragraph Input ---")
print(paragraph)

print("\n--- Translating Paragraph ---")
res_para = translate_text(paragraph)
print("Paragraph Output:\n", repr(res_para))

print("\n--- Translating Word-by-Word ---")
words = paragraph.split()
res_words = [translate_text(w) for w in words]
print("Word-by-word joined:\n", repr(' '.join(res_words)))

print("\n--- Comparing Paragraph Output vs Word-by-Word Output ---")
para_words = res_para.split()
for i, (pw, ww) in enumerate(zip(para_words, res_words)):
    match = (pw == ww)
    status = "OK" if match else "MISMATCH"
    print(f"[{i+1:02d}] {words[i]:<15} | Para: {repr(pw):<20} | Word: {repr(ww):<20} | {status}")
