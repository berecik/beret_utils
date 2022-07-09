import os
from dataclasses import dataclass
from typing import Iterable
from typing import TypeVar
from typing import Union
from .path_data import PathData


def all_files(root: str, patterns: str = "*", single_level: bool = False, yield_folders: bool = False) -> Iterable[str]:
    """return all files in given directory"""
    root_dir = Dir(root)
    return root_dir.ls(
            patterns=patterns,
            recursive=not single_level,
            dirs=yield_folders
        )


DIR_CLASS = TypeVar('DIR_CLASS', bound='Dir')


@dataclass
class Dir(PathData):
    """
    Special version of PathData, for configuration tasks.
    As a function return unique absolute paths of file.
    As a iterator returns absolute paths of contained files.
    """

    dirs: bool = False
    dirs_only: bool = False
    recursive: bool = True

    def __call__(self, *args, **kwargs) -> str:
        return str(self.get_dir(*args, **kwargs))

    def ls(self, patterns: Union[str, Iterable[str]] = None, **options) -> Iterable[str]:
        return [str(obj) for obj in super().iterator(patterns, **options)]

    def get_dir(self, *args, **kwargs) -> DIR_CLASS:
        return super().__call__(*args, **kwargs)


def get_dir(file=None, *args, **kwargs):
    if file is None:
        return Dir.main(*args, **kwargs)
    else:
        return Dir(file, *args, **kwargs)


def get_home():
    return Dir.home()
