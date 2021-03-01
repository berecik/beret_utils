import os
from unittest import TestCase
from beret_utils.path import get_path_fun
from beret_utils.path import all_files


class TestPath(TestCase):
    def setUp(self):
        self.get_path = get_path_fun()
        self.get_parent = get_path_fun(1)

    def test_path(self):
        file = __file__
        absolute_file = os.path.abspath(file)
        self.assertEqual(absolute_file, self.get_path('test_path.py'))

    def test_parent_path(self):
        file = __file__
        absolute_dir = os.path.abspath(os.path.dirname(file))
        parent_dir = os.path.dirname(absolute_dir)
        test_parent_path = os.path.join(parent_dir, 'TEST')
        self.assertEqual(test_parent_path, self.get_parent('TEST'))


class TestAllFiles(TestCase):
    def setUp(self):
        self.get_path = get_path_fun(1)

    def test_all_files(self):
        test_dir = self.get_path('tests')
        files = [file for file in all_files(test_dir, patterns='*.txt')]
        file_one = self.get_path('tests', 'subdir', 'test.txt')
        file_two = self.get_path('tests', 'subdir', 'subdir', 'test.txt')
        self.assertEqual(2, len(files))
        self.assertIn(file_one, files)
        self.assertIn(file_two, files)
