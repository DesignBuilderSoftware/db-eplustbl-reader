"""Define functions to extract and parse EnergyPlus temperature distribution."""


import csv
import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Union

from eppy.results import readhtml


class NoTemperatureDistribution(Exception):
    """Raised when input html file does not include time bins."""


Table = List[List[Union[str, float]]]


def read_html(path: Path) -> List[List[Any]]:
    """Get all tables from given html path."""
    with open(path, "r", encoding="utf-8") as file_handle:
        # use lines_table instead of titletable as lines
        # preceding time bins are needed to apply filtering
        tables = readhtml.lines_table(file_handle)
    return tables


def find_time_bins(html_tables: List[List[Any]]) -> Dict[str, Dict[str, Table]]:
    """Extract 'time bins' from all html tables."""
    time_bins = defaultdict(dict)
    for lines, table in html_tables:
        if lines[0] == "Table of Contents" and lines[4] == "Time Bin Results":
            pattern = re.compile(r"^Report: (.*?) \[C\].*$")
            temperature = pattern.findall(lines[1])[0]
            zone = lines[2][5:]  # drop "For: " prefix
            time_bins[temperature][zone] = table
    return time_bins


def strip_characters(text: str, *args: str):
    """Remove specified characters from given text."""
    for char in args:
        text = text.replace(char, "")
    return text


def parse_header_row(time_bin_table):
    """Merge information from interval information rows."""
    header_row = []
    joined_rows = list(zip(time_bin_table[1], time_bin_table[2]))
    n_rows = len(joined_rows)
    for i, (first, second) in enumerate(joined_rows):
        if i == 0:
            # use 'zone' instead of 'Interval Start - Interval End'
            item = "zone"
        elif i == (n_rows - 1):
            # use 'total' instead of 'Total - Row'
            item = "total"
        elif i in (1, n_rows - 2):
            # first and second from last use text description
            item = f"{first} {second}"
        else:
            # it's clearer to use decimal representation instead of equal signs
            stripped_first = strip_characters(first, " ", "<=")
            stripped_second = strip_characters(second, " ", ">")
            stripped_second = float(stripped_second) - 0.01
            item = f"{stripped_first}-{stripped_second:.2f}"
        header_row.append(item)
    return header_row


def create_header_row(time_bin_tables: Dict[str, Table]) -> List[str]:
    """Create formatted first spreadsheet row."""
    header_row = None
    for _, table in time_bin_tables.items():
        current_header_row = parse_header_row(table)
        if header_row and header_row != current_header_row:
            raise ValueError("Table headers differ! Cannot generate time bins.")
        header_row = current_header_row
    return header_row


def create_values_row(zone_name: str, time_bin_table: Table) -> List[Union[str, float]]:
    """Create spreadsheet values row."""
    values_row = time_bin_table[-1]
    values_row[0] = zone_name
    return values_row


def format_time_bins(all_time_bins: Dict[str, Dict[str, Table]]) -> Dict[str, Table]:
    """Extract only time bin 'totals' (filter irrelevant rows)."""
    formatted_time_bins = {}
    for temperature, time_bins in all_time_bins.items():
        formatted_table = [create_header_row(time_bins)]
        for zone_name, table in time_bins.items():
            values_row = create_values_row(zone_name, table)
            formatted_table.append(values_row)
        formatted_time_bins[temperature] = formatted_table
    return formatted_time_bins


def write_tables(all_time_bins: Dict[str, Table], directory: Path) -> None:
    """Write time bins to a given directory."""
    for temperature, time_bins in all_time_bins.items():
        filename = f"Distribution - {temperature}.csv"
        path = Path(directory, filename)
        with open(path, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(time_bins)


def process_time_bins(html_path: Path, destination_dir: Path) -> None:
    """
    Read source html file and write parsed time bins to .csv.

    Arguments
    ---------
    html_path : Path
        A path to energyplus html summary file.
    destination_dir : Path
        A path to directory to place output file / files.

    """
    tables = read_html(html_path)
    time_bins_dict = find_time_bins(tables)
    if time_bins_dict:
        formatted_time_bins = format_time_bins(time_bins_dict)
        write_tables(formatted_time_bins, destination_dir)
    else:
        raise NoTemperatureDistribution
