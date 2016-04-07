#!/usr/bin/python
# -*- coding: utf-8 -*-

# to make the imports work in tests
if __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    print path.dirname(path.dirname(path.abspath(__file__)))

# import all tests
from test_filters import *
from test_sources import *
from test_iterators import *
from test_iterator_grep import *
from test_iterator_concat_file import *
from test_iterator_add_header import *
from test_iterator_remove_files import *

# run tests
if __name__ == '__main__':
    unittest.main()
