import csv
import json
from pathlib import Path

import pytest

from db_temperature_distribution import NoTemperatureDistribution, process_time_bins
from src.db_writer import DbWriter


def read_csv(path):
    with open(path, "r") as csv_file:
        reader = csv.reader(csv_file)
        return list(reader)


@pytest.fixture(scope="session")
def expected_outputs(test_files_dir):
    with open(Path(test_files_dir, "expected_outputs.json")) as json_file:
        content = json.load(json_file)
    return content


@pytest.fixture(scope="module", autouse=True)
def parse_timebins(html_path):
    return process_time_bins(html_path)


@pytest.fixture(scope="module", autouse=True)
def write_timebins(parse_timebins, test_tempdir):
    return DbWriter.write_tables(parse_timebins, test_tempdir)


def test_file_paths(write_timebins):
    for path in write_timebins:
        assert path.exists()


@pytest.mark.parametrize(
    "filename",
    [
        "Distribution ZONE MEAN AIR TEMPERATURE.csv",
        "Distribution ZONE OPERATIVE TEMPERATURE.csv",
        "Distribution ZONE MEAN RADIANT TEMPERATURE.csv",
    ],
)
def test_parsed_timebins(filename, expected_outputs, test_tempdir):
    filepath = Path(test_tempdir, filename)
    content = read_csv(filepath)
    assert content == expected_outputs[filename]


def test_missing_timebins(html_path_no_bins):
    with pytest.raises(NoTemperatureDistribution):
        process_time_bins(html_path_no_bins)
