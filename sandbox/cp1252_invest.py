"""
Investigate CP1252 vs Unicode codepoint issue.
"""
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.stdout.reconfigure(encoding='utf-8')
import translation_mappings as tm
from translation_engine import assemble_syllable, translate_text
from linguistic_utils import segmentize

# KEY INSIGHT: assemble_syllable returns CP1252 byte values (0-255)
# But the translate_text pipeline decodes them as cp1252 -> unicode
# So byte 136 in CP1252 = Unicode 710 (ˆ)
# The expected output contains Unicode codepoints like 710, 338, 376 etc
# which represent what you GET after cp1252 decoding

# verify:
b136 = bytes([136])
print('CP1252 byte 136 decodes to Unicode:', ord(b136.decode('cp1252')), '=', repr(b136.decode('cp1252')))
b140 = bytes([140])
print('CP1252 byte 140 decodes to Unicode:', ord(b140.decode('cp1252')), '=', repr(b140.decode('cp1252')))
b159 = bytes([159])
print('CP1252 byte 159 decodes to Unicode:', ord(b159.decode('cp1252')), '=', repr(b159.decode('cp1252')))

print()
print('So expected [250, 710, 121] means:')
print('  250 = byte 250 = unicode 250 (ú)')
print('  710 = unicode 710 (ˆ) = CP1252 byte 136')
print('  121 = byte 121 = unicode 121 (y)')
print('This means translate_text returns Unicode codepoints (decoded from CP1252)')

print()
print('=== ఉద్దేశం trace ===')
syls = segmentize('ఉద్దేశం')
for s in syls:
    b = assemble_syllable(s)
    # Decode as cp1252 to get unicode
    try:
        decoded = bytes(b).decode('cp1252')
        decoded_ords = [ord(c) for c in decoded]
    except Exception as e:
        decoded_ords = [f'ERR:{e}']
    print(f"  syl={s.get('raw','?')!r}: cp1252_bytes={b} -> unicode_ords={decoded_ords}")

result = translate_text('ఉద్దేశం')
print(f"  translate_text: {[ord(c) for c in result]}")
print(f"  Expected:       [105, 209, 235, 182, 204, 196, 248, 338, 217]")

# Now: 105=i, 209=Ñ... Let's decode expected as cp1252
exp_unicode = [105, 209, 235, 182, 204, 196, 248, 338, 217]
# Convert back to bytes: 338 = Unicode Œ = CP1252 byte 140
# 204 = Ì = byte 204, 196 = Ä = byte 196
print()
print('Expected unicode codepoints -> cp1252 bytes:')
for u in exp_unicode:
    if u < 256:
        cp = u  # direct
    else:
        # find cp1252 byte for this unicode
        try:
            b = chr(u).encode('cp1252')
            cp = b[0]
        except:
            cp = None
    print(f'  unicode {u} -> cp1252 byte {cp}')

# So what are [105, 235, 182, 204, 196] in context?
# 105='i' = ASCII 'i', 235='ë', 182='¶', 204='Ì', 196='Ä'
# Wait: 105 = 'i' (ASCII letter i)! This is NOT a vowel - it's a GLYPH component
# ఉద్దేశం breakdown: ఉ+ద్+దే+శ+ం
# Expected: i(105) + Ñ(209) + ë(235) + ¶(182) + Ì(204) + Ä(196) + ø(248) + Œ(338->140) + Ù(217)
# So ఉ would need to produce TWO bytes: [105, 209]
# But ఉంటుంది PASSES with ఉ=[209] only (1 byte)!
# The difference: ఉంటుంది has ఉ standalone, then ం
# ఉద్దేశం has ఉ + ద్ which combines
# Actually wait - could ద్ produce a PRE-BASE mark that goes BEFORE ఉ?
# In Telugu rendering, some consonants have pre-matras that appear before the syllable
# But that's for vowel matras, not consonant combinations

print()
print('=== ద్దే assembly ===')
syls2 = segmentize('ద్దే')
for s in syls2:
    b = assemble_syllable(s)
    decoded = bytes([x for x in b if x < 256]).decode('cp1252', errors='replace')
    dec_ords = [ord(c) for c in bytes(b).decode('cp1252', errors='replace')] if all(x < 256 for x in b) else b
    print(f"  syl={s.get('raw','?')!r}: cp1252_bytes={b} decoded={dec_ords}")

# Check: current output for ఉద్దేశం = [209, 235, 195, 235, 182, 248, 338, 217]
# 235 appears TWICE and 195 in between
# Our assemble gives: ఉ=[209], ద్దే=[184,235,204], శం=[248,140,217]
# But translate_text gives:       [209, 235, 195, 235, 182, 248, 338, 217]
# This is DIFFERENT from assembly! Something in the translate pipeline changes it

print()
print('=== Checking PHRASE_MAPPINGS for ద్దే ===')
for k, v in tm.PHRASE_MAPPINGS.items():
    if 'ద్ద' in k or 'ద్దే' in k:
        print(f"  PHRASE[{k!r}] = {[ord(c) for c in v]}")

# Check GLOBAL_CORRECTIONS
print()
print('=== GLOBAL_CORRECTIONS for ద ===')
for k, v in tm.GLOBAL_CORRECTIONS.items():
    if 'ద' in k or 'ఉ' in k:
        print(f"  GC[{k!r}] = {v!r}")
