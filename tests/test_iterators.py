#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test the actual file iterators.
"""
import fileter
import unittest


class TestIterators(unittest.TestCase):
    """
    Unittests to test file iterators, eg the main class.
    """

    def _list_by_iter(self, fiter):
        """
        this helper function iterate over an iterator and return a list with all files in it.
        basically convert from iterator to list of files using for x in y syntax.
        """
        iter_ret = []
        for i in fiter:
            iter_ret.append(i)
        return iter_ret

    def __fix_sep(self, values):
        """
        Unify path separators to match win/linux shenanigans.
        We just replace all separators to be /
        """
        return [i.replace("\\", "/") for i in values]

    def __test_iterator(self, fiter, expected):
        """
        Test a given iterator with all methods - by get_all() and by iteration.
        """
        expected = self.__fix_sep(expected)
        self.assertListEqual(self.__fix_sep(fiter.get_all()), expected)
        self.assertListEqual(self.__fix_sep(self._list_by_iter(fiter)), expected)

    def test_iterator_filters_modes(self):
        """
        Test different filter modes for iterator
        """
        it = fileter.FilesIterator()
        files = ["a.txt", "a.exe", "b.txt", "c.aaa", "d.elf"]
        it.add_file(files)

        # check required filters
        it.add_filter_by_pattern("?.???", it.FilterType.Required)
        self.__test_iterator(it, files)
        it.add_filter_by_pattern("?.e??", it.FilterType.Required)
        self.__test_iterator(it, ["a.exe", "d.elf"])

        # check include filters
        it.add_filter_by_pattern("?.txt", it.FilterType.Include)
        self.__test_iterator(it, ["a.txt", "a.exe", "b.txt", "d.elf"])

        # check exclude filters
        it.add_filter_by_pattern("*.elf", it.FilterType.Exclude)
        self.__test_iterator(it, ["a.txt", "a.exe", "b.txt"])


    def test_creating_an_iterator(self):
        """
        Testing creation of an iterator
        """
        class TestIterator(fileter.FilesIterator):

            all_files = []
            started = False
            ended = False

            def process_file(self, path, dryrun):
                self.all_files.append(path)

            def on_start(self, dryrun):
                self.started = True

            def on_end(self, dryrun):
                self.ended = True

        # create and run test iterator
        _test = TestIterator()
        _test.add_file("test.txt")
        _test.add_file("foo.bar")
        _test.get_all()

        # validate iterator fields
        self.assertListEqual(_test.all_files, ["test.txt", "foo.bar"])
        self.assertTrue(_test.started)
        self.assertTrue(_test.ended)

    def test_basic_iterator_add_files(self):
        """
        Test a basic iterator adding files.
        """
        # add two files and test
        _test = fileter.FilesIterator()
        _test.add_file("test.txt")
        _test.add_file("foo.bar")
        self.__test_iterator(_test, ["test.txt", "foo.bar"])

        # add two more file sources
        _test.add_file(["g", "f"])
        self.__test_iterator(_test, ["test.txt", "foo.bar", "g", "f"])

    def test_basic_iterator_add_folders(self):
        """
        Test a basic iterator with folders
        """
        # iterate files with a single depth level
        _test = fileter.FilesIterator()
        _test.add_folder("test_dir", 0)
        self.__test_iterator(_test, ['test_dir/0_a', 'test_dir/0_b', 'test_dir/0_c.txt'])

        # iterate files with a 1-depth level
        _test = fileter.FilesIterator()
        _test.add_folder("test_dir", 1)
        self.__test_iterator(_test, ['test_dir/0_a', 'test_dir/0_b', 'test_dir/0_c.txt',
                                     'test_dir/depth1/1_a', 'test_dir/depth1/1_b.exe',
                                     'test_dir/foo/bar.txt'])

        # iterate files without depth limit
        _test = fileter.FilesIterator()
        _test.add_folder("test_dir")
        self.__test_iterator(_test, ['test_dir/0_a', 'test_dir/0_b', 'test_dir/0_c.txt',
                                     'test_dir/depth1/1_a', 'test_dir/depth1/1_b.exe',
                                     'test_dir/depth1/depth2/2_a', 'test_dir/depth1/depth2/bar.txt',
                                     'test_dir/depth1/depth2/depth3/3',
                                     'test_dir/foo/bar.txt'])

    def test_basic_iterator_add_filtered_folders(self):
        """
        Test a basic iterator with filtered folders
        """
        # filter only things inside "depth1" folder.
        _test = fileter.FilesIterator()
        _test.add_filtered_folder("test_dir", ".*depth1.*")
        self.__test_iterator(_test, ['test_dir/depth1/1_a', 'test_dir/depth1/1_b.exe',
                                     'test_dir/depth1/depth2/2_a', 'test_dir/depth1/depth2/bar.txt',
                                     'test_dir/depth1/depth2/depth3/3'])

        # filter out directories that have '3' in their name, eg "depth3"
        _test = fileter.FilesIterator()
        _test.add_filtered_folder("test_dir", "(?!^.*depth3.*$).*")
        self.__test_iterator(_test, ['test_dir/0_a', 'test_dir/0_b', 'test_dir/0_c.txt',
                                     'test_dir/depth1/1_a', 'test_dir/depth1/1_b.exe',
                                     'test_dir/depth1/depth2/2_a', 'test_dir/depth1/depth2/bar.txt',
                                     'test_dir/foo/bar.txt'])

        # filter only things inside "depth1" folder, but only with 1 depth level.
        _test = fileter.FilesIterator()
        _test.add_filtered_folder("test_dir", ".*depth1.*", 1)
        self.__test_iterator(_test, ['test_dir/depth1/1_a', 'test_dir/depth1/1_b.exe'])

    def test_basic_iterator_add_pattern(self):
        """
        Test a basic iterator adding patterns.
        """
        # add two files and test
        _test = fileter.FilesIterator()
        _test.add_pattern("*.txt", "test_dir", 1)
        self.__test_iterator(_test, ["test_dir/0_c.txt", "test_dir/foo/bar.txt"])

    def test_basic_iterator_with_extension_filter(self):
        """
        Test a basic iterator with extension filter
        """
        # create an iterator with all folders, and make sure everything works (sanity)
        _test = fileter.FilesIterator()
        _test.add_folder("test_dir")
        self.__test_iterator(_test, ['test_dir/0_a', 'test_dir/0_b', 'test_dir/0_c.txt',
                                     'test_dir/depth1/1_a', 'test_dir/depth1/1_b.exe',
                                     'test_dir/depth1/depth2/2_a', 'test_dir/depth1/depth2/bar.txt',
                                     'test_dir/depth1/depth2/depth3/3',
                                     'test_dir/foo/bar.txt'])

        # now add extension filter to return just txt files
        _test.add_filter_by_extension("txt")
        self.__test_iterator(_test, ['test_dir/0_c.txt', 'test_dir/depth1/depth2/bar.txt',
                                     'test_dir/foo/bar.txt'])

        # now create a new iter and add extension filter with two options
        _test = fileter.FilesIterator()
        _test.add_folder("test_dir")
        _test.add_filter_by_extension(["txt", "exe"])
        self.__test_iterator(_test, ['test_dir/0_c.txt', 'test_dir/depth1/1_b.exe',
                                     'test_dir/depth1/depth2/bar.txt', 'test_dir/foo/bar.txt'])

    def test_basic_iterator_with_regex_filter(self):
        """
        Test a basic iterator with regex filter
        """
        # create an iterator with all folders, and make sure everything works (sanity)
        _test = fileter.FilesIterator()
        _test.add_folder("test_dir")
        self.__test_iterator(_test, ['test_dir/0_a', 'test_dir/0_b', 'test_dir/0_c.txt',
                                     'test_dir/depth1/1_a', 'test_dir/depth1/1_b.exe',
                                     'test_dir/depth1/depth2/2_a', 'test_dir/depth1/depth2/bar.txt',
                                     'test_dir/depth1/depth2/depth3/3',
                                     'test_dir/foo/bar.txt'])

        # now add extension filter to return just txt files
        _test.add_filter_by_regex(".*\.txt")
        self.__test_iterator(_test, ['test_dir/0_c.txt', 'test_dir/depth1/depth2/bar.txt',
                                     'test_dir/foo/bar.txt'])
