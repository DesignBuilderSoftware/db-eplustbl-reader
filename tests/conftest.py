import importlib.metadata as importlib_metadata
import json
import platform
import shutil
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def root_dir():
    return Path(__file__).parents[1]


@pytest.fixture(scope="session")
def test_root_dir():
    return Path(__file__).parent


@pytest.fixture(scope="session")
def test_files_dir(test_root_dir):
    return Path(test_root_dir, "test_files")


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


@pytest.fixture(scope="session")
def exe_path(root_dir):
    current_version = importlib_metadata.version("db_temperature_distribution")
    path = Path(root_dir, "dist", f"db-temperature-distribution {current_version}")
    if platform.system() == "Windows":
        path = Path(path.parent, f"{path.name}.exe")
    return path


@pytest.fixture(scope="module")
def test_tempdir(request, test_root_dir):
    name = request.module.__name__
    path = Path(test_root_dir, f"temp-{name}")
    if path.exists():
        shutil.rmtree(path)
    path.mkdir()
    yield path
    shutil.rmtree(path)
