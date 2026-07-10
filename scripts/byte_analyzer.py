# -*- coding: utf-8 -*-
"""
scripts/byte_analyzer.py

Binary-safe byte-level analyzer and reversible encoding pipeline.

Features:
- Binary-safe file reading
- Encoding detection (utf-8 vs cp1252)
- Preserve original bytes
- Use renderer.de_render / renderer.render for reversible pipeline
- Byte-by-byte comparison and diff analyzer
- Frequency analysis for recurring mismatches
- Exact mapping overrides for known problematic preview sequences
- Validation mode printing original byte, decoded glyph, and mapped Unicode

Usage:
  python -m scripts.byte_analyzer <file1> [file2 ...]

Outputs:
  - sandbox/byte_analysis.csv
  - sandbox/byte_analysis.json

"""

import sys
import os
import csv
import json
from collections import Counter, defaultdict

from renderer import de_render, render


EXACT_OVERRIDES = {
    # Preview-level exact overrides (cp1252-decoded preview -> replacement preview)
    # Requirement: create exact mapping overrides for problematic symbols
    # Pair: '›' <-> '¸'
    '›': '¸',
    '¸': '›',
    # The sequences below include bytes that when decoded as cp1252 yield
    # odd multi-char previews; provide symmetric replacements.
    # Left: literal bytes sequence decoded; Right: replacement preview string
    'î\x81µü™x': 'îµüŒ}',
    'îµüŒ}': 'î\x81µü™x',
}


def detect_encoding(bdata: bytes) -> str:
    """Detect whether bytes are UTF-8 or CP1252 (fallback).
    Heuristic: try strict utf-8 decoding; if it fails or re-encoding changes bytes,
    assume cp1252 (Windows-1252 / Latin1-like).
    """
    try:
        text = bdata.decode('utf-8')
        # Re-encode and compare to confirm exact roundtrip
        if text.encode('utf-8') == bdata:
            return 'utf-8'
    except Exception:
        pass
    return 'cp1252'


def lossless_cp1252_decode(barr: bytes) -> str:
    """Decode CP1252 but preserve bytes 129,141,143,144,157 as-is by mapping to same codepoint."""
    res_chars = []
    for b in barr:
        if b in (129, 141, 143, 144, 157):
            res_chars.append(chr(b))
        else:
            res_chars.append(bytes([b]).decode('cp1252', errors='replace'))
    return ''.join(res_chars)


def apply_exact_overrides(preview: str) -> str:
    # Apply exact overrides if a preview exactly matches a key
    return EXACT_OVERRIDES.get(preview, preview)


def analyze_file(path: str):
    with open(path, 'rb') as f:
        bdata = f.read()

    encoding = detect_encoding(bdata)

    if encoding == 'utf-8':
        try:
            text = bdata.decode('utf-8')
        except Exception:
            text = bdata.decode('utf-8', errors='replace')
    else:
        text = lossless_cp1252_decode(bdata)

    # Preview-level: cp1252-decoded preview string for byte-level comparisons
    try:
        preview_cp1252 = bdata.decode('cp1252', errors='replace')
    except Exception:
        preview_cp1252 = lossless_cp1252_decode(bdata)

    # Use renderer.de_render to map legacy bytes -> Unicode (logical mapping)
    try:
        mapped_unicode = de_render(bdata)
    except Exception as e:
        mapped_unicode = f"<de_render-error: {e}>"

    # Re-render mapped_unicode back to legacy bytes
    try:
        re_raw, re_preview, _ = render(mapped_unicode)
    except Exception as e:
        re_raw = b''
        re_preview = f"<render-error: {e}>"

    # Apply exact overrides at preview level before comparing (best-effort)
    preview_cp1252_adj = apply_exact_overrides(preview_cp1252)
    re_preview_adj = apply_exact_overrides(re_preview)

    # Byte-by-byte comparison
    orig = bdata
    new = re_raw
    minlen = min(len(orig), len(new))
    diffs = []
    for i in range(minlen):
        if orig[i] != new[i]:
            diffs.append({'pos': i, 'orig': f"0x{orig[i]:02x}", 'new': f"0x{new[i]:02x}"})

    if len(orig) != len(new):
        diffs.append({'pos': 'len', 'orig_len': len(orig), 'new_len': len(new)})

    matched = len(diffs) == 0

    return {
        'path': path,
        'encoding': encoding,
        'orig_hex': orig.hex(),
        'preview_cp1252': preview_cp1252,
        'preview_cp1252_adj': preview_cp1252_adj,
        'mapped_unicode': mapped_unicode,
        're_render_hex': new.hex(),
        're_preview': re_preview,
        're_preview_adj': re_preview_adj,
        'matched': matched,
        'diffs': diffs,
        'orig_len': len(orig),
        're_len': len(new),
    }


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        print("Usage: python -m scripts.byte_analyzer <file1> [file2 ...]")
        sys.exit(1)

    results = []
    freq_counter = Counter()
    for p in argv:
        if not os.path.exists(p):
            print(f"Skipping missing path: {p}")
            continue
        res = analyze_file(p)
        results.append(res)
        if not res['matched']:
            # Create a simple key for recurring mismatch patterns: first 4 bytes
            key = res['orig_hex'][:8]
            freq_counter[key] += 1

    out_csv = os.path.join('sandbox', 'byte_analysis.csv')
    out_json = os.path.join('sandbox', 'byte_analysis.json')
    os.makedirs('sandbox', exist_ok=True)

    # Write CSV
    with open(out_csv, 'w', newline='', encoding='utf-8') as cf:
        writer = csv.writer(cf)
        writer.writerow(['path', 'encoding', 'orig_len', 're_len', 'matched', 'preview_cp1252', 'mapped_unicode', 'diff_count'])
        for r in results:
            writer.writerow([r['path'], r['encoding'], r['orig_len'], r['re_len'], r['matched'], r['preview_cp1252_adj'], r['mapped_unicode'], len(r['diffs'])])

    # Write JSON
    with open(out_json, 'w', encoding='utf-8') as jf:
        json.dump({'results': results, 'freq': freq_counter.most_common()}, jf, ensure_ascii=False, indent=2)

    # Print summary and top frequency mismatches
    total = len(results)
    mismatched = sum(1 for r in results if not r['matched'])
    print(f"Analyzed {total} files — mismatched: {mismatched}")
    if freq_counter:
        print("Top mismatch signatures:")
        for k, v in freq_counter.most_common(10):
            print(f"  {k} : {v}")

    print(f"Wrote CSV: {out_csv}")
    print(f"Wrote JSON: {out_json}")


if __name__ == '__main__':
    main()
