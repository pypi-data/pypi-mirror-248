import json
import csv
import sys

import jmespath
from rich import print_json as print_json_rich
from rich import print
from rich.table import Table

from githubctl.constants import PrintFormatOptions


def filter_list_of_dicts(list_of_dict, query) -> list:
    """
    Filter list of dict by query with jmespath
    """
    try:
        _query = jmespath.parser.Parser().parse(query)
        if _query.parsed["type"] != "filter_projection":
            print(f"Invalid query: {query}")
            return
    except jmespath.exceptions.JMESPathSyntaxError:
        print(f"Invalid query: {query}")
        return
    return _query.search(list_of_dict)


def sort_list_of_dicts(list_of_dict, key: str) -> list:
    """
    Sort list of dict by key, key format: key1,key2,key3
    """
    reverse = False
    if key.startswith("~"):
        reverse = True
        key = key[1:]
    keys = key.split(",")
    try:
        sorted_list = sorted(
            list_of_dict, key=lambda x: tuple(x[k] for k in keys), reverse=reverse
        )
    except:
        print(f"Invalid sort key: {key}")
        return
    return sorted_list


def print_json(json_data):
    print_json_rich(json.dumps(json_data))


def print_beauty(
    list_of_dict,
    output=PrintFormatOptions.table,
    table_columns=[],
    row_index=True,
) -> None:
    if output == PrintFormatOptions.json:
        print_json(list_of_dict)
        return

    if output == PrintFormatOptions.csv:
        if not table_columns:
            table_columns = list_of_dict[0].keys()
        writer = csv.DictWriter(
            sys.stdout, fieldnames=table_columns, extrasaction="ignore"
        )
        writer.writeheader()
        writer.writerows(list_of_dict)

        return

    # for table
    table = Table(show_header=True, header_style="bold magenta")

    # add column name
    if row_index:
        table.add_column("")
    if not table_columns:
        table_columns = list_of_dict[0].keys()

    for k in table_columns:
        table.add_column(str(k))

    # add rows
    if row_index:
        for row in list_of_dict:
            table.add_row(
                *[str(list_of_dict.index(row) + 1)]
                + [str(v) for v in [row.get(k, "") for k in table_columns]]
            )
    else:
        for row in list_of_dict:
            table.add_row(*[str(v) for v in [row.get(k, "") for k in table_columns]])

    print(table)
