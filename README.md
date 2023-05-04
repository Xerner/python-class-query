# Python Class Query <!-- omit from toc -->

![tests-passing](https://img.shields.io/badge/tests-passing-brightgreen)

`clsquery` is a searching tool implemented to help developers query classes available in files and folders for viewing or for use during runtime. Only classes defined in the files being searched are included. Imported classes are ignored.

- [Installation](#installation)
- [Usage](#usage)
  - [Python](#python)
  - [Command Line](#command-line)
- [Examples](#examples)
  - [Basic Search](#basic-search)
  - [With a tag filter and additional attributes](#with-a-tag-filter-and-additional-attributes)
  - [With grouping](#with-grouping)

**Todo**

- Make use of different log levels

## Installation

```bash
python -m pip install clsquery
```

## Usage

### Python

Simple query that finds any Python Class and prints results to console

```python
import clsquery

results = clsquery.query("/path/to/classes", log_results=True)
```

Simple query that finds any Python Class that inherits from `MyParentClass` and prints results to console

```python
import clsquery

results = clsquery.query("/path/to/classes", "MyParentClass", log_results=True)
```

Reusing a saved query

```python
import clsquery

saved_query = clsquery.ClassQuery("/path/to/classes", "MyParentClass")
results = saved_query.query(log_results=True)
# or
results = clsquery.query(query=saved_query, log_results=True)
```

Overriding an attribute of a saved query

```python
import clsquery

saved_query = clsquery.ClassQuery("/path/to/classes", "MyParentClass")
results = saved_query.query(paths="/different/path/to/classes", log_results=True)
```

A query that will find all Python Classes in each module found at the path provided that
- Inherits from `MyParentClass`
- has an attribute `tags` that is a list containing the value `"snake"`
- has an attribute `tags` that is a list that **does not** contain the value `"wolverine"`

And, using the default formatter, will print each class grouped by the module it came from and display its name and docstring in a table-like format

```python
import clsquery

results = clsquery.query(paths="/path/to/classes", 
                         supertypes="MyParentClass",
                         tags=["snake", "_wolverine"],
                         attributes=["__name__", "__doc__"],
                         group_by="__module__")
```

> Prefix tags with a _ (underscore) to specify they should NOT be included

A recursive search that will look in all folders and modules under the paths provided

```python
import clsquery

results = clsquery.query("/path/to/parent/folder", recursive=True, log_results=True)
```

### Command Line

Help dialog

```
usage: python -m clsquery.cli.py --path STRING

A query command for Python classes

optional arguments:
  -h, --help            show this help message and exit
  -p [STRING [STRING ...]], --paths [STRING [STRING ...]]
                        directory path or filepath to the classes to generate
                        docs for
  -t [STRING [STRING ...]], --tags [STRING [STRING ...]]
                        the tags to look for when including classes. A class
                        must have a 'tags' attribute for this to work. Prefix
                        tags with '_' to specify they should NOT be included
  -s [STRING [STRING ...]], --supertypes [STRING [STRING ...]]
                        The supertypes to look for when including classes
  -a [STRING [STRING ...]], --attributes [STRING [STRING ...]]
                        What attributes of the class to return
  -g [STRING [STRING ...]], --group-by [STRING [STRING ...]]
                        What attribute to group the classes by
  -r, --recursive       Whether or not a recursive search should be done on
                        each path in 'paths'
```

Queries are, by default, formatted by an internal formatter function with results similar to the below

```
# Input
python -m clsquery.cli -p "path/to/classes1" "path/to/classes2" -t Tag1 Tag2 _Tag3 -s ParentClass1 ParentClass2 -a __name__ tags <other attributes>
 
# Output
Search Results
---------------
 
Date:              2022-12-07 10:10:26
Paths:            
- path/to/classes1
- path/to/classes2
 
Supertypes filter: ParentClass1, ParentClass2
Tag filter:        Tag1, Tag2, _Tag3
 
__name__            tags                    <other attributes>
----------------------------------------------------------------
ChildClass1         ['Tag1']                ...
ChildClass2         ['Tag1', 'Tag2']        ...
ChildClass3         ['Tag2']                ...
```

> Prefix tags with a _ (underscore) to specify they should NOT be included

## Examples

### Basic Search

```
# Input
python -m clsquery.cli -p /path/to/classes
 
# Output
Search Results
---------------
 
Date:              2022-12-07 14:06:31
Paths:            
- /path/to/classes
 
Supertypes filter: None
Tag filter:        None
 
__name__                      
-------------------------------
SomeClass   
ASpecialClass
```

### With a tag filter and additional attributes

Below is assuming the `ASpecialClass` class has an attribute `tags` with the value `['special']`

Notice
- `_special` was supplied as a parameter to exclude `ASpecialClass` which contained `special` in its tags attribute
- `__doc__` is allowed. References to any class attribute is allowed, as long as it can be turned into a string

```
# Input
python -m clsquery.cli -p /path/to/classes --tags _avoid_me -a __name__ __doc__
 
# Output
Search Results
---------------
 
Date:              2022-12-07 14:54:52
Paths:            
- /path/to/classes
 
Supertypes filter: None
Tag filter:        _avoid_me
 
__name__          __doc__                                                          
-------------------------------------------------------------------------------------------------------------------------
SomeClass2        A class that does things
```

### With grouping

Below is assuming the `ASpecialClass` class has an attribute `is_special` with the value `True`, and `SomeClass` has the same attribute with the value `False`

Notice
- It is possible to have multiple levels of grouping

```
# Input
python -m clsquery.cli -p /path/to/classes -g __base__.__name__ is_special  
 
# Output
Search Results
---------------
 
Date:              2022-12-07 17:21:36
Paths:            
- /path/to/classes
 
Supertypes filter: None
Tag filter:        None
Grouped by:        __base__.__name__, is_special
 
SomeParentClass
 
    True
 
        __name__         
        ------------------
        SomeClass   
 
    False
 
        __name__         
        ------------------
        ASpecialClass
```
