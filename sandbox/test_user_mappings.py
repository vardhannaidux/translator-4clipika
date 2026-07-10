import sys
import unicodedata
from translation_engine import translate_text

pairs = [
    ("ద్వారపూడి", "ద్వా", "ë¯yô¢í£²è…", "ë¯y"),
    ("కాలనీ", "నీ", "Ú¥õF", "F"),
    ("ఎదుర్కొంటున్నారు", "ర్కొన్నా", "Óë]ªô•\Ùåªû¦oô¢ª", "ô•\û¦o"),
    ("సత్యమూర్తి", "మూర్తి", "ú£êŸu÷´Jh", "÷´Jh"),
    ("చేయిస్తానన్నారు", "స్తాన్నా", "à¶ô³þ§hìû¦oô¢ª", "þ§hû¦o"),
    ("ఇబ్బందులు", "ఇబ్బందులు", "Ïñ(Ùë]ªõª", "Ïñ(Ùë]ªõª"),
    ("మేము", "ము", "î¶ª÷³", "÷³"),
    ("మాతృత్వ", "మా", "÷«êŸ”êŸy", "÷«"),
    ("కేంద్ర", "కేంద్ర", "¸ÚÙvë]", "¸ÚÙvë]"),
    ("పూర్తి", "పూర్తి", "í£²Jh", "í£²Jh"),
    ("కేశవరం", "కేశవరం", "¸ÚøŒ÷ô¢Ù", "¸ÚøŒ÷ô¢Ù"),
    ("వైద్యుడు", "వైద్యుడు", "îµjë]ªuè[ª", "îµjë]ªuè[ª"),
    ("అభయాన్", "భి", "ÍGÅóŸ«ûÂ", "GÅ"),
    ("గర్భిణీ", "గర్భిణీ", "ÞœJ(Äé©", "ÞœJ(Äé©"),
    ("స్త్రీ", "స్త్రీ", "vúˆh", "vúˆh"),
    ("అన్నారు", "అన్నా", "Íû¦oô¢ª", "û¦o"),
    ("ద్వారా", "ద్వారా", "ë¯yô¦", "ë¯yô¦"),
    ("తగ్గిందన్నారు", "తగ్గిందన్నారు", "êŸT_Ùë]û¦oô¢ª", "êŸT_Ùë]û¦oô¢ª"),
    ("కార్యక్రమంలో", "కార్యక్రమంలో", "Ú¥ô¢uvÚÛ÷ªÙöËº", "Ú¥ô¢uvÚÛ÷ªÙöËº"),
    ("సౌకర్యం", "సౌకర్యం", "þ¿ÚÛô¢uÙ", "þ¿ÚÛô¢uÙ"),
    ("విజ్ఞప్తి", "విజ్ఞప్తి", "Ná‘í‡h", "Ná‘í‡h"),
    ("ప్రారంభించి", "ప్రారంభించి", "vð§ô¢ÙGÅÙ#", "vð§ô¢ÙGÅÙ#"),
    ("మాట్లాడుతూ", "మాట్లాడుతూ", "÷«æ°xè[ªêŸ«", "÷«æ°xè[ªêŸ«"),
    ("ప్రాథమిక", "ప్రాథమిక", "vð§ëÅ]NªÚÛ", "vð§ëÅ]NªÚÛ"),
    ("వచ్చే", "వచ్చే", "÷à¶a", "÷à¶a"),
    ("గొట్టాలకు", "గొట్టాలకు", "Þ•æ°dõÚÛª", "Þ•æ°dõÚÛª"),
    ("అర్తమూరు", "అర్తమూరు", "Íô¢h÷´ô¢ª", "Íô¢h÷´ô¢ª"),
    ("ఏర్పడి", "ఏర్పడి", "Ôô¢pè…", "Ôô¢pè…"),
    ("మరమ్మతులు", "మరమ్మతులు", "÷ªô¢÷ªtêŸªõª", "÷ªô¢÷ªtêŸªõª")
]

# We will write the comparison result to a file in utf-8
with open("sandbox/user_test_out.txt", "w", encoding="utf-8") as f:
    f.write(f"{'Telugu Input':<20} | {'Expected (Latin)':<30} | {'Actual (Latin)':<30} | {'Exp Ords':<30} | {'Act Ords':<30} | Status\n")
    f.write("-" * 170 + "\n")
    for word, part, exp_word_legacy, exp_part_legacy in pairs:
        actual_word = translate_text(word, editorial_mode=True)
        status = "OK" if actual_word == exp_word_legacy else "MISMATCH"
        
        # Get ords for debug
        exp_w_ords = [ord(c) for c in exp_word_legacy]
        act_w_ords = [ord(c) for c in actual_word]
        
        f.write(f"{word:<20} | {exp_word_legacy:<30} | {actual_word:<30} | {str(exp_w_ords):<30} | {str(act_w_ords):<30} | {status}\n")
        
        if part:
            actual_part = translate_text(part, editorial_mode=True)
            status_part = "OK" if actual_part == exp_part_legacy else "MISMATCH"
            
            exp_p_ords = [ord(c) for c in exp_part_legacy]
            act_p_ords = [ord(c) for c in actual_part]
            
            f.write(f"  (part) {part:<13} | {exp_part_legacy:<30} | {actual_part:<30} | {str(exp_p_ords):<30} | {str(act_p_ords):<30} | {status_part}\n")

print("Done! Wrote to sandbox/user_test_out.txt")
