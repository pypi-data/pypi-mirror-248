""" pyosplus
    Version 1.3.0 (2023-12-23)
    Copyright (c) 2023 Evgenii Shirokov
    MIT License
"""

from collections import Counter
from collections.abc import Generator
from html import escape
from os import listdir, walk
from os.path import exists, isdir, isfile, join, samefile, splitext


def count_in_dir(
        directory: str,
        scan_subdirs: bool,
        ignored_exts: list[str] | str = [],
        ) -> tuple[int, int, dict]:
    """Return numbers of objects in a directory.

    Arguments
    ---------
    `directory: str`
      Directory to scan.
    `scan_subdirs: bool`
      To scan subdirectories (`True`) or not (`False`).
    `ignored_exts: list[str] | str = []`
      Extension(s) of files to be ignored.
      Each extension should start with `.` (dot).
      Extension checks are always case-insensitive
      (e.g., `".jpg"` is the same as `".JPG"`).

    Returns
    -------
    `tuple[int, int, dict]`
      Number of directories, number of files, and dictionary 
      with numbers of files with each found extension.
      Files with extensions `ignored_exts` are not counted.

    Minimal Example
    ---------------
    ```
    from pyosplus import count_in_dir
    directory = "/path/to/dir"
    scan_subdirs = True
    num_dirs, num_files, ext_count = count_in_dir(directory, scan_subdirs)
    ```
    """
    if not isinstance(ignored_exts, list):
        ignored_exts = [ignored_exts]
    ignored_exts_lc = [ext.lower() for ext in ignored_exts]
    num_dirs, exts = 0, []
    if scan_subdirs:
        for _, dirs, files in walk(directory):
            num_dirs += len(dirs)
            for f in files:
                ext = splitext(f)[1].lower()
                if ext not in ignored_exts_lc:
                    exts.append(ext)
    else:
        for f in listdir(directory):
            if isdir(join(directory, f)):
                num_dirs += 1
            else:
                ext = splitext(f)[1].lower()
                if ext not in ignored_exts_lc:
                    exts.append(ext)
    return num_dirs, len(exts), dict(Counter(exts))


def ext_files(
        directory: str,
        extensions: str | list[str],
        scan_subdirs: bool,
        ) -> list[str]:
    """Return paths to files with given extensions in a directory.

    Arguments
    ---------
    `directory: str`
      Directory to scan.
    `extensions: str | list[str]`
      Extension(s) of files to search.
      Each extension should start with `.` (dot).
      Extension checks are always case-insensitive
      (e.g., `".jpg"` is the same as `".JPG"`).
    `scan_subdirs: bool`
      To scan subdirectories (`True`) or not (`False`).

    Returns
    -------
    `list[str]`
      Sorted list of paths to files with `extensions`.

    Minimal Example
    ---------------
    ```
    from pyosplus import ext_files
    directory = "/path/to/dir"
    extensions = [".jpg", ".jpeg"]
    paths = ext_files(directory, extensions)
    ```
    """
    if not isinstance(extensions, list):
        extensions = [extensions]
    extensions_lc = [ext.lower() for ext in extensions]
    result = []
    if not scan_subdirs:
        for f in sorted(listdir(directory)):
            path = join(directory, f)
            if isfile(path) and (splitext(f)[1].lower() in extensions_lc):
                result.append(path)
    else:
        for root, dirs, files in walk(directory):
            dirs.sort()
            files.sort()
            for f in files:
                if splitext(f)[1].lower() in extensions_lc:
                    result.append(join(root, f))
    return result


def find_files_dirs(
        what: str | list[str],
        where: str | list[str],
        where_not: str | list[str] = [],
        name_mode: str = "part",
        type_mode: str = "both",
        ignore_case: bool = True,
        ) -> Generator[str, None, None]:
    """Find files and/or directories.

    Arguments
    ---------
    `what: str | list[str]`
      String(s) to search in names of files/directories.
    `where: str | list[str]`
      Path(s) to the directories where to search.
    `where_not: str | list[str] = []`
      Path(s) to the directories to exclude from search.
      They should be subdirectories of `where`.
    `name_mode: str = "part"`
      `"full"` - `what` is the full name(s) of files/directories,
      `"part"` - `what` is the name part(s) of files/directories,
      `"end"` - `what` is the name end(s) of files/directories.
    `type_mode: str = "both"`
      `"both"` - search among files and directories,
      `"files"` - search among files only,
      `"dirs"` - search among directories only.
    `ignore_case: bool = True`
      Ignore the case or not:
      `True` - `"ABC"` is equal to `"abc"`,
      `False` - `"ABC"` is not equal to `"abc"`.
      It works for `what` only. Paths in `where` and `where_not`
      should have the same case as in the system.

    Returns
    -------
    `Generator[str, None, None]`
      Generator of paths to the found files/directories.

    Minimal Example
    ---------------
    ```
    from pyosplus import find_files_dirs
    what = "thesis"
    where = "/path/to/dir"
    for path in find_files_dirs(what, where):
        print(path)
    ```
    """
    if not isinstance(what, list):
        what = [what]
    if not isinstance(where, list):
        where = [where]
    if not isinstance(where_not, list):
        where_not = [where_not] if where_not.strip() else []
    what_cs = tuple(w.lower() for w in what) if ignore_case else tuple(what)
    for path in sorted(where):
        for root, dirs, files in walk(path):
            if any(samefile(root, w) for w in where_not):
                dirs[:] = []
                continue
            dirs.sort()
            files.sort()
            match type_mode:
                case "both":
                    entries = dirs + files
                case "files":
                    entries = files
                case "dirs":
                    entries = dirs
                case _:
                    raise ValueError(f"{type_mode = }")
            for entry in entries:
                entry_cs = entry.lower() if ignore_case else entry
                match name_mode:
                    case "full":
                        if entry_cs in what_cs:
                            yield join(root, entry)
                    case "part":
                        if any(w in entry_cs for w in what_cs):
                            yield join(root, entry)
                    case "end":
                        if entry_cs.endswith(what_cs):
                            yield join(root, entry)
                    case _:
                        raise ValueError(f"{name_mode = }")


def inc_name(
        path: str,
        width: int = 2,
        sep_1: str = ".",
        sep_2: str = "",
        start: int = 2,
        use_ext: bool = True,
        ) -> str:
    """Increment a file/directory name if it already exists.

    Arguments
    ---------
    `path: str`
      Path to file/directory to be incremented.
    `width: int = 2`
      Argument of `zfill()` to fill the counter with leading zeros.
    `sep_1: str = "."`
      Separator before the counter.
    `sep_2: str = ""`
      Separator after the counter.
    `start: int = 2`
      The counter first value.
    `use_ext: bool = True`
      If `True`, the counter will be put before the file extension.
      If `False`, the counter will be put at the end of string.
      The latter is for the directories with dot(s) in the names.

    Returns
    -------
    `str`
      Incremented `path` if `path` already exists,
      or `path` itself if it does not exist.

    Minimal Example
    ---------------
    ```
    from pyosplus import inc_name
    path = "/path/to/file.txt"
    inc = inc_name(path)
    ```
    It returns:
      `"/path/to/file.txt"` if this file does not exist;
      `"/path/to/file.02.txt"` if `"/path/to/file.txt"` exists
        and `"/path/to/file.02.txt"` does not exist;
      etc.
    """

    def new_path():
        if i > start - 1:
            return f"{root}{sep_1}{str(i).zfill(width)}{sep_2}{ext}"
        else:
            return path

    root, ext = splitext(path) if use_ext else (path, "")
    i = start - 1
    while exists(result := new_path()):
        i += 1
    return result


def write_dir_tree(
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
        ):
    """Write an HTML file with a directory tree structure.

    Arguments
    ---------
    `directories: str | list[str]`
      Directory/directories to scan.
    `html_file: str`
      Path to a new HTML file for output. If it exists,
      it will be overwritten.
    `print_exts: bool = True`
      Print file extensions (`True`) or not (`False`).
    `num_spaces: int = 4`
      Number of spaces for indentation.
    `shrunk_dirs: str | list[str] = []`
      Path(s) to the specific directories to be shrunk
      (i.e., collapsed) in HTML.
    `shrunk_depth: int = -1`
      The depth (i.e., hierarchy level) from which all
      the directories should be shrunk (collapsed) in HTML.
      The depth of `directories` equals 0.
      `shrunk_depth = -1` means that no directories should
      be shrunk except those in `shrunk_dirs` (if any).
    `shrunk_text: str = " &lt;...&gt;"`
      The text to be put next to a shrunk directory name.
    `ignored_exts: str | list[str] = []`
      Extensions of files to be ignored in HTML. Such files will
      not be visible in HTML at all. Each extension should start
      with `.` (dot). Extension checks are always case-insensitive
      (e.g., ".jpg" is the same as ".JPG").
    `ignored_paths: str | list[str] = []`
      Paths to the directories/files to be ignored.
      Unlike the shrunk directories, `ignored_paths` will not
      be visible in HTML at all.
    `print_root: bool = True`
      Print a root directory (`True`) or not (`False`).
    `captions: list[str] = []`
      List of captions to appear before the tree for each directory
      from `directories`. If `captions` are not empty, the lengths of
      `captions` and `directories` should be equal so there exists a
      caption for each directory (in the same order as in these lists).
    `print_hr: bool = True`
      Print a horizontal line (`True`) or not (`False`).

    Returns
    -------
      `None`. Writes a directory tree structure to `html_file`.

    Minimal Example
    ---------------
    ```
    from pyosplus import write_dir_tree
    directories = ["/path/to/dir_1", "/path/to/dir_2"]
    html_file = "tree.html"
    write_dir_tree(directories, html_file)
    ```
    """

    def recursive_scan(d_path, depth):
        # Shrink the directory if necessary
        if any(samefile(d_path, dd) for dd in shrunk_dirs) or \
                (shrunk_depth > 0 and depth >= shrunk_depth):
            result[-1] += shrunk_text
            return
        # Ignore the directory if necessary
        if any(samefile(d_path, dd) for dd in ignored_paths):
            del result[-1]
            return
        # List directories and files separately
        dirs, files = [], []
        for entry in sorted(listdir(d_path)):
            path = join(d_path, entry)
            if isdir(path):
                code = "<b>" + escape(entry) + "</b>"
                dirs.append((code, path))
            else:
                root, ext = splitext(entry)
                # Ignore the file if necessary
                if (ext.lower() in ignored_exts_lc) \
                        or any(samefile(path, dd) for dd in ignored_paths):
                    continue
                # Do not print extensions if necessary
                file_name = entry if print_exts else root
                files.append((escape(file_name), path))
        # Run recursively
        indent = depth * num_spaces * "&nbsp;"
        for entry, path in files + dirs:
            result.append(f"{indent}{entry}")
            if isdir(path):
                recursive_scan(path, depth + 1)

    if not isinstance(directories, list):
        directories = [directories]
    if not isinstance(ignored_exts, list):
        ignored_exts = [ignored_exts]
    if not isinstance(ignored_paths, list):
        ignored_paths = [ignored_paths]
    if not isinstance(shrunk_dirs, list):
        shrunk_dirs = [shrunk_dirs]
    if captions and (len(captions) != len(directories)):
        raise ValueError("Lengths of `captions` and `directories` "
                         "should be equal.")
    ignored_exts_lc = [ext.lower() for ext in ignored_exts]
    html = ('''<!DOCTYPE html>\n<html>\n<head>\n<meta charset="utf-8" />\n'''
            '''<style>\nmark{background-color: Gainsboro;}\n</style>\n'''
            '''</head>\n<body>\n<samp>\n''')
    num_dirs = len(directories)
    for i, d in enumerate(directories):
        if print_root:
            html += "<b><mark>" + escape(d) + "</mark></b><br />\n"
        if captions:
            html += "<b><mark>" + escape(captions[i]) + "</mark></b><br />\n"
        result = []
        recursive_scan(d, 0)
        if result:
            html += "<br />\n".join(result) + "<br />\n"
        if print_hr and (i != num_dirs - 1):
            html += "<hr />\n"
    html += '''</samp>\n</body>\n</html>\n'''
    with open(html_file, "w", encoding="utf_8") as f:
        f.write(html)
