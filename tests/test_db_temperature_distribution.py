import csv
from pathlib import Path

import pytest

from db_temperature_distribution.parser import (
    NoTemperatureDistribution,
    process_time_bins,
)
from db_temperature_distribution.writer import write_tables


def read_csv(path):
    with open(path, "r") as csv_file:
        reader = csv.reader(csv_file)
        return list(reader)


@pytest.fixture(scope="module", autouse=True)
def parse_timebins(html_path):
    return process_time_bins(html_path)


@pytest.fixture(scope="module", autouse=True)
def write_timebins(parse_timebins, test_tempdir):
    return write_tables(parse_timebins, test_tempdir)


def test_file_paths(write_timebins):
    for path in write_timebins:
        assert path.exists()


@pytest.mark.parametrize(
    "filename",
    [
        "Distribution - ZONE MEAN AIR TEMPERATURE.csv",
        "Distribution - ZONE OPERATIVE TEMPERATURE.csv",
        "Distribution - ZONE MEAN RADIANT TEMPERATURE.csv",
    ],
)
def test_parsed_timebins(filename, expected_outputs, test_tempdir):
    filepath = Path(test_tempdir, filename)
    content = read_csv(filepath)
    assert content == expected_outputs[filename]


def test_missing_timebins(html_path_no_bins):
    with pytest.raises(NoTemperatureDistribution):
        process_time_bins(html_path_no_bins)
