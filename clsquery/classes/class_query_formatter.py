from typing import Callable
from clsquery import ClassQueryResults


class ClassQueryFormatter(Callable[[ClassQueryResults, int], str]):
    """
    `Args[0]` A ClassQueryResult instance
    `Args[1]` The indent used when formatting the string
    """
