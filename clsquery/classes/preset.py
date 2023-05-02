from typing import List, Callable


class FinderPreset:
    def __init__(self, 
                 paths: List[str], 
                 supertypes: List[str], 
                 tags: List[str], 
                 attributes: List[str], 
                 group_by: List[str], 
                 formatter: Callable[[List[object], List[str], ], str]):
        self.paths = paths
        self.supertypes = supertypes
        self.tags = tags
        self.attributes = attributes
        self.group_by = group_by
        self.formatter = formatter
