# Python Class Query <!-- omit from toc -->

A package for querying Python classes

- [Todo](#todo)
- [Usage](#usage)
  - [Python](#python)
  - [Command Line](#command-line)
- [Examples](#examples)
  - [Basic Search](#basic-search)
  - [With a tag filter and additional attributes](#with-a-tag-filter-and-additional-attributes)
  - [With grouping](#with-grouping)
  - [With presets](#with-presets)

## Todo

- Add a way to distinguish classes with the same name that come from difference sources
- Make use of different log levels

## Usage

### Python

TODO

### Command Line

```
usage: python list.py --path STRING
 
A search command for Python classes
 
optional arguments:
  -h, --help            show this help message and exit
  -p [STRING [STRING ...]], --paths [STRING [STRING ...]]
                        directory path or filepath to the classes to generate docs for
  -t [STRING [STRING ...]], --tags [STRING [STRING ...]]
                        the tags to look for when including classes. A class must have a 'tags' attribute for this to work. Prefix tags with '_' to specify they should NOT be included
  -s [STRING [STRING ...]], --supertypes [STRING [STRING ...]]
                        The supertypes to look for when including classes
  -a [STRING [STRING ...]], --attributes [STRING [STRING ...]]
                        What attributes of the class to return
  -g [STRING [STRING ...]], --group-by [STRING [STRING ...]]
                        What attribute to group the classes by
  -l PRESET, --load-preset PRESET
                        load a preset list of args
 
Options provided on the command line will override options loaded by a preset
```

The list command is a generic python class searching tool implemented to help users discover topic, metric, and requirement classes available. Only classes defined in the files being searched are included. Imported classes are ignored.

It returns a format similar to below

```
# Input
list.py -p "path/to/classes1" "path/to/classes2" -t Tag1 Tag2 _Tag3 -s ParentClass1 ParentClass2 -a __name__ tags <other attributes>
 
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
list -p /path/to/classes
 
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
list -p /path/to/classes --tags _avoid_me -a __name__ __doc__
 
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
list -p /path/to/classes -g __base__.__name__ is_special  
 
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

### With presets

TODO
