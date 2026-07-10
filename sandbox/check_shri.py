# -*- coding: utf-8 -*-
import glob
import re

print("Searching for SHRI translations in test files:")
for filename in glob.glob("test_*.py"):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    # Find all correct_text blocks
    correct_match = re.search(r'correct_text\s*=\s*"""(.*?)"""', content, re.DOTALL)
    if not correct_match:
        correct_match = re.search(r"correct_text\s*=\s*'''(.*?)'''", content, re.DOTALL)
    if correct_match:
        text = correct_match.group(1)
        # Check if X (88) or öËÀ (246, 203, 192) or other bytes are present
        bytes_list = list(text.encode('cp1252', errors='replace'))
        count_x = bytes_list.count(88)
        count_oela = 0
        for i in range(len(bytes_list) - 2):
            if bytes_list[i] == 246 and bytes_list[i+1] == 203 and bytes_list[i+2] == 192:
                count_oela += 1
        print(f"File {filename}: X count = {count_x}, oela count = {count_oela}")
