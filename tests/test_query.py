import os
from unittest import TestCase
import clsquery

class TestQuery(TestCase):
    def setUp(self):
        self.base_folder = os.path.dirname(os.path.dirname(__file__))
        self.paths = [
            # folder
            os.path.join(self.base_folder, "clsquery", "classes"),
            # module
            os.path.join(self.base_folder, "clsquery", "classes", "class_query.py")
        ]

    def test_basic_query(self):
        result = clsquery.query(self.paths, log_results=True)

    def test_basic_query_literal_type_args(self):
        result = clsquery.query(paths=self.paths[0], 
                                supertypes="object", 
                                tags="", 
                                log_results=True)

    def test_basic_query_mixed_type_args(self):
        result = clsquery.query(paths=self.paths, 
                                supertypes="object", 
                                tags=None, 
                                log_results=True)

    def test_saved_query(self):
        saved_query = clsquery.ClassQuery(self.paths)
        results = saved_query.query(log_results=True)

    def test_saved_query_with_overrides(self):
        saved_query = clsquery.ClassQuery(self.paths, group_by=None)
        results = saved_query.query(paths=self.paths[0], group_by="__base__.__name__", log_results=True)

    def test_saved_query_with_overrides2(self):
        saved_query = clsquery.ClassQuery(self.paths, group_by=None)
        results = clsquery.query(paths=self.paths[0], group_by="__base__.__name__", query=saved_query, log_results=True)

    def test_grouped_query(self):
        result = clsquery.query(self.paths, group_by=["__base__.__name__", "__name__"], log_results=True)

    def test_no_duplicate_class(self):
        # This query runs into the DuplicateClassError class twice
        result = clsquery.query(paths=self.paths, log_results=True)
        query_item_set = set()
        for query_item in result.classes:
            if (query_item.cls.__name__, query_item.path) not in query_item_set:
                query_item_set.add(query_item.cls.__name__)
            else:
                raise DuplicateClassError(query_item.cls.__name__, query_item.path)

    def test_recursive_query(self):
        result = clsquery.query(paths=[os.path.join(self.base_folder, "clsquery")], 
                                recursive=True,
                                log_results=True)


class DuplicateClassError(Exception):
    def __init__(self, class_name: str, filepath:str) -> None:
        message = f"""While fetching classes, two classes with the same name and path were added to the query. This should not be possible

Class Name:  {class_name}
Path:  {filepath}
"""
        super().__init__(message)
