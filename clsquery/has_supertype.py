from typing import Union, List

def has_supertype(cls, supertypes: Union[str, List[str]], avoid_types: Union[str, List[str]] = ""):
    if not hasattr(cls, "__base__"):
        return False
    if cls.__base__ is None:
        return False
    if (type(avoid_types) == list and cls.__base__.__name__ in avoid_types) or \
        cls.__base__.__name__ == avoid_types:
        return False
    if (type(avoid_types) == list and cls.__base__.__name__ in supertypes) or \
        cls.__base__.__name__ == supertypes:
        return True
            
    return has_supertype(cls.__base__, supertypes, avoid_types)
