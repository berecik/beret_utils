import os, pathlib
from unittest import TestCase
from beret_utils.path_data import PathData


class TestPath(TestCase):
    def setUp(self):
        self.dir = PathData.main('testdir')
        self.parent_dir = self.dir.parent

    def test_path(self):
        file = __file__
        absolute_file = os.path.abspath(file)
        absolute_file_path = pathlib.Path(absolute_file)
        self.assertEqual(absolute_file, str(self.parent_dir('test_path.py')))
        self.assertEqual(absolute_file_path, self.parent_dir('test_path.py').path)

    def test_parent_path(self):
        file = __file__
        absolute_dir = os.path.abspath(os.path.dirname(file))
        parent_dir = os.path.dirname(absolute_dir)
        test_parent_path = os.path.join(parent_dir, 'TEST')
        test_parent_dir = self.parent_dir.parent('TEST')
        self.assertTrue(test_parent_dir == test_parent_path)

    def test_iterator(self):
        files = self.dir(patterns='*.txt', recursive=True)
        file_one = os.path.join('testdir/subdir', 'test.txt')
        file_two = os.path.join('testdir/subdir', 'subdir', 'test.txt')
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

    def test_home(self):
        home_path = os.path.abspath(pathlib.Path.home())
        home_path_data = os.path.abspath(PathData.home())
        home_expand_env = os.path.abspath(PathData("$HOME"))
        self.assertEqual(home_path, home_path_data)
        self.assertEqual(home_path, home_expand_env)

    def test_name(self):
        file_name = 'test_path.py'
        file_path_data = self.dir(file_name)
        self.assertEqual(file_name, file_path_data.name)
        self.assertEqual(str, type(file_path_data.name))

    def test_abspath(self):
        file = __file__
        file_name = 'test_path.py'
        absolute_file = os.path.abspath(file)
        file_path_data = self.dir.parent(file_name)
        self.assertEqual(absolute_file, file_path_data.abspath)
        self.assertEqual(str, type(file_path_data.abspath))

    def test_mime_type(self):
        file_name = 'test_path.py'
        file_type = 'text/x-python'
        file_path_data = self.dir(file_name)
        self.assertEqual(file_type, file_path_data.mime_type)
        self.assertEqual(str, type(file_path_data.mime_type))
        file_txt = self.dir('subdir', 'test.txt')
        self.assertEqual('text/plain', file_txt.mime_type)


class TestPathIterator(TestCase):
    def setUp(self):
        self.main_path = PathData.main()
        self.test_dir = self.main_path('testdir', recursive=True, filters=False)
        self.file_one = self.test_dir('subdir', 'test.txt')
        self.file_two = self.test_dir('subdir', 'subdir', 'test.txt')
        self.dir_one = self.test_dir('subdir')
        self.dir_two = self.test_dir('subdir', 'subdir')

    def test_txt_files(self):
        test_dir = self.test_dir(recursive=True, patterns='*.txt')
        self.assertEqual(2, len(test_dir))
        self.assertIn(self.file_one, test_dir)
        self.assertIn(self.file_two, test_dir)

    def test_all_files(self):
        test_dir = self.test_dir(recursive=True, filters=False)
        self.assertEqual(7, len(test_dir))
        self.assertIn(self.file_one, test_dir)
        self.assertIn(self.file_two, test_dir)
        self.assertIn(self.dir_one, test_dir)
        self.assertIn(self.dir_two, test_dir)

    def test_all_files_no_dirs(self):
        test_dir = self.test_dir(recursive=True, dirs=False, filters=False)
        self.assertEqual(4, len(test_dir))
        self.assertIn(self.file_one, test_dir)
        self.assertIn(self.file_two, test_dir)
        self.assertNotIn(self.dir_one, test_dir)
        self.assertNotIn(self.dir_two, test_dir)

    def test_all_files_dirs_only(self):
        test_dir = self.test_dir(recursive=True, dirs_only=True, filters=False)
        self.assertEqual(3, len(test_dir))
        self.assertNotIn(self.file_one, test_dir)
        self.assertNotIn(self.file_two, test_dir)
        self.assertIn(self.dir_one, test_dir)
        self.assertIn(self.dir_two, test_dir)

    def test_all_files_default_filters(self):
        test_dir = self.test_dir(recursive=True, filters=True)
        self.assertEqual(4, len(test_dir))
        self.assertIn(self.file_one, test_dir)
        self.assertIn(self.file_two, test_dir)
        self.assertIn(self.dir_one, test_dir)
        self.assertIn(self.dir_two, test_dir)

    def test_all_files_no_dirs_default_filters(self):
        test_dir = self.test_dir(recursive=True, dirs=False, filters=True)
        self.assertEqual(2, len(test_dir))
        self.assertIn(self.file_one, test_dir)
        self.assertIn(self.file_two, test_dir)
        self.assertNotIn(self.dir_one, test_dir)
        self.assertNotIn(self.dir_two, test_dir)

    def test_all_files_dirs_only_default_filters(self):
        test_dir = self.test_dir(recursive=True, dirs_only=True, filters=True)
        self.assertEqual(2, len(test_dir))
        self.assertNotIn(self.file_one, test_dir)
        self.assertNotIn(self.file_two, test_dir)
        self.assertIn(self.dir_one, test_dir)
        self.assertIn(self.dir_two, test_dir)

    def test_all_files_no_hidden(self):
        test_dir = self.test_dir(recursive=True, filters=["!is_hidden"])
        self.assertEqual(4, len(test_dir))
        self.assertIn(self.file_one, test_dir)
        self.assertIn(self.file_two, test_dir)
        self.assertIn(self.dir_one, test_dir)
        self.assertIn(self.dir_two, test_dir)

    def test_all_files_no_dirs_no_hidden(self):
        test_dir = self.test_dir(recursive=True, filters=["!is_hidden", "!is_dir"])
        self.assertEqual(2, len(test_dir))
        self.assertIn(self.file_one, test_dir)
        self.assertIn(self.file_two, test_dir)
        self.assertNotIn(self.dir_one, test_dir)
        self.assertNotIn(self.dir_two, test_dir)

    def test_all_files_dirs_only_no_hidden(self):
        test_dir = self.test_dir(recursive=True, dirs_only=True, filters=["!is_hidden", "is_dir"])
        self.assertEqual(2, len(test_dir))
        self.assertNotIn(self.file_one, test_dir)
        self.assertNotIn(self.file_two, test_dir)
        self.assertIn(self.dir_one, test_dir)
        self.assertIn(self.dir_two, test_dir)