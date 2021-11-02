import subprocess
from pathlib import Path

import pytest


def test_exe_exists(exe_path):
    assert exe_path.exists()


@pytest.mark.parametrize("output", ["csv"])
def test_exe(exe_path, html_path, test_tempdir, output):
    args = [exe_path, "-i", html_path, "-o", test_tempdir, "--no-dialogs"]
    subprocess.run(args)
    for name in [
        "Distribution - ZONE MEAN AIR TEMPERATURE.csv",
        "Distribution - ZONE OPERATIVE TEMPERATURE.csv",
        "Distribution - ZONE MEAN RADIANT TEMPERATURE.csv",
    ]:
        assert Path(test_tempdir, name).exists()
