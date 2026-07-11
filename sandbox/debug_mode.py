"""
debug_mode.py — Character-by-character debugger and visual tracer for Eenadu 4C Lipika conversion.
"""
import sys
import os
import unicodedata

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from translation_engine import _get_sorted_keys, translate_text
from translation_mappings import REVERSE_MAP, PHRASE_MAPPINGS, SPECIAL_RA_CLUSTERS
from linguistic_utils import segmentize, GraphemeClusterSegmenter

def debug_legacy_to_unicode(data):
    """
    Decodes legacy text and prints the step-by-step resolution of characters.
    Format: Input Character -> Matched Rule -> Replacement -> Final Unicode
    """
    if isinstance(data, str):
        data = data.encode('cp1252', errors='replace')
    byte_tuple = tuple(data)
    n = len(byte_tuple)
    i = 0
    match_keys, max_lookahead = _get_sorted_keys()
    
    print("\n=== DEBUG: LEGACY TO UNICODE TRANSLATION TRACE ===")
    header = f"{'Input Character/Byte':<30} -> {'Matched Rule':<30} -> {'Replacement':<20} -> {'Final Unicode'}"
    print(header)
    print("-" * 110)
    
    accumulated = []
    while i < n:
        match_found = False
        for length in range(min(max_lookahead, n - i), 0, -1):
            chunk = byte_tuple[i: i + length]
            if chunk in REVERSE_MAP:
                replacement = REVERSE_MAP[chunk]
                chunk_bytes_str = ", ".join(str(b) for b in chunk)
                try:
                    visual = bytes(chunk).decode('cp1252')
                    input_display = f"'{visual}' (bytes: {chunk_bytes_str})"
                except Exception:
                    input_display = f"bytes: {chunk_bytes_str}"
                
                rule_desc = f"REVERSE_MAP (len {length})"
                accumulated.append(replacement)
                final_unicode = "".join(accumulated)
                
                print(f"{input_display:<30} -> {rule_desc:<30} -> {repr(replacement):<20} -> {repr(final_unicode)}")
                i += length
                match_found = True
                break
        
        if not match_found:
            b = byte_tuple[i]
            char = bytes([b]).decode('cp1252', errors='replace')
            input_display = f"'{char}' (byte: {b})"
            rule_desc = "CP1252 Fallback"
            accumulated.append(char)
            final_unicode = "".join(accumulated)
            
            print(f"{input_display:<30} -> {rule_desc:<30} -> {repr(char):<20} -> {repr(final_unicode)}")
            i += 1
    print("=" * 110)
    return "".join(accumulated)


def debug_unicode_to_legacy(text):
    """
    Encodes Unicode Telugu text and prints the step-by-step resolution of syllables and phrases.
    """
    text = unicodedata.normalize("NFC", text)
    print("\n=== DEBUG: UNICODE TO LEGACY TRANSLATION TRACE ===")
    print(f"{'Input Unit':<30} -> {'Matched Rule':<30} -> {'Replacement (Visual)':<20} -> {'Final Legacy String'}")
    print("-" * 110)
    
    # 1. Phase-based protection trace
    protect_mappings = {}
    for key, val in PHRASE_MAPPINGS.items():
        norm_key = unicodedata.normalize("NFC", key)
        protect_mappings[norm_key] = ("PHRASE_MAPPINGS", val)
    for key, val in SPECIAL_RA_CLUSTERS.items():
        norm_key = unicodedata.normalize("NFC", key)
        val_str = bytes(val).decode('cp1252', errors='replace')
        protect_mappings[norm_key] = ("SPECIAL_RA_CLUSTERS", val_str)
        
    sorted_keys = sorted(protect_mappings.keys(), key=len, reverse=True)
    
    res_units = []
    i = 0
    n = len(text)
    token_id = 0
    token_dict = {}
    
    while i < n:
        match_found = False
        for key in sorted_keys:
            if text.startswith(key, i):
                rule_name, val = protect_mappings[key]
                token = f"__P_{token_id}__"
                token_dict[token] = (key, rule_name, val)
                res_units.append(token)
                i += len(key)
                token_id += 1
                match_found = True
                break
        if not match_found:
            res_units.append(text[i])
            i += 1
            
    # Trace protected phrases
    accumulated = []
    for unit in res_units:
        if unit.startswith("__P_") and unit.endswith("__"):
            key, rule_name, val = token_dict[unit]
            accumulated.append(val)
            final_str = "".join(accumulated)
            print(f"{repr(key):<30} -> {rule_name:<30} -> {repr(val):<20} -> {repr(final_str)}")
        else:
            # Render character-by-character or syllable-by-syllable
            syllables = segmentize(unit)
            for syl in syllables:
                from translation_engine import assemble_syllable
                bts = assemble_syllable(syl)
                val_str = bytes(bts).decode('cp1252', errors='replace')
                accumulated.append(val_str)
                final_str = "".join(accumulated)
                syl_display = syl.get('raw', str(syl))
                print(f"{repr(syl_display):<30} -> {'assemble_syllable':<30} -> {repr(val_str):<20} -> {repr(final_str)}")
                
    print("=" * 110)
    return "".join(accumulated)


if __name__ == "__main__":
    # Test reverse direction
    legacy_input = "î¶ÞœªüŒx"
    decoded = debug_legacy_to_unicode(legacy_input)
    
    # Test forward direction
    unicode_input = "వేగుళ్ల"
    encoded = debug_unicode_to_legacy(unicode_input)
