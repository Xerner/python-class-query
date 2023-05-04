from typing import List, Union
from clsquery.classes.class_query_results import ClassQueryResults
from clsquery.classes.class_query_item import ClassQueryItem
from clsquery.format_table import format_table
from clsquery.format_list import format_list
from clsquery.get_time import get_time
from clsquery.convert_classes_to_table import convert_classes_to_table

def default_formatter(results: ClassQueryResults, indent: int):
    def flat_formatting(query_items: List[ClassQueryItem], attributes: List[str], indent: int):
        classes = [item.cls for item in query_items]
        return format_table(convert_classes_to_table(classes, attributes), indent)

    def grouped_formatting(classes_or_groups: Union[List[ClassQueryItem], dict], attributes: List[str], indent: int):
        if type(classes_or_groups) == list:
            return flat_formatting(classes_or_groups, attributes, indent=indent) + "\n"
        str_ = ""
        for group in classes_or_groups:
            str_ += ("\t"*indent) + group + "\n\n" + grouped_formatting(classes_or_groups[group], attributes, indent=indent+1)
        return str_

    is_grouped = results.groups is not None and type(results.groups) != list and results.query.group_by is not None and len(results.query.group_by) != 0
    lines = []
    lines.append("Logging results with default formatter")
    lines.append("")
    lines.append("Search Results")
    lines.append("---------------")
    lines.append("")
    lines.append("{: <20}{}".format("Date", get_time()))
    lines.append("{: <20}{}".format("Paths", format_list(results.query.paths, is_long_format=True)))
    lines.append("{: <20}{}".format("Recursive", str(results.query.recursive)))
    lines.append("{: <20}{}".format("Supertypes filter", format_list(results.query.supertypes)))
    lines.append("{: <20}{}".format("Tag filter", format_list(results.query.tags)))
    if results.query.group_by is not None:
        lines.append(f"Grouped by:        {format_list(results.query.group_by)}")
    lines.append("")

    # grouped formatting
    if is_grouped:
        lines.append(grouped_formatting(results.groups, results.query.attributes, indent))
    # normal formatting
    else:
        lines.append(flat_formatting(results.classes, results.query.attributes, indent))

    return "\n".join(lines)
