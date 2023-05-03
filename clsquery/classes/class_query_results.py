from typing import TYPE_CHECKING, Dict, List
if TYPE_CHECKING:
    from clsquery import ClassQuery, ClassQueryFormatter, ClassQueryItem


class ClassQueryResults:
    def __init__(self, classes: List['ClassQueryItem'], groups: Dict[str, List['ClassQueryItem']], query: 'ClassQuery', formatter: 'ClassQueryFormatter'):
        self.classes = classes
        self.groups = groups
        self.query = query
        self.formatter = formatter

    def __str__(self):
        return self.formatter(self, 0)
