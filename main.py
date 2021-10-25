import argparse
import os
from pathlib import Path

from db_temperature_distribution.logger import Logger
from db_temperature_distribution.parser import process_time_bins

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
        default=os.path.join(energyplus_folder, "eplustbl.html"),
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
    parser.add_argument(
        "--no-dialogs",
        help="Suppress error dialog windows.",
        action="store_true",
        default=False,
    )
    args = parser.parse_args()
    html_path = Path(args.source_path)
    with Logger(show_dialogs=not args.no_dialogs) as logger:
        process_time_bins(html_path, Path(args.dest_dir))
        logger.print_message("Success!", "")
