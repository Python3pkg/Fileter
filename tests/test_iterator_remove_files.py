#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test the actual file iterators.
"""
import fileter
import unittest
import shutil
import os


class TestIteratorRemoveFiles(unittest.TestCase):
    """
    Unittests to test the built-in remove files iterator.
    """

    def setUp(self):
        if os.path.isdir("_temp"):
            shutil.rmtree('_temp')
        os.makedirs("_temp")

    def tearDown(self):
        shutil.rmtree("_temp")

    def test_basic_remove(self):
        """
        Test basic remove files
        """
        # create a testing file
        with open("_temp/test1", "w") as outf:
            outf.write("first file\n")
        with open("_temp/test2", "w") as outf:
            outf.write("second file\n")

        # sanity test to make sure we succeed in creating files
        self.assertTrue(os.path.isfile("_temp/test1"))
        self.assertTrue(os.path.isfile("_temp/test2"))

        # create remove-files iterator and execute
        rf = fileter.iterators.RemoveFiles(True)
        rf.add_folder("_temp")
        rf.process_all()

        # make sure files are removed
        self.assertFalse(os.path.isfile("_temp/test1"))
        self.assertFalse(os.path.isfile("_temp/test2"))
