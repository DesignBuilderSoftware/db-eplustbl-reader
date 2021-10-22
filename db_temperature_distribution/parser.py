import argparse
import csv
import ctypes
import os
import re
import traceback
from collections import OrderedDict, defaultdict

from eppy.results import readhtml


def show_message(title, text):
    """Display native Windows information dialog."""
    ctypes.windll.user32.MessageBoxW(0, text, title, 0)


def read_html(path):
    """Get all tables from given html path."""
    with open(path, "r") as file_handle:
        # use lines_table instead of titletable as lines
        # preceding time bins are needed to apply filtering
        tables = readhtml.lines_table(file_handle)
    return tables


def find_time_bins(html_tables):
    """Extract 'time bins' from all html tables."""
    time_bins = defaultdict(OrderedDict)
    for lines, table in html_tables:
        if lines[0] == "Table of Contents" and lines[4] == "Time Bin Results":
            pattern = re.compile(r"^Report: (.*?) \[C\].*$")
            temperature = pattern.findall(lines[1])[0]
            zone = lines[2][5:]  # drop "For: " prefix
            time_bins[temperature][zone] = table
    return time_bins


def strip_characters(text, *args):
    """Remove specified characters from given text."""
    for char in args:
        text = text.replace(char, "")
    return text


def parse_header_row(time_bin_table):
    """Merge information from interval information rows."""
    header_row = []
    joined_rows = list(zip(time_bin_table[1], time_bin_table[2]))
    n = len(joined_rows)
    for i, (first, second) in enumerate(joined_rows):
        if i == 0:
            # use 'zone' instead of 'Interval Start - Interval End'
            item = "zone"
        elif i == (n - 1):
            # use 'total' instead of 'Total - Row'
            item = "total"
        elif i == 1 or i == (n - 2):
            # first and second from last use text description
            item = "{} {}".format(first, second)
        else:
            # it's clearer to use decimal representation instead of equal signs
            stripped_first = strip_characters(first, " ", "<=")
            stripped_second = strip_characters(second, " ", ">")
            stripped_second = float(stripped_second) - 0.01
            item = "{}-{:.2f}".format(stripped_first, stripped_second)
        header_row.append(item)
    return header_row


def create_header_row(time_bin_tables):
    header_row = None
    for zone_name, table in time_bin_tables.items():
        current_header_row = parse_header_row(table)
        if header_row and header_row != current_header_row:
            raise ValueError("Table headers differ! Cannot generate time bins.")
        else:
            header_row = current_header_row
    return header_row


def create_values_row(zone_name, time_bin_table):
    values_row = time_bin_table[-1]
    values_row[0] = zone_name
    return values_row


def format_time_bins(all_time_bins):
    """Extract only time bin 'totals' (filter irrelevant rows)."""
    formatted_time_bins = {}
    for temperature, time_bins in all_time_bins.items():
        formatted_table = [create_header_row(time_bins)]
        for zone_name, table in time_bins.items():
            values_row = create_values_row(zone_name, table)
            formatted_table.append(values_row)
        formatted_time_bins[temperature] = formatted_table
    return formatted_time_bins


def write_tables(all_time_bins, directory):
    for temperature, time_bins in all_time_bins.items():
        filename = "Distribution - %s.csv" % temperature
        path = os.path.join(directory, filename)
        with open(path, mode="wb") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(time_bins)


def process_time_bins(source_dir, dest_dir):
    html_file = os.path.join(source_dir, "eplustbl.htm")
    html_filename = os.path.basename(html_file)
    try:
        tables = read_html(html_file)
        time_bins_dict = find_time_bins(tables)
        if time_bins_dict:
            formatted_time_bins = format_time_bins(time_bins_dict)
            write_tables(formatted_time_bins, dest_dir)
        else:
            show_message(
                u"Information", u"File '%s' does not include time bins." % html_filename
            )
    except IOError:
        show_message(u"Information", u"%s" % traceback.format_exc())