from typing import List, TYPE_CHECKING, Union
if TYPE_CHECKING:
    from clsquery import ClassQueryFormatter
from clsquery import default_formatter, AVOID_TAG_STR


class ClassQuery:
    def __init__(self, 
                 paths: List[str], 
                 supertypes: List[str] = None, 
                 tags: List[str] = None, 
                 attributes: List[str] = ["__name__"], 
                 group_by: List[str] = None, 
                 recursive = False,
                 formatter: 'ClassQueryFormatter' = default_formatter,
                 avoid_tag_str = AVOID_TAG_STR):
        """
        - `paths` A list of file and/or directory paths
        - `supertypes` A list of parent types to limit the search to
        - `tags` A list of tags to limit the search to. This is assuming classes found have a global attribute `tags`
        - `attributes` A list of attributes to be printed for each class found
        - `group_by` A list of attributes to group the found classes by
        - `formatter` A function that takes in query results, and a few other args, and returns a str to be printed and returned by this function

            Default: clsquery.default_formatter
        - `avoid_tag_str` A string that if found prefixing a tag, the search will avoid the tag rather than include it

            Default: '_'
        - `query` A ClassQuery instance. Other provided args will override the args in the query instance
        - `recursive` Whether or not a recursive search should be done on each path in `paths`
            
            Default: False
        - `log_results` Whether or not the query results should be logged to the console using the str returned from `formatter`

            Default: False
        """
        self.paths = paths
        self.supertypes = supertypes
        self.tags = tags
        self.attributes = attributes
        self.group_by = group_by
        self.recursive = recursive
        self.formatter = formatter
        self.avoid_tag_str = avoid_tag_str

    def query(self, 
              paths: Union['ClassQuery', str, List[str]] = None, 
              supertypes: Union[str, List[str]] = None, 
              tags: Union[str, List[str]] = None, 
              attributes: Union[str, List[str]] = ["__name__"], 
              group_by: Union[str, List[str]] = None, 
              formatter: 'ClassQueryFormatter' = None,
              avoid_tag_str = None,
              recursive: bool = None,log_results=False):
        from clsquery import query as query_
        return query_(paths=paths,
                      supertypes=supertypes,
                      tags=tags,
                      attributes=attributes,
                      group_by=group_by,
                      formatter=formatter,
                      avoid_tag_str=avoid_tag_str,
                      query=self, 
                      recursive=recursive,
                      log_results=log_results)
