from enum import Enum


class PrintFormatOptions(str, Enum):
    table = "table"
    json = "json"
    csv = "csv"
