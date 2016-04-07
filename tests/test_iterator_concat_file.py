#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test the actual file iterators.
"""
import fileter
import unittest
import shutil
import os


class TestIteratorConcat(unittest.TestCase):
    """
    Unittests to test the built-in concat iterator.
    """

    def setUp(self):
        if os.path.isdir("_temp"):
            shutil.rmtree('_temp')
        os.makedirs("_temp")

    def tearDown(self):
        shutil.rmtree("_temp")

    def test_basic_concat(self):
        """
        Test basic concat
        """
        # create a testing file
        with open("_temp/test1", "w") as outf:
            outf.write("first file\n")
        with open("_temp/test2", "w") as outf:
            outf.write("second file\n")

        # create concat iterator and execute
        c = fileter.iterators.ConcatFiles("_temp/output")
        c.add_folder("_temp")
        c.process_all()

        # check result
        with open("_temp/output", "r") as infile:
            result = infile.read()
        self.assertEqual(result, "first file\nsecond file\n")
