import sys
import subprocess
import re
import pathlib


def test_ini_mismatch_count_not_increasing():
    """Run the INI coverage script and ensure mismatches do not exceed baseline."""
    repo_root = pathlib.Path(__file__).resolve().parents[1]
    script = repo_root / 'sandbox' / 'check_ini_coverage.py'
    proc = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
    out = proc.stdout + proc.stderr
    m = re.search(r'Total mismatches:\s*(\d+)', out)
    assert m, 'Could not find mismatch count in coverage output'
    mismatches = int(m.group(1))
    baseline_file = repo_root / 'sandbox' / 'baseline_mismatch_count.txt'
    baseline = int(baseline_file.read_text().strip())
    assert mismatches <= baseline, f'Mismatches increased: {mismatches} > baseline {baseline}'
