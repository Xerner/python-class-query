
def format_list(list_: list, is_long_format = False, level=1, trailing_new_line = True) -> str:
    if list_ is None:
        return "None"
    if len(list_) == 0:
        return "Empty list"
    else:
        if is_long_format:
            new_line = "\n" if trailing_new_line else ""
            return "\n" + "\n".join([("-"*level)+" " + str(item) for item in list_]) + new_line
        else:
            return ", ".join(str(item) for item in list_)
