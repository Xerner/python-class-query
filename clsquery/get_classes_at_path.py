import inspect
import importlib
import sys
import os
from typing import List
from clsquery.has_supertype import has_supertype
from clsquery.classes.class_query_item import ClassQueryItem
from clsquery.constants import AVOID_TAG_STR


def get_classes_in_module(module_path: str, supertypes: List[str] = [], tag_filter: List[str] = [], avoid_tag_str = AVOID_TAG_STR) -> List[ClassQueryItem]:
    def should_avoid_tag(tag: str, avoid_tag_str) -> bool:
        return tag[0] == avoid_tag_str
    
    def remove_avoid_tag_str(tag: str):
        if should_avoid_tag(tag):
            return tag[1:]
        
    def filter_classes(cls: object, supertypes: List[str] = [], tag_filter: List[str] = []):
        if not inspect.isclass(cls) or cls.__module__ != module_name:
            return False

        has_tag = True
        if tag_filter is not None and len(tag_filter) > 0:
            has_tag = False
            if hasattr(cls, "tags"):
                for tag in tag_filter:
                    if should_avoid_tag(tag, avoid_tag_str):
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
    
    module_name = os.path.splitext(os.path.basename(module_path))[0]
    spec = importlib.util.spec_from_file_location(module_name,module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    classes: List[ClassQueryItem] = []
    for _, cls in inspect.getmembers(module, lambda cls: filter_classes(cls, supertypes, tag_filter)):
        classes.append(ClassQueryItem(cls, module_path))
    return classes
