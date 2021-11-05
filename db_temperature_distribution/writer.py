"""Define functions to writer parsed tables to various formats."""
import csv
from pathlib import Path
from typing import Dict, List

from db_temperature_distribution.parser import Table


def write_tables(all_time_bins: Dict[str, Table], directory: Path) -> List[Path]:
    """
    Write time bins to a given directory.

    Arguments
    ---------
    all_time_bins : Dict of {str, Table}
        Parsed time bins for all temperature ypes.
    directory : Path
        A path to directory to place output file / files.

    Returns
    -------
    list of Path
        Paths of all output files.

    """
    output_paths = []
    for temperature, time_bins in all_time_bins.items():
        filename = f"Distribution - {temperature}.csv"
        path = Path(directory, filename)
        with open(path, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(time_bins)
        output_paths.append(path)
    return output_paths
