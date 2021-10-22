import argparse
import os

from db_temperature_distribution.parser import process_time_bins

if __name__ == '__main__':
    energyplus_folder = os.path.expandvars(r"%LOCALAPPDATA%\DesignBuilder\EnergyPlus")
    parser = argparse.ArgumentParser(
        description="Read energyplus html output and export time bin tables."
    )
    parser.add_argument(
        "--source-dir",
        "-i",
        type=str,
        help="Source directory containing 'eplustbl.htm' file.",
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
    process_time_bins(args.source_dir, args.dest_dir)
