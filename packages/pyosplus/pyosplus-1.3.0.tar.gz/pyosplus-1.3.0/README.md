# pyosplus

This Python package provides several useful functions based on `os`/`os.path`:

* [`count_in_dir`](#count_in_dir)

* [`ext_files`](#ext_files)

* [`find_files_dirs`](#find_files_dirs)

* [`inc_name`](#inc_name)

* [`write_dir_tree`](#write_dir_tree)

These functions are really primitive but they happen to be used quite often by some people.

Please feel free to report any bugs.

## Requirements

Python 3.10 or higher.

## Installation

```
pip install pyosplus
```
(see <https://pypi.org/project/pyosplus/>)

## Functions

### `count_in_dir`

```python
count_in_dir(
    directory: str,
    scan_subdirs: bool,
    ignored_exts: list[str] | str = [],
    ) -> tuple[int, int, dict]
```

**Arguments**

* `directory: str`  
    Directory to scan.

* `scan_subdirs: bool`  
    To scan subdirectories (`True`) or not (`False`).

* `ignored_exts: list[str] | str = []`  
    Extension(s) of files to be ignored. Each extension should start with `.` (dot). Extension checks are always case-insensitive (e.g., `".jpg"` is the same as `".JPG"`).

**Returns**

* `tuple[int, int, dict]`  
    Number of directories, number of files, and dictionary with numbers of files with each found extension. Files with extensions `ignored_exts` are not counted.

**Minimal Example**

```python
from pyosplus import count_in_dir
directory = "/path/to/dir"
scan_subdirs = True
num_dirs, num_files, ext_count = count_in_dir(directory, scan_subdirs)
```

--------

### `ext_files`

```python
ext_files(
    directory: str,
    extensions: str | list[str],
    scan_subdirs: bool,
    ) -> list[str]
```

**Arguments**

* `directory: str`  
    Directory to scan.

* `extensions: str | list[str]`  
    Extension(s) of files to search. Each extension should start with `.` (dot). Extension checks are always case-insensitive (e.g., `".jpg"` is the same as `".JPG"`).

* `scan_subdirs: bool`  
    To scan subdirectories (`True`) or not (`False`).

**Returns**

* `list[str]`  
    Sorted list of paths to files with `extensions`.

**Minimal Example**

```python
from pyosplus import ext_files
directory = "/path/to/dir"
extensions = [".jpg", ".jpeg"]
paths = ext_files(directory, extensions)
```

--------

### `find_files_dirs`

```python
find_files_dirs(
    what: str | list[str],
    where: str | list[str],
    where_not: str | list[str] = [],
    name_mode: str = "part",
    type_mode: str = "both",
    ignore_case: bool = True,
    ) -> Generator[str, None, None]
```

**Arguments**

* `what: str | list[str]`  
    String(s) to search in names of files/directories.

* `where: str | list[str]`  
    Path(s) to the directories where to search.

* `where_not: str | list[str] = []`  
    Path(s) to the directories to exclude from search. They should be subdirectories of `where`.

* `name_mode: str = "part"`  
    `"full"` &mdash; `what` is the full name(s) of files/directories,  
    `"part"` &mdash; `what` is the name part(s) of files/directories,  
    `"end"` &mdash; `what` is the name end(s) of files/directories.
    
* `type_mode: str = "both"`  
    `"both"` &mdash; search among files and directories,  
    `"files"` &mdash; search among files only,  
    `"dirs"` &mdash; search among directories only.

* `ignore_case: bool = True`  
    Ignore the case or not:  
    `True` &mdash; `"ABC"` is equal to `"abc"`,  
    `False` &mdash; `"ABC"` is not equal to `"abc"`.  
    It works for `what` only. Paths in `where` and `where_not` should have the same case as in the system.

**Returns**

* `Generator[str, None, None]`  
    Generator of paths to the found files/directories.

**Minimal Example**

```python
from pyosplus import find_files_dirs
what = "thesis"
where = "/path/to/dir"
for path in find_files_dirs(what, where):
    print(path)
```

--------

### `inc_name`

```python
inc_name(
    path: str,
    width: int = 2,
    sep_1: str = ".",
    sep_2: str = "",
    start: int = 2,
    use_ext: bool = True,
    ) -> str
```

**Arguments**

* `path: str`  
    Path to file/directory to be incremented.

* `width: int = 2`  
    Argument of `zfill()` to fill the counter with leading zeros.

* `sep_1: str = "."`  
    Separator before the counter.

* `sep_2: str = ""`  
    Separator after the counter.

* `start: int = 2`  
    The counter first value.

* `use_ext: bool = True`  
    If `True`, the counter will be put before the file extension.  
    If `False`, the counter will be put at the end of string.  
    The latter is for the directories with dot(s) in the names.

**Returns**

* `str`  
    Incremented `path` if `path` already exists or `path` itself if it does not exist.

**Minimal Example**

```python
from pyosplus import inc_name
path = "/path/to/file.txt"
inc = inc_name(path)
```
It returns:

* `"/path/to/file.txt"`  
    if this file does not exist;

* `"/path/to/file.02.txt"`  
    if `"/path/to/file.txt"` exists and `"/path/to/file.02.txt"` does not exist;

* etc.

--------

### `write_dir_tree`

```python
write_dir_tree(
    directories: str | list[str],
    html_file: str,
    print_exts: bool = True,
    num_spaces: int = 4,
    shrunk_dirs: str | list[str] = [],
    shrunk_depth: int = -1,
    shrunk_text: str = " &lt;...&gt;",
    ignored_exts: str | list[str] = [],
    ignored_paths: str | list[str] = [],
    print_root: bool = True,
    captions: list[str] = [],
    print_hr: bool = True,
    )
```

**Arguments**


* `directories: str | list[str]`  
    Directory/directories to scan.

* `html_file: str`  
    Path to a new HTML file for output. If it exists, it will be overwritten.

* `print_exts: bool = True`  
    Print file extensions (`True`) or not (`False`).

* `num_spaces: int = 4`  
    Number of spaces for indentation.

* `shrunk_dirs: str | list[str] = []`  
    Path(s) to the specific directories to be shrunk (i.e., collapsed) in HTML.

* `shrunk_depth: int = -1`  
    The depth (i.e., hierarchy level) from which all the directories should be shrunk (collapsed) in HTML. The depth of `directories` equals 0. `shrunk_depth = -1` means that no directories should be shrunk except those in `shrunk_dirs` (if any).

* `shrunk_text: str = " &lt;...&gt;"`  
    The text to be put next to a shrunk directory name.

* `ignored_exts: str | list[str] = []`  
    Extensions of files to be ignored in HTML. Such files will not be visible in HTML at all. Each extension should start with `.` (dot). Extension checks are always case-insensitive (e.g., ".jpg" is the same as ".JPG").

* `ignored_paths: str | list[str] = []`  
    Paths to the directories/files to be ignored. Unlike the shrunk directories, `ignored_paths` will not be visible in HTML at all.

* `print_root: bool = True`  
    Print a root directory (`True`) or not (`False`).

* `captions: list[str] = []`  
    List of captions to appear before the tree for each directory from `directories`. If `captions` are not empty, the lengths of `captions` and `directories` should be equal so there exists a caption for each directory (in the same order as in these lists).

* `print_hr: bool = True`  
    Print a horizontal line (`True`) or not (`False`).

**Returns**

* `None`. Writes a directory tree structure to `html_file`.

**Minimal Example**

```python
from pyosplus import write_dir_tree
directories = ["/path/to/dir_1", "/path/to/dir_2"]
html_file = "tree.html"
write_dir_tree(directories, html_file)
```

--------

## Changelog

* Version 1.3.0 (2023-12-23)
    * argument `captions` added to `write_dir_tree`.

* Version 1.2.0 (2023-11-11):
    * function `write_html_dir_tree` removed.

* Version 1.1.0 (2023-11-07):
    * function `write_dir_tree` added,
    * function `write_html_dir_tree` deprecated,
    * the default values of `scan_subdirs` in functions `count_in_dir` and `ext_files` removed.

* Version 1.0.0 (2023-11-05): initial release

--------

**pyosplus**

* Version 1.3.0 (2023-12-23)

Copyright (c) 2023 Evgenii Shirokov

MIT License
