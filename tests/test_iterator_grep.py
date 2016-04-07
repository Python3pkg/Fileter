#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test the actual file iterators.
"""
import fileter
import unittest
import os, shutil


class TestIteratorGrep(unittest.TestCase):
    """
    Unittests to test the built-in grep iterator.
    """

    def setUp(self):
        if os.path.isdir("_temp"):
            shutil.rmtree('_temp')
        os.makedirs("_temp")

    def tearDown(self):
        shutil.rmtree("_temp")

    def test_basic_grep(self):
        """
        Test basic grepping
        """
        # create a testing file
        with open("_temp/test", "w") as outf:
            outf.write("first line\n")
            outf.write("second line\n")
            outf.write("no l' word here...\n")
            outf.write("another line\n")
            outf.write("l-ine\n")

        # create grep iterator and grep
        g = fileter.iterators.Grep("line")
        g.add_file("_temp/test")
        self.assertListEqual(g.get_all()[0], ["first line\n", "second line\n", "another line\n"])
