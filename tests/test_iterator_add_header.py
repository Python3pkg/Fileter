#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test the actual file iterators.
"""
import fileter
import unittest
import shutil
import os


class TestIteratorAddHeader(unittest.TestCase):
    """
    Unittests to test the built-in add-header iterator.
    """

    def setUp(self):
        if os.path.isdir("_temp"):
            shutil.rmtree('_temp')
        os.makedirs("_temp")

    def tearDown(self):
        shutil.rmtree("_temp")

    def test_basic_add_header(self):
        """
        Test basic add header iterator
        """
        # header string
        header = "HEADER\n~~~~~~~\n"

        # create a file without header
        with open("_temp/test1", "w") as outf:
            outf.write("first file\n")

        # create another file, already with the header
        with open("_temp/test2", "w") as outf:
            outf.write(header + "second file\n")

        # create add-header iterator and execute
        ah = fileter.iterators.AddHeader(header)
        ah.add_folder("_temp")
        ah.process_all()

        # check result of the file we were supposed to add header to
        with open("_temp/test1", "r") as infile:
            result = infile.read()
        self.assertEqual(result, header + "first file\n")

        # check result of the file that already had header
        with open("_temp/test2", "r") as infile:
            result = infile.read()
        self.assertEqual(result, header + "second file\n")
