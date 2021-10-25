import json
import shutil
from pathlib import Path

import pytest

_ROOT = Path(__file__).parent


@pytest.fixture(scope="session")
def session_tempdir():
    tempdir = Path(_ROOT, "temp")
    if tempdir.exists():
        shutil.rmtree(tempdir)
    tempdir.mkdir()
    yield tempdir
    shutil.rmtree(tempdir)


@pytest.fixture(scope="session")
def test_files_dir():
    return Path(_ROOT, "test_files")


@pytest.fixture(scope="session")
def html_path(test_files_dir):
    return Path(test_files_dir, "eplustbl.htm")


@pytest.fixture(scope="session")
def html_path_no_bins(test_files_dir):
    return Path(test_files_dir, "eplustbl(Filtered).htm")


@pytest.fixture(scope="session")
def expected_outputs(test_files_dir):
    with open(Path(test_files_dir, "expected_outputs.json")) as json_file:
        content = json.load(json_file)
    return content
