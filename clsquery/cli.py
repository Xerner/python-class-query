import argparse
import json
from pathlib import Path
from clsquery import query, AVOID_TAG_STR

def cli():
    """
    run `python -m clsquery.cli -h` for help

    Note: Custom formatting is only supported when calling the query function directly from a script
    """
    usage = f"""python -m clsquery.{Path(__file__).name} --path STRING

A query command for Python classes

"""
    parser = argparse.ArgumentParser(usage=usage, formatter_class=argparse.RawDescriptionHelpFormatter)
    mutex = parser.add_mutually_exclusive_group(required=True)
    mutex.add_argument('-p', '--paths', metavar="STRING", type=str, nargs="*", help='directory path or filepath to the classes to generate docs for')
    parser.add_argument('-t', '--tags', metavar="STRING", type=str, nargs="*", help=f"the tags to look for when including classes. A class must have a 'tags' attribute for this to work. Prefix tags with '{AVOID_TAG_STR}' to specify they should NOT be included")
    parser.add_argument('-s', '--supertypes', metavar="STRING", type=str, nargs="*", help="The supertypes to look for when including classes")
    parser.add_argument('-a', '--attributes', metavar="STRING", type=str, nargs="*", default=["__name__"], help="What attributes of the class to return")
    parser.add_argument('-g', '--group-by', metavar="STRING", type=str, nargs="*", help="What attribute to group the classes by")
    parser.add_argument('-r', '--recursive', action="store_true", help="Whether or not a recursive search should be done on each path in 'paths'")
    args = parser.parse_args()
    query(paths=args.paths, 
          supertypes=args.supertypes, 
          tags=args.tags, 
          attributes=args.attributes, 
          group_by=args.group_by, 
          recursive=args.recursive,
          log_results=True)

if __name__ == '__main__':
    cli()
