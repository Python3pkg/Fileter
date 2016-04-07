#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for the file filters.
"""
import fileter
import unittest


class TestSources(unittest.TestCase):
    """
    Unittests to test file sources.
    """

    def _list_by_iter(self, source):
        """
        this helper function iterate over a source and return a list with all files in it.
        basically convert from source to list of files using for x in y syntax.
        """
        iter_ret = []
        for i in source:
            iter_ret.append(i)
        return iter_ret

    def __fix_sep(self, values):
        """
        Unify path separators to match win/linux shenanigans.
        We just replace all separators to be /
        """
        return [i.replace("\\", "/") for i in values]

    def __test_source(self, source, expected):
        """
        Test a given files source with all methods - by get_all() and by iteration.
        """
        expected = self.__fix_sep(expected)
        self.assertListEqual(self.__fix_sep(source.get_all()), expected)
        self.assertListEqual(self.__fix_sep(self._list_by_iter(source)), expected)

    def test_creating_source(self):
        """
        Testing creation of a basic filter.
        """
        # create a custom source
        class TestSource(fileter.sources.SourceAPI):
            def next(self):
                yield "1"
                yield "2"
                raise StopIteration
        _test = TestSource()

        # test getting all files in source as list
        self.__test_source(_test, ["1", "2"])

    def test_file_source(self):
        """
        Test the basic file(s) source.
        """
        # basic file source with a single file
        _test = fileter.sources.FileSource("test.exe")
        self.__test_source(_test, ["test.exe"])

        # file source with a list of files
        _test = fileter.sources.FileSource(["test.exe", "foo.bar"])
        self.__test_source(_test, ["test.exe", "foo.bar"])

    def test_folder_source(self):
        """
        Test the folder source.
        Take a look at test_dir for expected values.
        """
        # iterate files with a single depth level
        _test = fileter.sources.FolderSource("test_dir", 0)
        self.__test_source(_test, ['test_dir/0_a', 'test_dir/0_b', 'test_dir/0_c.txt'])

        # iterate files with a 1-depth level
        _test = fileter.sources.FolderSource("test_dir", 1)
        self.__test_source(_test, ['test_dir/0_a', 'test_dir/0_b', 'test_dir/0_c.txt',
                                   'test_dir/depth1/1_a', 'test_dir/depth1/1_b.exe',
                                   'test_dir/foo/bar.txt'])

        # iterate files without depth limit
        _test = fileter.sources.FolderSource("test_dir")
        self.__test_source(_test, ['test_dir/0_a', 'test_dir/0_b', 'test_dir/0_c.txt',
                                   'test_dir/depth1/1_a', 'test_dir/depth1/1_b.exe',
                                   'test_dir/depth1/depth2/2_a', 'test_dir/depth1/depth2/bar.txt',
                                   'test_dir/depth1/depth2/depth3/3',
                                   'test_dir/foo/bar.txt'])

        # iterate *folders* with unlimited depth level
        _test = fileter.sources.FolderSource("test_dir", ret_files=False, ret_folders=True)
        self.__test_source(_test, ['test_dir', 'test_dir/depth1', 'test_dir/depth1/depth2',
                                   'test_dir/depth1/depth2/depth3', 'test_dir/foo'])

        # iterate *folders and files* with a single depth level
        _test = fileter.sources.FolderSource("test_dir", depth_limit=0, ret_files=True, ret_folders=True)
        self.__test_source(_test, ['test_dir', 'test_dir/0_a', 'test_dir/0_b', 'test_dir/0_c.txt'])

    def test_filtered_folder_source(self):
        """
        Test the filtered folders source.
        Take a look at test_dir for expected values.
        """
        # filter only things inside "depth1" folder.
        _test = fileter.sources.FilteredFolderSource("test_dir", ".*depth1.*")
        self.__test_source(_test, ['test_dir/depth1/1_a', 'test_dir/depth1/1_b.exe',
                                   'test_dir/depth1/depth2/2_a', 'test_dir/depth1/depth2/bar.txt',
                                   'test_dir/depth1/depth2/depth3/3'])

        # filter out directories that have '3' in their name, eg "depth3"
        _test = fileter.sources.FilteredFolderSource("test_dir", "(?!^.*depth3.*$).*")
        self.__test_source(_test, ['test_dir/0_a', 'test_dir/0_b', 'test_dir/0_c.txt',
                                   'test_dir/depth1/1_a', 'test_dir/depth1/1_b.exe',
                                   'test_dir/depth1/depth2/2_a', 'test_dir/depth1/depth2/bar.txt',
                                   'test_dir/foo/bar.txt'])

        # filter only things inside "depth1" folder, but only with 1 depth level.
        _test = fileter.sources.FilteredFolderSource("test_dir", ".*depth1.*", 1)
        self.__test_source(_test, ['test_dir/depth1/1_a', 'test_dir/depth1/1_b.exe'])

        # iterate *folders* with unlimited depth level
        _test = fileter.sources.FilteredFolderSource("test_dir", ".*depth1.*", ret_files=False, ret_folders=True)
        self.__test_source(_test, ['test_dir/depth1', 'test_dir/depth1/depth2', 'test_dir/depth1/depth2/depth3'])

        # iterate *folders and files* with a single depth level
        _test = fileter.sources.FilteredFolderSource("test_dir", ".*test_dir.*", depth_limit=0,
                                                     ret_files=True, ret_folders=True)
        self.__test_source(_test, ['test_dir', 'test_dir/0_a', 'test_dir/0_b', 'test_dir/0_c.txt'])

    def test_pattern_source(self):
        """
        Test the pattern files source.
        Take a look at test_dir for expected values.
        """
        # only files inside "depth1" folder.
        _test = fileter.sources.PatternSource("*depth1*", "test_dir")
        self.__test_source(_test, ['test_dir/depth1/1_a', 'test_dir/depth1/1_b.exe',
                                   'test_dir/depth1/depth2/2_a', 'test_dir/depth1/depth2/bar.txt',
                                   'test_dir/depth1/depth2/depth3/3'])

        # only files in depth 2
        _test = fileter.sources.PatternSource("*/depth2/*", "test_dir")
        self.__test_source(_test, ['test_dir/depth1/depth2/2_a', 'test_dir/depth1/depth2/bar.txt',
                                   'test_dir/depth1/depth2/depth3/3'])

        # filter exe file in 1 level deep
        _test = fileter.sources.PatternSource("*.exe", "test_dir", 1)
        self.__test_source(_test, ['test_dir/depth1/1_b.exe'])
