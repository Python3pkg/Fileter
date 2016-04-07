# Fileter
Lightweight lib to iterate and process files using multiple sources and filters.

Source at [GitHub](https://github.com/RonenNess/Fileter).
Docs at [PythonHosted.org](http://pythonhosted.org/fileter/).

## Install

Install fileter via pip:

```python
pip install fileter
```

## How to use

This lib provide an easy way to iterate files (recursively) using filters, and process selected files.

To use this lib you need to create an iterator, add some files and folder sources to it, add some optional filters if needed and execute the iterator actions.

For example, say you want to iterate over all all cpp files in a project dir, skip folders containing the word "readonly", and add the line "// this is cpp" to the beginning of every file.
With Fileter, you do it like this:


```python
import fileter

it = fileter.iterators.AddHeader("// this is cpp\n")
it.add_pattern("*.cpp", root="project_dir")
it.add_filter_by_pattern("*/*readonly*/*", it.FilterType.Exclude)
it.process_all()
```

And if you want to cover all gcc-recognized cpp files, you can use these alternative methods:

```python
import fileter

it = fileter.iterators.AddHeader("// this is cpp\n")
it.add_folder("project_dir")
it.add_filter_by_pattern("*/*readonly*/*", it.FilterType.Exclude)
it.add_filter_by_extension(["cpp", "h", "hpp", "c", "cc", "cp", "c++", "cxx"])
it.process_all()
```

You can also use the iter to iterate over the files while processing them, eg:

```python
for filename in it:
    print "Processed: " + filename
```

For more simple examples check out the [Recipes](#recipes).

## Meet the classes

Fileter contains few class types you should know. 
In this section we will list the important objects.

### FilesIterator

This is the basic class you use to iterate files.
To use it, create an instance, add file sources (like files, directories, etc), and use it as an iterator.

This class doesn't do anything special while processing files, its just for iterating:

```python
import fileter

it = fileter.FilesIterator()
it.add_folder("iterate_this")
for filename in it:
    print "Found file: " + filename
```

You can also request all files in a list, by using:

```python
import fileter

it = fileter.FilesIterator()
files = it.get_all()
```

### Adding sources to iterator

Iterators are fed with file sources that tells them which files to process.
A source can be a single file, a folder to scan, or a customized class that can do anything, like generate file names based on some algorithm.

For most cases you only need to add files and folders, and for that you can use the following 4 functions:

```python
# adding single or list of files:
it.add_file("some_file")
it.add_file(["first_file", "second_file"])

# adding folders to scan files inside
it.add_folder("some_dir")
it.add_folder("some_dir", depth=1)

# adding folders with filter
it.add_filtered_folder("project_dir", regex_expression, depth=3)

# adding folders with linux-style file patterns (by a single pattern or a list of patterns)
it.add_pattern("src/*", root="project/", depth=3)
it.add_pattern(["src/*.c", "project/src/*.cpp"], root="project/", depth=3)
```

If you find yourself in need to create a customized source, all the sources are located in the 'sources' folder and you can inherit from SourceAPI to create your own.
To add a custom source, use add_source():

```python
# define custom source class
class CustomSource(SourceAPI):
    def next(self):
        yield my_magic_files_getter()

# add it to iterator
it.add_source(CustomSource())
```

### Iterate folders

Filter is not just for files, you can also use it to iterate folders:

```python
# iterate recursively just the folders in "some_dir"
it.add_folder("some_dir", source_type=it.SourceTypes.FoldersOnly)

# iterate file and folders in "some_dir"
it.add_folder("some_dir", source_type=it.SourceTypes.FilesAndFolders)

# same works with filtered folders and patterns
it.add_filtered_folder("project_dir", regex_expression, source_type=it.SourceTypes.FilesAndFolders)
it.add_pattern("src/*", root="project/", depth=3, source_type=it.SourceTypes.FilesAndFolders)
```

### Filters

If you need to scan lots of folders but want to be able to filter which files to process (for example, by extension), you can use filters.
A filter is a simple class that get filenames and return if should process them it or not.

Fileter comes with three basic filters: by extensions, by pattern, and by regex:

```python
# will only process py and js files:
it.add_filter_by_extension(["py", "js"])

# using regex to only process files ending with .exe
it.add_filter_by_regex(".*\.exe$")

# using linux-style patterns to only process files in git folders
it.add_filter_by_pattern("*/.git/*")
```

If you need to create your own filters inherit from FilterAPI located in the "filters" folder and implement the matching function.
To use a custom filter:

```python
# define custom filter
class CustomFilter(FilterAPI):
    def match(self, filepath):
        return magic_filter(filepath)

# add it to iterator
it.add_filter(CustomFilter())
```

#### Filter types

By default, a file must match all filters for it to be processed.
However, this behavior can be changed by using filter types.

When adding a new filter you can also provide a second param to determine filter behavior.
For example:

```python
it.add_filter_by_extension(["py", "js"], it.FilterType.Required)
```

The filter options are:

##### FilterType.Required

This is the default option. All required filters must match in order for a file to be processed.

##### FilterType.Include

As soon as a single include filter match the file, we will stop filtering and process file right away.
This means that order of filters is important.

##### FilterType.Exclude

As soon as a single exclude filter match the file, we will stop filtering and ignore file right away.
This means that order of filters is important.

#### Dry runs

For debugging, you can use dry-runs to just print the files that passed all the filters and about to be processed:

```python
it.dry_run()
```

### Special iterator types

You can inherit from the file iterator class to add a special processing method to apply on every file while iterating.
Fileter comes with several built-in iterators, all located in 'iterators' folder.

To list few:

- AddHeader: add a constant header to all files.
- ConcatFiles: concat all files into a single output file.
- Grep: do grep filtering on files.
- PrintFiles: for tests, simply print files.
- RemoveFiles: remove all files (apply with filters for selective removing).

If you implement your own iterator remember there are many hooks you can implement to invoke while processing files.
For more information check out the FilesIterator implementation (in files_iterator.py).

## Recipes

Some examples to show cool stuff you can easily do with Fileter!

### Clean python dir

This script will remove all .pyc files from current dir (recursively).

```python
import fileter
it = fileter.iterators.RemoveFiles(force=False)
it.add_pattern("*.pyc")
it.process_all()
```

Note: for caution measures, this script will prompt user for every file about to be deleted.
To remove all files silently, just set force=True in constructor.

### Compile JS

This script will merge together all js files in folder (recursively).

```python
import fileter
it = fileter.iterators.ConcatFiles("output.js")
it.add_folder(".")
it.add_filter_by_extension("js")
it.process_all()
```

### Fix python encoding & execution

This file will add the famous comment:

```
#!/usr/bin/python
# -*- coding: utf-8 -*-
```

To the beginning of every python file in folder.
If header already exist, it will not add twice.

```python
import fileter
head = """
#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
it = fileter.iterators.AddHeader(head)
it.add_folder(".")
it.add_filter_by_extension("py")
it.process_all()
```

### Grep something

Grep lines using regex from all files in current folder.

Note: this script will ignore all files inside .git and .svn folders.

```python
import fileter
it = fileter.iterators.Grep("grep_expression...")
it.add_folder(".")
it.add_filter_by_pattern(["*/.git/*", "*/.svn/*"], it.FilterType.Exclude)
for line in it:
    print line
```

### Normalize CRLF to LF

This script iterate all files in a given folder and replace "\r\n" with a single "\n".

```python
import fileter

class NormalizeLF(fileter.FilesIterator):
    """
    Iterate over files and replace \r\n with \n (eg CRLF -> LF).
    """
    def process_file(self, path, dryrun):
    
        if dryrun:
            return path
            
        with open(path, 'rb') as infile:
            buff = infile.read()
            buff = buff.replace("\r\n", "\n")
        with open(path, 'wb') as outfile:
            outfile.write(buff)
        return path

it = NormalizeLF()
it.add_folder(".")
it.process_all()
```

### Search and replace

This code iterate common text files and replace the word "hello" with "world".

```python
import os
import fileter

class ReplaceWords(fileter.FilesIterator):
    """
    Iterate over files and replace 'hello' with 'world'.
    """
    def process_file(self, path, dryrun):
    
        if dryrun:
            return path

        with open(path, "r") as infile:
            buffer = infile.read()

        buffer = buffer.replace("hello", "world")

        with open(path, "w") as outfile:
            outfile.write(buffer)

it = ReplaceWords()
it.add_folder(".")
it.add_filter_by_extension(["txt", "text", "md", "srt"])
it.process_all()
```

### Show files stats

This code will iterate over files and print useful information about them.

```python
import os
import fileter

class PrintStats(fileter.FilesIterator):
    """
    Iterate over files and print their data.
    """

    def on_start(self):
        print "nlink", "ctime", "mtime", "mode", "size"

    def process_file(self, path, dryrun):
        stat = os.stat(path)
        for field in ["st_nlink", "st_ctime", "st_mtime", "st_mode", "st_size"]:
            print getattr(stat, field),
        print ""
        return path

it = PrintStats()
it.add_folder(".")
it.add_filter_by_pattern(["*/.git/*", "*/.svn/*"], it.FilterType.Exclude)
it.process_all()
```

## Run Tests

From Fileter root dir:

```shell
cd tests
python test_all.py
```

Tests are not included in the pypi package, to run them please clone from git.

## Changes

### 1.0.3

- Added pattern filter.
- Added pattern source.
- Added new hooks (enter directory, start source, etc..)
- Changed the way dry-runs are handled.
- Added filtering type - Required / Include / Exclude.

### 1.0.4

- Fixed Files Print iterator.
- Added some tests.
- Added option to return just files, just folders, or both for iterators and sources.
- Renamed get_files() into get_all(), since its now not just for files.

#### Contact

For bugs use the issue report, for other stuff feel free to contact me at ronenness@gmail.com.

