from pathlib import Path
import translation_mappings

ROOT = Path(__file__).resolve().parents[1]
COMMITTED = ROOT / 'sandbox' / 'committed_proposals.py'


def test_committed_proposals_file_exists_and_loaded():
    assert COMMITTED.exists(), f'{COMMITTED} missing'
    ns = {}
    exec(COMMITTED.read_text(encoding='utf-8'), ns)
    committed = ns.get('COMMITTED_PROPOSALS', {})
    assert isinstance(committed, dict)
    assert len(committed) >= 0


def test_embedded_committed_proposals_are_in_reverse_map():
    embedded = getattr(translation_mappings, 'EMBEDDED_COMMITTED_PROPOSALS', {})
    assert isinstance(embedded, dict)
    rm = translation_mappings.build_reverse_map()
    for key, value in embedded.items():
        assert key in rm
        assert rm[key] == value
