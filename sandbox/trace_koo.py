import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from translation_engine import translate_text

res = translate_text("కో")
print("ko bytes:", [ord(c) for c in res])
