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
        files = [file for file in self.dir(patterns='*.txt', recursive=True)]
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
        file_path_data = self.dir(file_name)
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
        self.get_path = PathData.main(depth=1)

    def test_txt_files(self):
        test_dir = self.get_path('tests', recursive=True, patterns='*.txt')
        files = [file for file in test_dir]
        file_one = self.get_path('tests', 'subdir', 'test.txt')
        file_two = self.get_path('tests', 'subdir', 'subdir', 'test.txt')
        self.assertEqual(2, len(files))
        self.assertIn(file_one, files)
        self.assertIn(file_two, files)

    def test_all_files(self):
        test_dir = self.get_path('tests', recursive=True, filters=False)
        files = [file for file in test_dir]
        file_one = self.get_path('tests', 'subdir', 'test.txt')
        file_two = self.get_path('tests', 'subdir', 'subdir', 'test.txt')
        dir_one = self.get_path('tests', 'subdir')
        dir_two = self.get_path('tests', 'subdir', 'subdir')
        self.assertEqual(14, len(files))
        self.assertIn(file_one, files)
        self.assertIn(file_two, files)
        self.assertIn(dir_one, files)
        self.assertIn(dir_two, files)

    def test_all_files_no_dirs(self):
        test_dir = self.get_path('tests', recursive=True, dirs=False, filters=False)
        files = [file for file in test_dir]
        file_one = self.get_path('tests', 'subdir', 'test.txt')
        file_two = self.get_path('tests', 'subdir', 'subdir', 'test.txt')
        dir_one = self.get_path('tests', 'subdir')
        dir_two = self.get_path('tests', 'subdir', 'subdir')
        self.assertEqual(11, len(files))
        self.assertIn(file_one, files)
        self.assertIn(file_two, files)
        self.assertNotIn(dir_one, files)
        self.assertNotIn(dir_two, files)

    def test_all_files_dirs_only(self):
        test_dir = self.get_path('tests', recursive=True, dirs_only=True, filters=False)
        files = [file for file in test_dir]
        file_one = self.get_path('tests', 'subdir', 'test.txt')
        file_two = self.get_path('tests', 'subdir', 'subdir', 'test.txt')
        dir_one = self.get_path('tests', 'subdir')
        dir_two = self.get_path('tests', 'subdir', 'subdir')
        self.assertEqual(3, len(files))
        self.assertNotIn(file_one, files)
        self.assertNotIn(file_two, files)
        self.assertIn(dir_one, files)
        self.assertIn(dir_two, files)

    def test_all_files_default_filters(self):
        test_dir = self.get_path('tests', recursive=True, filters=True)
        files = [file for file in test_dir]
        file_one = self.get_path('tests', 'subdir', 'test.txt')
        file_two = self.get_path('tests', 'subdir', 'subdir', 'test.txt')
        dir_one = self.get_path('tests', 'subdir')
        dir_two = self.get_path('tests', 'subdir', 'subdir')
        self.assertEqual(11, len(files))
        self.assertIn(file_one, files)
        self.assertIn(file_two, files)
        self.assertIn(dir_one, files)
        self.assertIn(dir_two, files)

    def test_all_files_no_dirs_default_filters(self):
        test_dir = self.get_path('tests', recursive=True, dirs=False, filters=True)
        files = [file for file in test_dir]
        file_one = self.get_path('tests', 'subdir', 'test.txt')
        file_two = self.get_path('tests', 'subdir', 'subdir', 'test.txt')
        dir_one = self.get_path('tests', 'subdir')
        dir_two = self.get_path('tests', 'subdir', 'subdir')
        self.assertEqual(9, len(files))
        self.assertIn(file_one, files)
        self.assertIn(file_two, files)
        self.assertNotIn(dir_one, files)
        self.assertNotIn(dir_two, files)

    def test_all_files_dirs_only_default_filters(self):
        test_dir = self.get_path('tests', recursive=True, dirs_only=True, filters=True)
        files = [file for file in test_dir]
        file_one = self.get_path('tests', 'subdir', 'test.txt')
        file_two = self.get_path('tests', 'subdir', 'subdir', 'test.txt')
        dir_one = self.get_path('tests', 'subdir')
        dir_two = self.get_path('tests', 'subdir', 'subdir')
        self.assertEqual(2, len(files))
        self.assertNotIn(file_one, files)
        self.assertNotIn(file_two, files)
        self.assertIn(dir_one, files)
        self.assertIn(dir_two, files)

    def test_all_files_no_hidden(self):
        test_dir = self.get_path('tests', recursive=True, filters=["!is_hidden"])
        files = [file for file in test_dir]
        file_one = self.get_path('tests', 'subdir', 'test.txt')
        file_two = self.get_path('tests', 'subdir', 'subdir', 'test.txt')
        dir_one = self.get_path('tests', 'subdir')
        dir_two = self.get_path('tests', 'subdir', 'subdir')
        self.assertEqual(11, len(files))
        self.assertIn(file_one, files)
        self.assertIn(file_two, files)
        self.assertIn(dir_one, files)
        self.assertIn(dir_two, files)

    def test_all_files_no_dirs_no_hidden(self):
        test_dir = self.get_path('tests', recursive=True, filters=["!is_hidden", "!is_dir"])
        files = [file for file in test_dir]
        file_one = self.get_path('tests', 'subdir', 'test.txt')
        file_two = self.get_path('tests', 'subdir', 'subdir', 'test.txt')
        dir_one = self.get_path('tests', 'subdir')
        dir_two = self.get_path('tests', 'subdir', 'subdir')
        self.assertEqual(9, len(files))
        self.assertIn(file_one, files)
        self.assertIn(file_two, files)
        self.assertNotIn(dir_one, files)
        self.assertNotIn(dir_two, files)

    def test_all_files_dirs_only_no_hidden(self):
        test_dir = self.get_path('tests', recursive=True, dirs_only=True, filters=["!is_hidden", "is_dir"])
        files = [file for file in test_dir]
        file_one = self.get_path('tests', 'subdir', 'test.txt')
        file_two = self.get_path('tests', 'subdir', 'subdir', 'test.txt')
        dir_one = self.get_path('tests', 'subdir')
        dir_two = self.get_path('tests', 'subdir', 'subdir')
        self.assertEqual(2, len(files))
        self.assertNotIn(file_one, files)
        self.assertNotIn(file_two, files)
        self.assertIn(dir_one, files)
        self.assertIn(dir_two, files)