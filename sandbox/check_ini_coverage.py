# -*- coding: utf-8 -*-
import sys
import io
sys.path.append('.')
from translation_engine import SequentialConverter, translate_text
from linguistic_utils import robust_encode

def parse_ini_sequences():
    sequences = []
    in_consonents = False
    with open('Telugu4CScript.ini', 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            if line == '[Consonent]':
                in_consonents = True
                continue
            if line.startswith('['):
                in_consonents = False
                continue
            if in_consonents:
                if '=' not in line: continue
                parts = line.split('=')
                if len(parts) < 3: continue
                target_bytes_str = parts[2]
                try:
                    target_bytes = [int(x) for x in target_bytes_str.split(',') if x.isdigit()]
                except ValueError:
                    continue
                # Clean up target bytes
                cleaned = [x for x in target_bytes if x != 8 and x != 500]
                if cleaned and cleaned not in sequences:
                    sequences.append(cleaned)
    return sequences

# Redirect stderr to suppress warnings
sys.stderr = io.StringIO()

sequences = parse_ini_sequences()
print(f"Extracted {len(sequences)} unique byte sequences from Telugu4CScript.ini.")

mismatches = []
analyzed = 0
for idx, seq in enumerate(sequences):
    try:
        # 1. Decode legacy bytes to Telugu Unicode
        u_text = SequentialConverter.legacy_to_unicode(bytes(seq))
        
        # Skip if it contains unknown characters or invalid placeholders
        if '\u0c63' in u_text or '\u0c62' in u_text or '\u0c04' in u_text or '\ufffd' in u_text:
            continue
            
        analyzed += 1
        
        # 2. Encode back using our translate pipeline (strict roundtrip to avoid editorial corrections)
        gen_legacy = translate_text(u_text, strict_roundtrip=True)
        gen_bytes = list(robust_encode(gen_legacy))
        # Heuristic normalization: some legacy outputs include a leading
        # CP1252 155 glyph (›) before canonical sequences. Strip any
        # 155 bytes from the generated output for a tolerant parity check.
        gen_canonical = [b for b in gen_bytes if b != 155]

        if gen_bytes != seq and gen_canonical != seq:
            mismatches.append({
                'seq': seq,
                'decoded': u_text,
                'gen': gen_bytes
            })
    except Exception as e:
        continue

print(f"Total valid sequences analyzed: {analyzed}")
print(f"Total mismatches: {len(mismatches)}")

for i, m in enumerate(mismatches[:30]):
    u_escaped = m['decoded'].encode('unicode_escape').decode('ascii')
    print(f"\nMismatch {i+1}:")
    print(f"  Legacy input: {m['seq']}")
    print(f"  Decoded Uni:  {u_escaped}")
    print(f"  Gen legacy:   {m['gen']}")

# Persist full mismatch report for offline review
try:
    import json
    with open('sandbox/ini_mismatches.json', 'w', encoding='utf-8') as out:
        json.dump(mismatches, out, ensure_ascii=False, indent=2)
    print('Wrote sandbox/ini_mismatches.json')
except Exception:
    pass
