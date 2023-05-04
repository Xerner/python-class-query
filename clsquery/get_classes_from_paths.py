import os
from glob import glob
from pathlib import Path
from typing import List
from clsquery.classes.class_query_item import ClassQueryItem
from clsquery.constants import AVOID_TAG_STR
from clsquery.get_classes_at_path import get_classes_in_module
from clsquery.format_list import format_list
from clsquery.custom_logger import logger


def get_classes_from_paths(file_or_dir_paths: List[str], 
                           supertype_filter: List[str] = [], 
                           tag_filter: List[str] = [],
                           avoid_tag_str = AVOID_TAG_STR,
                           recursive=False):
    # https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly
    # https://stackoverflow.com/questions/3178285/list-classes-in-directory-python
    def find_and_extend_classes(classes: List[ClassQueryItem], file_or_dir_path: str, type_filter: List[str], tag_filter: List[str] = [], avoid_tag_str = AVOID_TAG_STR):
        query_result = get_classes_in_module(file_or_dir_path, type_filter, tag_filter, avoid_tag_str)
        for query_item in query_result:
            if query_item in classes:
                continue
            classes.append(query_item)

        if len(query_result) == 0:
            log_func = logger.warning # used to be a warning
        else:
            log_func = logger.info # used to be a success
        
        if len(query_result) == 1:
            log_func(f"Fetched {len(query_result)} class from {file_or_dir_path}")
        else:
            log_func(f"Fetched {len(query_result)} classes from {file_or_dir_path}")
        if len(query_result) > 0:
            long_format = len(query_result) > 1
            logger.info(f"Classes fetched: " + format_list([item.cls.__name__ for item in query_result], is_long_format=long_format))
    
    classes: List[ClassQueryItem] = []

    logger.info("Fetching classes...")
    logger.info("Paths to search:  " + format_list(file_or_dir_paths, is_long_format=True))
    logger.info("Recursive:        " + str(recursive))
    logger.info("Supertype filter: " + format_list(supertype_filter))
    logger.info("Tag filter:       " + format_list(tag_filter))

    for file_or_dir_path in file_or_dir_paths:
        path = Path(os.path.expandvars(file_or_dir_path))
        
        file_or_dir_path = os.path.expandvars(file_or_dir_path)
        if path.is_dir():
            # recursive search
            # https://stackoverflow.com/questions/50714469/recursively-iterate-through-all-subdirectories-using-pathlib
            for file_path in path.glob("*.py"):
                find_and_extend_classes(classes, file_path, supertype_filter, tag_filter, avoid_tag_str)
            
            if recursive:
                for recursive_path in path.glob('**/*'):
                    if recursive_path.is_dir():
                        for file_path in recursive_path.glob("*.py"):
                            find_and_extend_classes(classes, file_path, supertype_filter, tag_filter, avoid_tag_str)
        elif os.path.isfile(file_or_dir_path):
            find_and_extend_classes(classes, file_or_dir_path, supertype_filter, tag_filter, avoid_tag_str)
        else:
            raise FileNotFoundError(file_or_dir_path)

    classes.sort(key=lambda item: item.cls.__name__)
    class_names = [item.cls.__name__ for item in classes]
    if len(classes) == 0:
        logger.warning("No classes fetched: " + format_list(class_names)) # was a warning
    else:
        logger.info("All classes fetched: " + format_list(class_names))
    return classes
