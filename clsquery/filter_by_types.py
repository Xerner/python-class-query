from typing import List, Union
from clsquery.has_supertype import has_supertype

def filter_by_types(self, classes: List, supertype: str, avoid_types: Union[str, List[str]] = ""):
        self.supertype = supertype
        self.avoid_types = avoid_types
        return [class_ for class_ in classes if has_supertype(class_, supertype, avoid_types)]
