Sources are iteratable objects that provide a collection of files to scan.
This folder contains 3 basic source types: files(s), recursive folders, and recursive folders with regex filter.

If you need any special files source (for example something that query server for filenames or something that generate new filenames via code), you can inherit from the SourceAPI.