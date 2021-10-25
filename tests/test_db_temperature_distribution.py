import csv
from pathlib import Path

import pytest

from main import NoTemperatureDistribution, process_time_bins


def read_csv(path):
    with open(path, "r") as csv_file:
        reader = csv.reader(csv_file)
        return list(reader)


@pytest.fixture(scope="module", autouse=True)
def parse_timebins(html_path, test_tempdir):
    process_time_bins(html_path, test_tempdir)


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


def test_missing_timebins(html_path_no_bins, test_tempdir):
    with pytest.raises(NoTemperatureDistribution):
        process_time_bins(html_path_no_bins, test_tempdir)
