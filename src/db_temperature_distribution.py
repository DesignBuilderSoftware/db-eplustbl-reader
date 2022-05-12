"""Define functions to extract and parse EnergyPlus temperature distribution."""
import os
import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List

from eppy.results import readhtml

from db_logger import Logger
from db_table import DbTable, RawTable
from db_writer import DbWriter


class NoTemperatureDistribution(Exception):
    """Raised when input html file does not include time bins."""


def read_html(path: Path) -> List[List[Any]]:
    """Get all tables from given html path."""
    with open(path, "r", encoding="utf-8") as file_handle:
        # use lines_table instead of titletable as lines
        # preceding time bins are needed to apply filtering
        tables = readhtml.lines_table(file_handle)
    return tables


def find_time_bins(html_tables: List[List[Any]]) -> Dict[str, Dict[str, RawTable]]:
    """Extract 'time bins' from all html tables."""
    time_bins = defaultdict(dict)
    for lines, table in html_tables:
        if lines[0] == "Table of Contents" and lines[4] == "Time Bin Results":
            pattern = re.compile(r"^Report: (.*?) \[C\].*$")
            temperature = pattern.findall(lines[1])[0]
            zone = lines[2][5:]  # drop "For: " prefix
            time_bins[temperature][zone] = table
    return time_bins


def strip_characters(text: str, *args: str) -> str:
    """Remove specified characters from given text."""
    for char in args:
        text = text.replace(char, "")
    return text


def parse_header_row(time_bin_table: RawTable) -> List[str]:
    """Merge information from interval information rows."""
    header_row = []
    joined_rows = list(zip(time_bin_table[1], time_bin_table[2]))
    n_rows = len(joined_rows)
    for i, (first, second) in enumerate(joined_rows):
        if i == 0:
            # skip first item as this is in place in index
            continue
        if i == (n_rows - 1):
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


def create_header_row(time_bin_tables: Dict[str, RawTable]) -> List[str]:
    """Create formatted first spreadsheet row."""
    header_row = None
    for _, raw_table in time_bin_tables.items():
        current_header_row = parse_header_row(raw_table)
        if header_row and header_row != current_header_row:
            raise ValueError("Table headers differ! Cannot generate time bins.")
        header_row = current_header_row
    return header_row


def create_values_row(time_bin_table: RawTable) -> List[float]:
    """Create spreadsheet values row."""
    values_row = time_bin_table[-1]
    return values_row[1:]


def format_time_bins(raw_time_bins: Dict[str, Dict[str, RawTable]]) -> List[DbTable]:
    """Extract only time bin 'totals' (filter irrelevant rows)."""
    formatted_time_bins = []
    for temperature, time_bins in raw_time_bins.items():
        db_table = DbTable(f"Distribution {temperature}")
        db_table.header = create_header_row(time_bins)
        for table in time_bins.values():
            values_row = create_values_row(table)
            db_table.append_row(values_row)
        db_table.index = list(time_bins.keys())
        formatted_time_bins.append(db_table)
    return formatted_time_bins


def process_time_bins(html_path: Path) -> List[DbTable]:
    """
    Read source html file and write parsed time bins to .csv.

    Arguments
    ---------
    html_path : Path
        A path to energyplus html summary file.

    Returns
    -------
    list of DbTable
        Processed time bins for all temperature types.

    """
    tables = read_html(html_path)
    time_bins_dict = find_time_bins(tables)
    if time_bins_dict:
        return format_time_bins(time_bins_dict)
    raise NoTemperatureDistribution(
        f"File '{html_path}' does not include temperature distribution time bins."
    )


if __name__ == "__main__":
    energyplus_folder = Path(
        os.path.expandvars(r"%LOCALAPPDATA%\DesignBuilder\EnergyPlus")
    )
    default_html = Path(energyplus_folder, "eplustbl.htm")
    with Logger(show_dialogs=True) as logger:
        parsed_time_bins = process_time_bins(default_html)
        DbWriter.write_tables(parsed_time_bins, energyplus_folder)
        table_names = "\n - ".join([table.name for table in parsed_time_bins])
        logger.print_message(
            "Success!",
            f"Bins successfully extracted."
            f"\nOutput files:\n - {table_names}"
            f"\nare located in: {energyplus_folder}.",
        )
