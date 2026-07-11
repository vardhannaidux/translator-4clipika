import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from translation_engine import translate_text

para_user = "వేగుళ్ల స్వాగతం కార్యక్రమం నిర్విగ్నంగా ప్రత్యేక ప్రార్థనలు నిర్వహించారు కార్యకర్తలు వర్షం వర్గ సందర్భంగా వే ళ్ల స్వా ర్య ర్వి గ్న త్యే క ర్థ ర్వ ర్య ర్త ర్ష ర్గ ధ్యే ర్భ"
output = translate_text(para_user)

print("Output representation:")
print(output.encode("ascii", errors="backslashreplace").decode("ascii"))
