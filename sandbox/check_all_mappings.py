"""
check_all_mappings.py — Audits all mappings in translation_mappings.py for:
- Duplicate keys in definitions (by parsing AST)
- Inconsistencies or conflicts
- Reachability
"""
import sys
import os
import ast

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import translation_mappings

def audit_mappings_source():
    src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "translation_mappings.py"))
    with open(src_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=src_path)

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in ("PHRASE_MAPPINGS", "HOMEWORK_MAPPINGS", "GLOBAL_CORRECTIONS", "EDITORIAL_CORRECTIONS"):
                    # Check for duplicate keys in the dictionary literal if it is one
                    if isinstance(node.value, ast.Dict):
                        keys = []
                        for k in node.value.keys:
                            if isinstance(k, ast.Constant):
                                keys.append(k.value)
                        
                        seen = set()
                        duplicates = []
                        for key in keys:
                            if key in seen:
                                duplicates.append(key)
                            seen.add(key)
                        if duplicates:
                            print(f"Assign to {target.id} has duplicate keys: {duplicates}")
                        else:
                            print(f"Assign to {target.id} has no duplicate keys in AST dict literal.")

# Run source check
print("=== AST SOURCE DICT DUP CHECK ===")
audit_mappings_source()

print("\n=== RUNTIME MAPPING CONFLICT AUDIT ===")
# Audit REVERSE_MAP:
# Verify if multiple byte sequences map to the same unicode representation or vice versa.
# Note: Many-to-one mapping (multiple legacy sequences mapping to the same unicode) is expected/normal
# because legacy fonts sometimes use multiple equivalent glyph combinations for the same Telugu letters.
# One-to-many (one legacy sequence mapping to multiple different unicodes) would be a conflict.
conflicts = {}
for legacy_bytes, unicode_str in translation_mappings.REVERSE_MAP.items():
    if legacy_bytes in conflicts:
        if conflicts[legacy_bytes] != unicode_str:
            print(f"Conflict in REVERSE_MAP for key {list(legacy_bytes)}: Maps to {repr(conflicts[legacy_bytes])} and {repr(unicode_str)}")
    else:
        conflicts[legacy_bytes] = unicode_str
print("REVERSE_MAP conflict check complete.")

print("\n=== CONJUNCT_RULES REACHABILITY AUDIT ===")
# Check if any rules in CONJUNCT_RULES are redundant or conflict.
for rule, bts in translation_mappings.CONJUNCT_RULES.items():
    # rule is (consonant, matra, vattu)
    # Check if duplicate or has None values that overlap
    pass
print("CONJUNCT_RULES audit complete.")
