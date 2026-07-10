import json
import sys
from pathlib import Path
import copy

# Ensure repository root is on sys.path so imports work when run from /scripts
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

MISMATCHES = ROOT / 'sandbox' / 'ini_mismatches.json'
PROPOSALS = ROOT / 'sandbox' / 'ini_mismatch_proposals.py'
COMMITTED = ROOT / 'sandbox' / 'committed_proposals.py'

def load_proposals():
    ns = {}
    exec(PROPOSALS.read_text(encoding='utf-8'), ns)
    return ns.get('INI_MISMATCH_PROPOSALS', {})

def parse_ini_sequences():
    sequences = []
    with open('Telugu4CScript.ini', 'r', encoding='utf-8', errors='ignore') as f:
        in_consonents = False
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
                cleaned = [x for x in target_bytes if x != 8 and x != 500]
                if cleaned and cleaned not in sequences:
                    sequences.append(cleaned)
    return sequences

def build_local_decoder(rm):
    # return a function that mimics SequentialConverter.legacy_to_unicode using rm
    import unicodedata, re
    def normalize_punctuation(text):
        text = re.sub(r'[ \t\r\n]+', ' ', text)
        text = re.sub(r'[ \t]+([,.!?])', r'\1', text)
        return text

    def decode(data):
        if isinstance(data, str):
            data = data.encode('cp1252', errors='replace')
        byte_tuple = tuple(data)
        n = len(byte_tuple)
        i = 0
        tokens = []
        match_keys = sorted(rm.keys(), key=len, reverse=True)
        max_lookahead = len(match_keys[0]) if match_keys else 1
        while i < n:
            match_found = False
            for length in range(min(max_lookahead, n - i), 0, -1):
                chunk = byte_tuple[i: i + length]
                if chunk in rm:
                    tokens.append(rm[chunk])
                    i += length
                    match_found = True
                    break
            if not match_found:
                char = bytes([byte_tuple[i]]).decode('cp1252', errors='replace')
                tokens.append(char)
                i += 1
        text = ''.join(tokens)
        text = normalize_punctuation(text)
        return unicodedata.normalize('NFC', text)

    return decode

def main(batch_size=5):
    from translation_mappings import build_reverse_map
    from translate import translate_text
    from encode_user_correct import robust_encode

    base_rm = build_reverse_map()
    sequences = parse_ini_sequences()

    # baseline mismatches using current map
    decode_base = build_local_decoder(base_rm)
    baseline_mismatches = 0
    analyzed = 0
    for seq in sequences:
        try:
            u_text = decode_base(bytes(seq))
            if '\u0c63' in u_text or '\u0c62' in u_text or '\u0c04' in u_text or '\ufffd' in u_text:
                continue
            analyzed += 1
            gen_legacy = translate_text(u_text, strict_roundtrip=True)
            gen_bytes = list(robust_encode(gen_legacy))
            gen_canonical = [b for b in gen_bytes if b != 155]
            if gen_bytes != seq and gen_canonical != seq:
                baseline_mismatches += 1
        except Exception:
            continue

    print('baseline analyzed=', analyzed, 'mismatches=', baseline_mismatches)

    proposals = load_proposals()
    items = list(proposals.items())
    accepted = {}

    # iterate batches
    for i in range(0, len(items), batch_size):
        batch = dict(items[i:i+batch_size])
        # apply batch on top of base_rm
        test_rm = copy.copy(base_rm)
        test_rm.update(batch)
        decode_test = build_local_decoder(test_rm)

        mismatches = 0
        analyzed = 0
        for seq in sequences:
            try:
                u_text = decode_test(bytes(seq))
                if '\u0c63' in u_text or '\u0c62' in u_text or '\u0c04' in u_text or '\ufffd' in u_text:
                    continue
                analyzed += 1
                gen_legacy = translate_text(u_text, strict_roundtrip=True)
                gen_bytes = list(robust_encode(gen_legacy))
                gen_canonical = [b for b in gen_bytes if b != 155]
                if gen_bytes != seq and gen_canonical != seq:
                    mismatches += 1
            except Exception:
                continue

        print(f'tested batch {i//batch_size + 1}: mismatches={mismatches} (baseline {baseline_mismatches})')
        if mismatches < baseline_mismatches:
            print('  -> batch accepted')
            accepted.update(batch)
            # update baseline to new lower mismatches for subsequent batches
            baseline_mismatches = mismatches
        else:
            print('  -> batch rejected')

    # write accepted proposals
    with open(COMMITTED, 'w', encoding='utf-8') as f:
        f.write('# Auto-committed proposals that passed conservative batch testing\n')
        f.write('COMMITTED_PROPOSALS = {\n')
        for k, v in accepted.items():
            f.write(f'    {k}: {v!r},\n')
        f.write('}\n')

    print('Committed entries=', len(accepted))

if __name__ == '__main__':
    main()
