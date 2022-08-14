import os
from unittest import TestCase

from beret_utils import all_files
from beret_utils import get_dir


class TestDir(TestCase):
    def setUp(self):
        self.dir = get_dir()
        self.parent_dir = get_dir(depth=1)

    def test_path(self):
        file = __file__
        absolute_file = os.path.abspath(file)
        self.assertEqual(absolute_file, self.dir('test_dir.py'))

    def test_parent_path(self):
        file = __file__
        absolute_dir = os.path.abspath(os.path.dirname(file))
        parent_dir = os.path.dirname(absolute_dir)
        test_parent_path = os.path.join(parent_dir, 'TEST')
        self.assertEqual(test_parent_path, self.parent_dir('TEST'))

    def test_ls(self):
        files = self.dir.ls(patterns='*.txt', recursive=True)
        file_one = os.path.join('testdir/subdir', 'test.txt')
        file_two = os.path.join('testdir/subdir', 'subdir', 'test.txt')
        self.assertEqual(2, len(files))
        self.assertIn(os.path.abspath(file_one), files)
        self.assertIn(os.path.abspath(file_two), files)

    def test_ls_paths(self):
        files = self.dir.ls('*.txt')
        file_one = self.dir('testdir', 'subdir', 'test.txt')
        file_two = self.dir('testdir', 'subdir', 'subdir', 'test.txt')
        self.assertEqual(2, len(files))
        self.assertIn(file_one, files)
        self.assertIn(file_two, files)


class TestAllFiles(TestCase):
    def setUp(self):
        self.get_path = get_dir(depth=1)

    def test_all_files(self):
        test_dir = self.get_path('tests')
        files = [file for file in all_files(test_dir, patterns='*.txt')]
        file_one = self.get_path('tests', 'testdir', 'subdir', 'test.txt')
        file_two = self.get_path('tests', 'testdir', 'subdir', 'subdir', 'test.txt')
        self.assertEqual(2, len(files))
        self.assertIn(str(file_one), files)
        self.assertIn(str(file_two), files)
