import datetime
import fnmatch
import mimetypes
import os
import pathlib
from dataclasses import dataclass, replace
from functools import cached_property
from typing import Iterable
from typing import Optional
from typing import TypeVar
from typing import Union


PATH_DATA_CLASS = TypeVar('PATH_DATA_CLASS', bound='PathData')


@dataclass
class PathData(os.PathLike):
    """
    Object representing all data related with data.
    """

    file_path: Union[str, os.PathLike] = None
    file_name: Optional[str] = None
    ls_patterns: Union[str, Iterable[str]] = "*"
    ls_dirs: bool = True
    ls_dirs_only: bool = False
    ls_recursive: bool = False
    depth: int = 0

    def __post_init__(self):

        if self.file_path is str:
            self.file_path = os.path.expandvars(self.file_path)

        while self.depth:
            self.file_path = os.path.dirname(self.file_path)
            self.depth -= 1

        self.file_path = pathlib.Path(self.abspath)

    @classmethod
    def home(cls, *args, **kwargs):
        file_path = pathlib.Path.home()
        return cls(file_path, *args, **kwargs)

    @classmethod
    def root(cls, *args, **kwargs):
        file_path = pathlib.Path("/")
        return cls(file_path, *args, **kwargs)

    @classmethod
    def main(cls, *args, **kwargs):
        file_path = os.getcwd()
        return cls(file_path, *args, **kwargs)

    def dir(self, *args, **kwargs):
        file_path = os.path.dirname(self)
        return __class__(file_path, *args, **kwargs)

    def __call__(self, *paths: Union[str, Iterable[str]], **options: dict) -> PATH_DATA_CLASS:
        """
        :param paths: one file path or list of file path's elements
        Return absolute path of give file in context of base dir.
        """
        if len(paths) == 1 and paths[0] and len(paths[0]):
            if isinstance(paths[0], str):
                "if is one argument, and it is a string, get it as file_name"
                file_name = paths[0]
                if file_name[0] != '/':
                    file_name = self.join(file_name)
            else:
                "if is one argument, and it is not a string, get it as argument list to join"
                file_name = self.join(paths[0])
        else:
            file_name = self.join(*paths)

        options["file_name"] = options.get("file_name")

        return replace(self, file_path=file_name, **options)

    def __fspath__(self) -> str:
        """for PathLike interface"""
        return self.abspath

    def __hash__(self) -> int:
        return hash(self.__fspath__())

    def __str__(self):
        return self.abspath

    @cached_property
    def path(self) -> pathlib.Path:
        return pathlib.Path(self.file_path)

    @cached_property
    def abspath(self) -> str:
        return os.path.abspath(self.file_path)

    @cached_property
    def name(self) -> str:
        return self.file_name or self.path.name

    @cached_property
    def is_dir(self) -> bool:
        return self.path.is_dir()

    @cached_property
    def created_at(self) -> Optional[datetime.datetime]:
        try:
            system_time = self.path.stat().st_ctime
            return datetime.datetime.fromtimestamp(system_time)
        except Exception as _:
            return None

    @cached_property
    def change_at(self) -> Optional[datetime.datetime]:
        try:
            system_time = self.path.stat().st_mtime
            return datetime.datetime.fromtimestamp(system_time)
        except Exception as _:
            return None

    @cached_property
    def size(self) -> int:
        try:
            file_size = os.path.getsize(self)
        except:
            file_size = 0
        return file_size

    @cached_property
    def mime_type(self):
        return mimetypes.guess_type(self.path)[0]

    @cached_property
    def is_hidden(self) -> bool:
        return False

    @cached_property
    def pwd(self):
        """
        Return absolute path of base directory
        """
        return self.abspath

    def join(self, *paths) -> str:
        return os.path.join(self.abspath, *paths)

    def iterator(self, patterns: Union[str, Iterable[str]] = None, **options) -> Iterable[PATH_DATA_CLASS]:
        """
        :param patterns: patterns as a list or in string separate by ';'
        :param self.ls_patterns: default '*', default patterns value
        :yield: PathData object for each file

        Return files in given directory where names pass one of given patterns
        as a default return all files pass one from pattern list.
        """

        assert self.is_dir

        patterns = patterns or self.ls_patterns

        if isinstance(patterns, str):
            patterns = patterns.split(';')

        for path in self.all(**options):
            name = path.name
            for pattern in patterns:
                if fnmatch.fnmatch(name, pattern):
                    yield __class__(path)
                    break

    def all(
            self,
            dirs: bool = None,
            dirs_only: bool = None,
            recursive: bool = None,
    ) -> Iterable[os.PathLike]:
        """
        :param recursive: walk recursively through subdirectories
        :param dirs: yield directories too
        :param dirs_only: yield only directories
        :yield: name of each file

        Return directory names.
        """

        assert self.is_dir

        dirs = self.ls_dirs if dirs is None else dirs
        dirs_only = self.ls_dirs_only if dirs_only is None else dirs_only
        recursive = self.ls_recursive if recursive is None else recursive

        dirs_list: list[PATH_DATA_CLASS] = [self]

        while dirs_list:
            dir = dirs_list.pop()
            assert dir.is_dir
            for path in dir.path.iterdir():
                if path.is_dir():
                    if recursive:
                        dirs_list.append(__class__(path))
                    if not dirs:
                        continue
                else:
                    if dirs_only:
                        continue
                yield path

    def __iter__(self) -> Iterable[PATH_DATA_CLASS]:
        return self.iterator()

    def ls(self, patterns: Union[str, Iterable[str]] = None, **options) -> Optional[list[PATH_DATA_CLASS]]:
        return list(self.iterator(patterns, **options)) if self.is_dir else None


