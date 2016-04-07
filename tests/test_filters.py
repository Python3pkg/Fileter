#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for the file filters.
"""
import fileter
import unittest


class TestFilters(unittest.TestCase):
    """
    Unittests to test file filters.
    """

    def test_creating_filter(self):
        """
        Testing creation of a basic filter.
        """
        class TestFilter(fileter.filters.FilterAPI):
            def match(self, filepath):
                return True
        self.assertTrue(TestFilter().match("bla"))

    def test_regex_filter(self):
        """
        Test the regex filter.
        """
        _filter = fileter.filters.FilterRegex("test")
        self.assertTrue(_filter.match("test"))
        self.assertFalse(_filter.match("no-no"))

        _filter = fileter.filters.FilterRegex(".*test")
        self.assertTrue(_filter.match("test"))
        self.assertTrue(_filter.match("bla_test"))
        self.assertFalse(_filter.match("no-no"))

    def test_pattern_filter(self):
        """
        Test the file pattern filter.
        """
        _filter = fileter.filters.FilterPattern("/test/*")
        self.assertTrue(_filter.match("/test/"))
        self.assertTrue(_filter.match("/test/abc"))
        self.assertFalse(_filter.match("no-no"))

    def test_extension_filter(self):
        """
        Test the files extension filter.
        """
        _filter = fileter.filters.FilterExtension("py")
        self.assertTrue(_filter.match("file.py"))
        self.assertFalse(_filter.match("file.exe"))
        self.assertFalse(_filter.match("file"))
        self.assertFalse(_filter.match(""))

        _filter = fileter.filters.FilterExtension(["py", "js"])
        self.assertTrue(_filter.match("file.py"))
        self.assertTrue(_filter.match("file.js"))
        self.assertFalse(_filter.match("file.exe"))
        self.assertFalse(_filter.match("file"))
        self.assertFalse(_filter.match(""))
