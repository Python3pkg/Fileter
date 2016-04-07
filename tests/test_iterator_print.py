#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test the actual file iterators.
"""
import fileter
import unittest
import shutil
import os


class TestIteratorPrint(unittest.TestCase):
    """
    Unittests to test the built-in print files iterator.
    """

    def test_basic_print(self):
        """
        Test basic print - this don't actually test input, just that nothing is broken.
        """
        # create remove-files iterator and execute
        rf = fileter.iterators.PrintFiles()
        rf.add_folder("test_dir")
        rf.dry_run()
