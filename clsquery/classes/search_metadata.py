from typing import List
from clsquery.format_list import format_list
from clsquery.get_time import get_time


class SearchMetadata:
    def __init__(self, file_or_dir_paths: List[str], supertypes: List[str], tags: List[str], group_by_attributes: List[str] = None) -> None:
        doc_gen_metadata = []
        doc_gen_metadata.append(f"Date:              {get_time()}")
        doc_gen_metadata.append("Paths:             " + format_list(file_or_dir_paths, is_long_format=True))
        doc_gen_metadata.append("Supertypes filter: " + format_list(supertypes))
        doc_gen_metadata.append("Tag filter:        " + format_list(tags))
        if group_by_attributes is not None:
            doc_gen_metadata.append(f"Grouped by:        {format_list(group_by_attributes)}")
        self.metadata = "\n".join(doc_gen_metadata)
