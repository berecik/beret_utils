import os, pathlib
from unittest import TestCase
from beret_utils.path_data import PathData


class TestPath(TestCase):
    def setUp(self):
        self.dir = PathData.main()
        self.parent_dir = PathData.main(depth=1)

    def test_path(self):
        file = __file__
        absolute_file = os.path.abspath(file)
        absolute_file_path = pathlib.Path(absolute_file)
        self.assertEqual(absolute_file, str(self.dir('test_path.py')))
        self.assertEqual(absolute_file_path, self.dir('test_path.py').path)

    def test_parent_path(self):
        file = __file__
        absolute_dir = os.path.abspath(os.path.dirname(file))
        parent_dir = os.path.dirname(absolute_dir)
        test_parent_path = os.path.join(parent_dir, 'TEST')
        self.assertEqual(PathData(test_parent_path), self.parent_dir('TEST'))

    def test_iterator(self):
        files = [file for file in self.dir(ls_patterns='*.txt', ls_recursive=True)]
        file_one = os.path.join('subdir', 'test.txt')
        file_two = os.path.join('subdir', 'subdir', 'test.txt')
        path_one = PathData(file_one)
        path_two = PathData(file_two)
        self.assertEqual(2, len(files))
        self.assertIn(path_one, files)
        self.assertIn(path_two, files)

    def test_ls(self):
        files = self.dir('subdir').ls('*.txt')
        file_one = self.dir('subdir', 'test.txt')
        file_two = self.dir('subdir', 'subdir', 'test.txt')
        self.assertEqual(1, len(files))
        self.assertIn(file_one, files)
        self.assertNotIn(file_two, files)

    def test_ls_recursive(self):
        files = self.dir.ls('*.txt', recursive=True)
        file_one = self.dir('subdir', 'test.txt')
        file_two = self.dir('subdir', 'subdir', 'test.txt')
        self.assertEqual(2, len(files))
        self.assertIn(file_one, files)
        self.assertIn(file_two, files)


class TestPathIterator(TestCase):
    def setUp(self):
        self.get_path = PathData.main(depth=1)

    def test_all_files(self):
        test_dir = self.get_path('tests', ls_recursive=True, ls_patterns='*.txt')
        files = [file for file in test_dir]
        file_one = self.get_path('tests', 'subdir', 'test.txt')
        file_two = self.get_path('tests', 'subdir', 'subdir', 'test.txt')
        self.assertEqual(2, len(files))
        self.assertIn(file_one, files)
        self.assertIn(file_two, files)