from typing import Dict, List, Union
from clsquery import default_formatter, \
                     get_classes_from_paths, \
                     ClassQuery, \
                     ClassQueryFormatter, \
                     ClassQueryResults, \
                     ClassQueryItem, \
                     logger, \
                     AVOID_TAG_STR, \
                     NULL_GROUP

def query(paths: Union[ClassQuery, List[str]] = None, 
         supertypes: List[str] = None, 
         tags: List[str] = None, 
         attributes: List[str] = ["__name__"], 
         group_by: List[str] = None, 
         formatter: ClassQueryFormatter = None,
         avoid_tag_str = None,
         query: ClassQuery = None,
         recursive: bool = None,
         log_results = False):
    """
    A query for python classes

    Either paths or a query instance must be provided. 
    If both are provided, this functions args will 
    override the query instances args

    Args:
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
    def create_groups(classes: List[ClassQueryItem], group_by: List[str]):
        def get_group_by_attr_value(obj: object, group_by: List[str]):
            if len(group_by) == 0:
                return obj
            attribute = group_by.pop(0)
            if not hasattr(obj, attribute):
                return NULL_GROUP
        
            return get_group_by_attr_value(getattr(obj, attribute), group_by)
        
        def fill_groups(class_: ClassQueryItem, groups: Dict[str, List[ClassQueryItem]], group_by: List[str], group_by_index = 0):
            group_key = str(get_group_by_attr_value(class_.cls, group_by[group_by_index].split(".")))
            if group_key == NULL_GROUP or group_by_index == len(group_by) - 1:
                if group_key not in groups:
                    groups[group_key] = []
                groups[group_key].append(class_)
                return
            if group_key not in groups:
                groups[group_key] = {}
            fill_groups(class_, groups[group_key], group_by, group_by_index+1)

        if group_by is None:
            return None
        
        root_group = {}
        for class_ in classes:
            fill_groups(class_, root_group, group_by)
        
        return root_group

    if type(paths) == ClassQuery:
        query = paths
        paths = None

    if query is not None:
        paths = query.paths if paths is None else paths
        supertypes = query.supertypes if supertypes is None else supertypes
        tags = query.tags if tags is None else tags
        attributes = query.attributes if attributes is None else attributes
        group_by = query.group_by if group_by is None else group_by
        recursive = query.recursive if recursive is None else recursive
        formatter = query.formatter if query.formatter is not None else formatter
        avoid_tag_str = query.avoid_tag_str if query.avoid_tag_str is None else avoid_tag_str

    if paths is None:
        raise ValueError("No Paths argument provided. Expected list of valid paths")
    
    if formatter is None:
        formatter = default_formatter

    if avoid_tag_str is None:
        avoid_tag_str = AVOID_TAG_STR

    if recursive is None:
        recursive = True

    query_ = ClassQuery(paths=paths, 
                        supertypes=supertypes, 
                        tags=tags, 
                        attributes=attributes, 
                        group_by=group_by, 
                        recursive=recursive,
                        formatter=formatter,
                        avoid_tag_str=avoid_tag_str)

    classes = get_classes_from_paths(paths, supertypes, tags, avoid_tag_str=avoid_tag_str, recursive=recursive)
    groups = create_groups(classes, group_by)
    results = ClassQueryResults(classes, groups, query_, formatter)
    if log_results:
        logger.info(str(results))
    
    return results
