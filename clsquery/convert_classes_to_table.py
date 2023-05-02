from typing import List

def convert_classes_to_table(classes: list, attributes_to_print: List[str]):
    table = []
    table.append(attributes_to_print)
    for class_ in classes:
        row = []
        for attribute_path in attributes_to_print:
            attribute = class_
            for attribute_key in attribute_path.split("."):
                if not hasattr(attribute, attribute_key):
                    raise AttributeError(f"'{class_}' does not have the attribute '{attribute_path}'")
                attribute = getattr(attribute, attribute_key)
            row.append(str(attribute))
        table.append(row)
    return table
