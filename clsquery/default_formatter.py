from typing import List
from clsquery.classes.search_metadata import SearchMetadata
from clsquery.format_table import format_table
from clsquery.convert_classes_to_table import convert_classes_to_table

def default_formatter(classes: list, attributes_to_print: List[str], indent: int, metadata: SearchMetadata):
    return format_table(convert_classes_to_table(classes, attributes_to_print), indent)
