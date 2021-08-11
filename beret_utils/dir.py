import fnmatch
import os
from dataclasses import dataclass
from functools import cached_property
from typing import Iterable
from typing import TypeVar
from typing import Union


def all_files(root: str, patterns: str = "*", single_level: bool = False, yield_folders: bool = False) -> Iterable[str]:
    """return all files in given directory"""
    root_dir = Dir(root)
    return root_dir.ls_paths(patterns=patterns, rec=not single_level, dirs=yield_folders)


DIR_CLASS = TypeVar('DIR_CLASS', bound='Dir')


@dataclass
class Dir:
    __base_dir: str

    def __call__(self, *paths: Union[str, Iterable[str]]) -> str:
        """
        :param paths: one file path or list of file path's elements
        Return absolute path of give file in context of base dir.
        """
        if len(paths) == 1:
            if isinstance(paths[0], str):
                "if is one argument, and it is a string, get it as file_name"
                file_name = paths[0]
                if file_name[0] != '/':
                    return self.join(file_name)
            else:
                "if is one argument, and it is not a string, get it as argument list to join"
                paths = paths[0]

        file_name = self.join(*paths)
        file_name = os.path.expandvars(file_name)
        return os.path.abspath(file_name)

    @cached_property
    def pwd(self):
        """
        Return absolute path of base directory
        """
        return os.path.abspath(self.__base_dir)

    def join(self, *paths) -> str:
        return os.path.join(self.__base_dir, *paths)

    def ls_paths(
            self,
            patterns: Union[str, Iterable[str]] = "*",
            rec: bool = True,
            dirs: bool = False,
            dirs_only: bool = False
    ) -> Iterable[str]:
        """
        :param patterns: patterns as a list or in string separate by ';'
        :param patterns: default '*', show all files
        :param rec: walk recursively through subdirectories
        :param dirs: yield directories too
        :yield: absolute path to each file

        Return files in given directory where names pass one of given patterns
        as a default return all files pass one from pattern list.
        """
        if isinstance(patterns, str):
            patterns = patterns.split(';')

        for path, name in self.all(rec=rec, dirs=dirs, dirs_only=dirs_only):
            for pattern in patterns:
                if fnmatch.fnmatch(name, pattern):
                    yield self.join(path, name)
                    break

    def ls(
            self,
            patterns: Union[str, Iterable[str]] = "*",
            rec: bool = False,
            dirs: bool = False,
            dirs_only: bool = False,
    ) -> Iterable[str]:
        """
        :param patterns: patterns as a list or in string separate by ';'
        :param patterns: default '*', show all files
        :param rec: walk recursively through subdirectories
        :param dirs: yield directories too
        :yield: name of each file

        Return files in given directory where names pass one of given patterns
        as a default return all files pass one from pattern list.
        """

        for path in self.ls_paths(patterns=patterns, rec=rec, dirs=dirs, dirs_only=dirs_only):
            reduced_path = path[len(self.__base_dir) + len(os.path.sep):]
            yield reduced_path

    def all(
            self,
            rec: bool = False,
            dirs: bool = False,
            dirs_only: bool = False,
    ) -> Iterable[str]:
        """
        :param rec: walk recursively through subdirectories
        :param dirs: yield directories too
        :yield: name of each file

        Return directory names.
        """

        for path, subdirs, files in os.walk(self.__base_dir):
            if dirs_only:
                files = subdirs
            elif dirs:
                files.extend(subdirs)
            files.sort()
            for name in files:
                yield path, name
            if not rec:
                break

    def get_dir(self, subdir: str) -> DIR_CLASS:
        """
        :param subdir: subdirectory of base directory
        Generate new dir object base on selected subdir of base dir.
        """
        base_subdir = self.join(subdir)
        return self.__class__(base_subdir)

    @cached_property
    def files(self):
        return set(map(lambda path, name: name, self.all(rec=False, dirs=False, dirs_only=False)))

    @cached_property
    def dirs(self):
        return set(map(lambda path, name: name, self.all(rec=False, dirs=False, dirs_only=True)))

    def __str__(self):
        return str(self.pwd)


def get_dir(file=None, depth=0):
    _dir = os.getcwd() if file is None else os.path.dirname(file)
    while depth:
        _dir = os.path.dirname(_dir)
        depth -= 1
    BASE_DIR = _dir

    return Dir(BASE_DIR)
