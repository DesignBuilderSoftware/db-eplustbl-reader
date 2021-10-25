import argparse
import ctypes
import os
import traceback
from pathlib import Path

from db_temperature_distribution.parser import (
    NoTemperatureDistribution,
    process_time_bins,
)


def show_message(title: str, text: str) -> None:
    """Display native Windows information dialog."""
    ctypes.windll.user32.MessageBoxW(0, text, title, 0)


if __name__ == "__main__":
    energyplus_folder = os.path.expandvars(r"%LOCALAPPDATA%\DesignBuilder\EnergyPlus")
    parser = argparse.ArgumentParser(
        description="Read energyplus html output and export time bin tables."
    )
    parser.add_argument(
        "--source-path",
        "-i",
        type=str,
        help="A path to energyplus .htm summary file.",
        required=False,
        default=energyplus_folder,
        nargs="?",
    )
    parser.add_argument(
        "--dest-dir",
        "-o",
        type=str,
        help="Destination directory to store parsed tables.",
        required=False,
        default=energyplus_folder,
        nargs="?",
    )
    args = parser.parse_args()
    html_path = Path(args.source_path)
    try:
        process_time_bins(html_path, Path(args.dest_dir))
    except IOError:
        show_message("Information", traceback.format_exc())
    except NoTemperatureDistribution:
        show_message(
            "Information",
            f"File '{html_path}' does not include temperature distribution time bins.",
        )
