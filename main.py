import argparse
import json
import sys
from pathlib import Path
from types import FunctionType
from typing import List
from clsquery import *

LIST_COMMAND_PRESETS = {}

NULL_GROUP = "No Group"

def main(file_or_dir_paths: List[str] = None, 
         supertypes: List[str] = None, 
         tags: List[str] = None, 
         attributes_to_print: List[str] = None, 
         group_by_attr: str = None, 
         load_preset: str = None,
         formatter = default_formatter):
    """
    run 'main.py list -h' for the usual help message

    This function supports loading different default parameters from a json file
    
    `formatter` is not supported in the command line. It can only be changed if loading the parameters from a preset, 
    or if this function is called directly in a Python script
    """

    def normal_print(classes, attributes_to_print: List[str], formatter: FunctionType, metadata: str):
        print(formatter(classes, attributes_to_print, indent=0, metadata=metadata))
    
    def grouped_print(classes, attributes_to_print: List[str], group_by_attributes: str, formatter: FunctionType, metadata: str):
        def get_group_by_attr_value(class_, attributes: list):
            if len(attributes) == 0:
                return class_
            attribute = attributes.pop(0)
            if not hasattr(class_, attribute):
                return NULL_GROUP
                # raise AttributeError(f"Tried to group by {group_by_attr}. {class_} does not have the attribute {attribute}")
        
            return get_group_by_attr_value(getattr(class_, attribute), attributes)

        root_group = {}
        def fill_groups(class_, groups, attributes, attributes_index = 0):
            group_key = str(get_group_by_attr_value(class_, attributes[attributes_index].split(".")))
            if group_key == NULL_GROUP or attributes_index == len(attributes) - 1:
                if group_key not in groups:
                    groups[group_key] = []
                groups[group_key].append(class_)
                return
            if group_key not in groups:
                groups[group_key] = {}
            fill_groups(class_, groups[group_key], attributes, attributes_index+1)

        for class_ in classes:
            fill_groups(class_, root_group, group_by_attributes)

        def print_groups(classes_or_groups, attributes_to_print, indent, metadata):
            if type(classes_or_groups) == list:
                return formatter(classes_or_groups, attributes_to_print, indent=indent, metadata=metadata) + "\n"
            str_ = ""
            for group in classes_or_groups:
                str_ += ("\t"*indent) + group + "\n\n" + print_groups(classes_or_groups[group], attributes_to_print, indent=indent+1, metadata=metadata)
            return str_
        
        print(print_groups(root_group, attributes_to_print, 0, metadata))
    
    def init_param(value, preset_options_key: str, default_value = None):
        if value is not None:
            return value
        if preset_params is not None:
            default = preset_params.get(preset_options_key)
            logger.info(f"Using default value for '{preset_options_key}' option: {default}")
            return default
        if default_value is not None:
            return default_value
        return None
    
    preset_params = None
    no_args_given = file_or_dir_paths is None and supertypes is None and tags is None and attributes_to_print is None and group_by_attr is None
    if load_preset is None and no_args_given:
        load_preset = "default"
    if load_preset is not None:
        preset_json_path = LIST_COMMAND_PRESETS[load_preset]
        logger.info("Loading parameters from " + preset_json_path)
        with open(preset_json_path) as params:
            preset_params: dict = json.load(params)

    file_or_dir_paths =   init_param(file_or_dir_paths,   "paths")
    supertypes =          init_param(supertypes,          "supertypes")
    tags =                init_param(tags,                "tags")
    attributes_to_print = init_param(attributes_to_print, "attributes", ["__name__"])
    group_by_attr =       init_param(group_by_attr,       "group-by")
    formatter =           init_param(formatter,           "formatter")
    if formatter is None:
        formatter = default_formatter

    classes = get_classes_from_paths(file_or_dir_paths, supertypes, tags)
    
    print()
    print("Search Results")
    print("---------------")
    print()
    doc_gen_metadata = SearchMetadata(file_or_dir_paths, supertypes, tags, group_by_attr)
    print(doc_gen_metadata.metadata)
    print()

    if group_by_attr is None or len(group_by_attr) == 0:
        normal_print(classes, attributes_to_print, formatter, doc_gen_metadata)
    else:
        grouped_print(classes, attributes_to_print, group_by_attr, formatter, doc_gen_metadata)

    print()

def main_cli():
    usage = f"""python {Path(__file__).name} --path STRING

A search command for Python classes

"""
    presets = list(LIST_COMMAND_PRESETS.keys())
    presets.sort()
    presets_str = "\n    ".join(presets)
    epilog = f"""
Presets Available
    {presets_str}

Options provided on the command line will override options loaded by a preset
"""
    parser = argparse.ArgumentParser(usage=usage, epilog=epilog, formatter_class=argparse.RawDescriptionHelpFormatter)
    mutex = parser.add_mutually_exclusive_group(required=True)
    mutex.add_argument('-p', '--paths', metavar="STRING", type=str, nargs="*", help='directory path or filepath to the classes to generate docs for')
    parser.add_argument('-t', '--tags', metavar="STRING", type=str, nargs="*", help=f"the tags to look for when including classes. A class must have a 'tags' attribute for this to work. Prefix tags with '{AVOID_TAG_STR}' to specify they should NOT be included")
    parser.add_argument('-s', '--supertypes', metavar="STRING", type=str, nargs="*", help="The supertypes to look for when including classes")
    parser.add_argument('-a', '--attributes', metavar="STRING", type=str, nargs="*", help="What attributes of the class to return")
    # parser.add_argument('-g', '--group-by', metavar="STRING", type=str, nargs="?", default="", const="", help="What attribute to group the classes by")
    parser.add_argument('-g', '--group-by', metavar="STRING", type=str, nargs="*", help="What attribute to group the classes by")
    mutex.add_argument('-l', '--load-preset', metavar="PRESET", type=str, help="load a preset list of args. See src/utility/list_command_presets")
    args = parser.parse_args()
    
    main(args.paths, args.supertypes, args.tags, args.attributes, args.group_by, args.load_preset, None)

if __name__ == '__main__':
    main_cli()
