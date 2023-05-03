from typing import Type


class ClassQueryItem:
    def __init__(self, cls: Type, path: str):
        self.cls = cls
        self.path = path

    def __eq__(self, __value: object) -> bool:
        if type(__value) != ClassQueryItem:
            return False
        
        return self.cls.__name__ == __value.cls.__name__ and self.path == __value.path