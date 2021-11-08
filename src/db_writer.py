"""Define functions to writer parsed tables to various formats."""
import csv
from pathlib import Path
from typing import List

from db_table import DbTable


class DbWriter:
    """Writes table data to filesystem."""

    @classmethod
    def write_table(cls, table: DbTable, directory: Path) -> Path:
        """
        Write table to given directory, table name is used as file name.

        Arguments
        ---------
        table : DbTable
            Parsed DbTable.
        directory : Path
            A path to directory to place output files.

        Returns
        -------
        list of Path
            Paths of all output files.

        """
        filename = table.name + ".csv"
        path = Path(directory, filename)
        with open(path, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(table.as_2d_table())
        return path

    @classmethod
    def write_tables(cls, tables: List[DbTable], directory: Path) -> List[Path]:
        """
        Write tables as spreadsheet files to a given directory.

        Arguments
        ---------
        tables : List of DbTable
            Parsed DbTables.
        directory : Path
            A path to directory to place output files.

        Returns
        -------
        list of Path
            Paths of all output files.

        """
        output_paths = []
        for table in tables:
            path = cls.write_table(table, directory)
            output_paths.append(path)
        return output_paths
