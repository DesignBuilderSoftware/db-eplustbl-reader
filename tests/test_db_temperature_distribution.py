import csv
from pathlib import Path

import pytest

from main import NoTemperatureDistribution, process_time_bins


def read_csv(path):
    with open(path, "r") as csv_file:
        reader = csv.reader(csv_file)
        return list(reader)


@pytest.fixture(scope="session", autouse=True)
def parse_timebins(html_path, session_tempdir):
    process_time_bins(html_path, session_tempdir)


@pytest.mark.parametrize(
    "filename",
    [
        "Distribution - ZONE MEAN AIR TEMPERATURE.csv",
        "Distribution - ZONE OPERATIVE TEMPERATURE.csv",
        "Distribution - ZONE MEAN RADIANT TEMPERATURE.csv",
    ],
)
def test_parsed_timebins(filename, expected_outputs, session_tempdir):
    filepath = Path(session_tempdir, filename)
    content = read_csv(filepath)
    assert content == expected_outputs[filename]


def test_missing_timebins(html_path_no_bins, session_tempdir):
    with pytest.raises(NoTemperatureDistribution):
        process_time_bins(html_path_no_bins, session_tempdir)


# class TestParser(unittest.TestCase):
#     def setUp(self):
#         tests_dir = os.path.dirname(__file__)
#         self.temp_dir = os.path.join(tests_dir, "temp")
#         self.files_dir = os.path.join(
#             tests_dir, "../../db-temperature-distribution/tests/test_files"
#         )
#         os.mkdir(self.temp_dir)
#         process_time_bins(self.files_dir, self.temp_dir)
#
#     def tearDown(self):
#         shutil.rmtree(self.temp_dir)
#
#     def test_header(self):
#         pass
#
#     def test_values(self):
#         pass
#
#     def test_air_temperature(self):
#         csv_path = os.path.join(
#             self.temp_dir,
#         )
#         csv_content = read_csv(csv_path)
#         print(list(csv_content))
