# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.getcwd())

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

from translation_engine import translate_text

telugu_inputs = [
    "ల్లి",
    "టీ ఎస్ ఎం",
    "ష్ణా",
    "రెడ్డి",
    "ర్ఘ",
    "సర్పంచి",
    "సర్పంచ్",
    "ఒక",
    "క్తి",
    "కాంగ్రెస్",
    "ప్పు",
    "య్యే",
    "ర్జ్",
    "మా",
    "మళ్ళి",
    "డ్పి",
    "ట్",
    "సొంత",
    "స్వా"
]

out_lines = []
for w in telugu_inputs:
    translated = translate_text(w)
    line = f"{w} -> {translated} (repr: {repr(translated)})"
    out_lines.append(line)
    print(line)

with open("sandbox/mappings_output.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out_lines) + "\n")
