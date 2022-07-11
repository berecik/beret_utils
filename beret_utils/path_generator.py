import os
from dataclasses import dataclass
from typing import Iterable
from typing import TypeVar
from typing import Union
from .path_data import PathData


def all_files(root: str, patterns: str = "*", single_level: bool = False, yield_folders: bool = False) -> Iterable[str]:
    """return all files in given directory"""
    root_dir = PathGenerator(root)
    return root_dir.ls(
            patterns=patterns,
            recursive=not single_level,
            dirs=yield_folders
        )


DIR_CLASS = TypeVar('DIR_CLASS', bound='Dir')


@dataclass
class PathGenerator(PathData):
    """
    Special version of PathData, for configuration tasks.
    As a function return a string value of unique absolute paths of file.
    As a iterator returns a string value of absolute paths of contained files.
    """

    dirs: bool = False
    dirs_only: bool = False
    recursive: bool = True

    def __call__(self, *args, **kwargs) -> str:
        return str(self.get_dir(*args, **kwargs))

    def ls(self, patterns: Union[str, Iterable[str]] = None, **options) -> Iterable[str]:
        iterator = super().iterator(patterns, **options)
        if not iterator:
            return iterator
        return [str(obj) for obj in iterator]

    def get_dir(self, *args, **kwargs) -> DIR_CLASS:
        return super().__call__(*args, **kwargs)


def get_dir(file=None, *args, **kwargs):
    if file is None:
        return PathGenerator.main(*args, **kwargs)
    else:
        return PathGenerator(file, *args, **kwargs)


def get_home():
    return PathGenerator.home()
