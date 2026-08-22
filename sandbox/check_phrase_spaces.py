import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.stdout.reconfigure(encoding='utf-8')

import translation_mappings as tm

space_mismatches = []
for k, v in tm.PHRASE_MAPPINGS.items():
    if ' ' in k:
        k_spaces = k.count(' ')
        v_spaces = v.count(' ')
        if k_spaces != v_spaces:
            space_mismatches.append((k, v, k_spaces, v_spaces))

print(f"Total phrase keys with spaces: {sum(1 for k in tm.PHRASE_MAPPINGS if ' ' in k)}")
print(f"Space count mismatches: {len(space_mismatches)}")
print("\nMismatched Keys:")
for k, v, ks, vs in space_mismatches:
    print(f"  Key: {repr(k):<30} (spaces: {ks}) -> Value: {repr(v):<30} (spaces: {vs})")
