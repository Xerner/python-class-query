import os
import inspect
import importlib
import sys
from glob import glob
from typing import List
from clsquery.errors import DuplicateClassError
from clsquery.has_supertype import has_supertype


AVOID_TAG_STR = "_"
"""The string used when trying to specify what tags to AVOID using the get_classes_from_paths function"""


def get_classes_from_paths(file_or_dir_paths: List[str], supertype_filter: List[str] = [], tag_filter: List[str] = [], avoid_tag_str = AVOID_TAG_STR):
    # https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly
    # https://stackoverflow.com/questions/3178285/list-classes-in-directory-python
    
    classes = {} # maps class name -> source filepath

    def remove_avoid_tag_str(tag: str):
        if should_avoid_tag(tag):
            return tag[1:]

    def should_avoid_tag(tag: str) -> bool:
        return tag[0] == avoid_tag_str

    def find_classes(path: str, supertypes: List[str] = [], tag_filter: List[str] = []) -> dict:
        def filter_classes(cls: object, supertypes: List[str] = [], tag_filter: List[str] = []):
            if not inspect.isclass(cls) or cls.__module__ != name:
                return False

            has_tag = True
            if tag_filter is not None and len(tag_filter) > 0:
                has_tag = False
                if hasattr(cls, "tags"):
                    for tag in tag_filter:
                        if should_avoid_tag(tag):
                            if remove_avoid_tag_str(tag) in cls.tags:
                                return False
                            else:
                                has_tag = True
                        else:
                            if tag in cls.tags:
                                has_tag = True
                                break
                            else:
                                has_tag = False

            if supertypes is None or len(supertypes) == 0:
                valid_supertype = True
            else:
                valid_supertype = any([has_supertype(cls, supertype) for supertype in supertypes])

            return has_tag and valid_supertype
        
        name = os.path.splitext(os.path.basename(path))[0]
        spec = importlib.util.spec_from_file_location(name,path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        classes = {} # maps class name -> source filepath
        for _, cls in inspect.getmembers(module, lambda cls: filter_classes(cls, supertypes, tag_filter)):
            classes[cls] = path
        return classes

    def find_and_extend_classes(classes: dict, file_or_dir_path: str, type_filter: List[str], tag_filter: List[str] = []):
        search_results = find_classes(file_or_dir_path, type_filter, tag_filter)
        for class_ in search_results:
            if class_ in classes:
                raise DuplicateClassError(class_, classes[class_], search_results[class_])
            else:
                # maps class name -> source filepath
                # search_results[class_] = source filepath
                classes[class_] = search_results[class_]
        if len(classes) == 0:
            log_func = print # used to be a warning
        else:
            log_func = print # used to be a success
        
        if len(search_results) == 1:
            log_func(f"Fetched {len(search_results)} class from {file_or_dir_path}")
        else:
            log_func(f"Fetched {len(search_results)} classes from {file_or_dir_path}")
    
    print("Fetching classes...")
    print("Paths to search:  " + str(file_or_dir_paths))
    print("Supertype filter: " + str(supertype_filter))
    print("Tag filter:       " + str(tag_filter))

    for file_or_dir_path in file_or_dir_paths:
        file_or_dir_path = os.path.expandvars(file_or_dir_path)
        if os.path.isdir(file_or_dir_path):
            for file_path in glob(os.path.join(file_or_dir_path, "*.py")):
                find_and_extend_classes(classes, file_path, supertype_filter, tag_filter)
        elif os.path.isfile(file_or_dir_path):
            find_and_extend_classes(classes, file_or_dir_path, supertype_filter, tag_filter)
        else:
            raise FileNotFoundError(file_or_dir_path)

    classes = list(classes)
    classes.sort(key=lambda cls: cls.__name__)
    if len(classes) == 0:
        print("No classes fetched: " + str([class_.__name__ for class_ in classes])) # was a warning
    else:
        print("All classes fetched: " + str([class_.__name__ for class_ in classes]))
    return classes
