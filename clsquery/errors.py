

class DuplicateClassError(Exception):
    def __init__(self, class_: object, original_filepath:str, duplicate_filepath: str) -> None:
        message = f"""While fetching classes, a duplicate class {class_.__name__} was found at {duplicate_filepath}. First copy found at {original_filepath}

Are all file and directory paths correct in the provided test agenda JSON?"""
        super().__init__(message)
