import pytest
from pathlib import Path
import shutil
_ROOT = Path(__file__)


@pytest.fixture(scope="session")
def session_tempdir():
    tempdir = Path(_ROOT, "temp")
    tempdir.mkdir()
    yield tempdir
    shutil.rmtree(tempdir)


@pytest.fixture(scope="session")
def test_files_dir():
    return Path(_ROOT, "test_files")



