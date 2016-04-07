# a fileter script to remove all pyc files before I upload package to pypi.
import fileter
it = fileter.iterators.RemoveFiles(force=True)
it.add_pattern("*.pyc")
it.process_all()
