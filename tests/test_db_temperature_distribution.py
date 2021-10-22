import csv
import os
import shutil
import unittest

from main import process_time_bins


def read_csv(path):
    with open(path, "rb") as csv_file:
        reader = csv.reader(csv_file)
        return list(reader)


class TestParser(unittest.TestCase):
    def setUp(self):
        tests_dir = os.path.dirname(__file__)
        self.temp_dir = os.path.join(tests_dir, "temp")
        self.files_dir = os.path.join(tests_dir, "../../db-temperature-distribution/tests/test_files")
        os.mkdir(self.temp_dir)
        process_time_bins(self.files_dir, self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_header(self):
        pass

    def test_values(self):
        pass

    def test_air_temperature(self):
        csv_path = os.path.join(self.temp_dir, "Distribution - ZONE MEAN AIR TEMPERATURE.csv")
        csv_content = read_csv(csv_path)
        print(list(csv_content))
