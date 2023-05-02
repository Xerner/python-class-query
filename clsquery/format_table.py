
def format_table(values: list, indent = 0, margin = 4, has_headers = True) -> str:
    table = []
    if len(values) == 0:
        return "No values"
    format_str = []
    for row in values:
        if type(row) == tuple:
            row = list(row)
        if type(row) == list and len(row) > len(format_str):
            format_str = [0] * len(row)
        row_str = []
        for i, value in enumerate(row):
            value = str(value)
            row_str.append(value)
            if len(value) + margin > format_str[i]:
                format_str[i] = len(value) + margin
        table.append(row_str)
    total_len = sum(format_str)
    format_str = list(map(lambda x: '{:<'+str(x)+"}", format_str))
    format_str = "\t"*indent + " ".join(format_str)
    total_str = ""
    for i, row_str in enumerate(table):
        total_str += format_str.format(*row_str) + "\n"
        if has_headers and i == 0:
            total_str += "\t"*indent + "-"*total_len + "\n"
    return total_str
