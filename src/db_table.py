"""Contains simple table class."""

from typing import Any, List


class ShapeMismatch(Exception):
    """Raised when added row length does not match number of columns.."""


RawTable = List[List[Any]]


class DbTable:
    """
    Represents simple two dimensional table.

    Number of columns needs to be uniform.

    """

    def __init__(self, name: str):
        self.name = name
        self._rows = []
        self._n_columns = 0
        self._header = None
        self._index = None

    @property
    def n_rows(self) -> int:
        """Number of rows."""
        return len(self._rows)

    @property
    def n_columns(self) -> int:
        """Number of columns."""
        return self._n_columns

    @property
    def header(self) -> List[str]:
        """Header data."""
        return self._header if self._header else range(self.n_columns)

    @header.setter
    def header(self, items: List[str]) -> None:
        """Sets header data."""
        self._verify_x(items)
        self._header = items

    @property
    def index(self) -> List[Any]:
        """Table index."""
        return self._index if self._index else range(self.n_rows)

    @index.setter
    def index(self, items: List[Any]) -> None:
        """Sets table index."""
        self._verify_y(items)
        self._index = items

    @property
    def rows(self) -> List[Any]:
        """Values (without header and index)."""
        return self._rows

    def as_2d_table(self) -> List[List[Any]]:
        """Get table as a simple nested list, includes header and index."""
        table = [[""] + self.header]
        for i, row in enumerate(self.rows):
            table.append([self.index[i]] + row)
        return table

    def _verify_x(self, row: List[Any]) -> None:
        """Check if number of items matches number of columns."""
        if self.n_columns > 0 and self._n_columns != len(row):
            raise ShapeMismatch(
                f"Cannot add row, number of items ({len(row)}) does "
                f"not match number of columns ({self._n_columns})"
            )
        self._n_columns = len(row)

    def _verify_y(self, column: List[Any]) -> None:
        """Check if number of items matches number of rows."""
        if self.n_rows != len(column):
            raise ShapeMismatch(
                f"Cannot add column, number of items ({len(column)}) does "
                f"not match number of rows ({self.n_rows})"
            )

    def append_row(self, row: List[Any]) -> None:
        """Append row, checks if column number matches."""
        self._verify_x(row)
        self._rows.append(row)
