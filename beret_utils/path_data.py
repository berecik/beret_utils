import datetime
import fnmatch
import mimetypes
import os
import pathlib
from dataclasses import dataclass, replace
from dataclasses import field
from functools import cached_property
from typing import Callable
from typing import Iterable
from typing import Optional
from typing import TypeVar
from typing import Union

try:
    from os import PathLike
except ImportError:  # Python 3.5 support
    from pathlib import PurePath as PathLike

PATH_DATA_CLASS = TypeVar('PATH_DATA_CLASS', bound='PathData')
DEFAULT_FILTERS = [
    lambda obj: not obj.is_hidden
]


@dataclass(order=True)
class PathData(PathLike):
    """
    Object representing all data related with data.
    """

    file_path: Union[str, PathLike] = field(compare=True)
    file_name: Optional[str] = field(compare=False, default=None)
    patterns: Union[str, Iterable[str]] = field(compare=False, default="*")
    dirs: bool = field(compare=False, default=True)
    dirs_only: bool = field(compare=False, default=False)
    recursive: bool = field(compare=False, default=False)
    depth: int = field(compare=False, default=0)
    filters: Union[str, bool, Iterable[Union[Callable[[PATH_DATA_CLASS], bool], str]]] = field(
        compare=False,
        default=False
    )

    def __post_init__(self):

        if isinstance(self.file_path, str):
            self.file_path = os.path.expandvars(self.file_path)

        while self.depth:
            self.file_path = os.path.dirname(self.file_path)
            self.depth -= 1

        # is only one object for each system file.
        self.file_path = self.abspath

        self.parse_filters()

    def parse_filters(self):
        def __parse_filter(filter_data):
            if isinstance(filter_data, str):
                if filter_data[0] == '!':
                    default = False
                    filter_data = filter_data[1:]
                else:
                    default = True
                return lambda obj: default if getattr(obj, filter_data) else not default
            return filter_data
        if isinstance(self.filters, str):
            self.filters = [self.filters]

        elif isinstance(self.filters, bool):
            self.filters = DEFAULT_FILTERS if self.filters else ()

        self.filters = list(map(__parse_filter, self.filters))

    @classmethod
    def home(cls, *args, **kwargs):
        file_path = pathlib.Path.home()
        return cls(file_path, *args, **kwargs)

    @classmethod
    def root(cls, *args, **kwargs):
        file_path = pathlib.Path("/")
        return cls(file_path, *args, **kwargs)

    @classmethod
    def main(cls, *paths, **kwargs):
        file_path = os.getcwd()
        __main = cls(file_path, **kwargs)
        if paths:
            return __main(*paths)
        else:
            return __main

    @cached_property
    def parent(self):
        file_path = os.path.dirname(self)
        return replace(self, file_path=file_path)

    def __call__(self, *paths: Union[str, Iterable[str]], **options: dict) -> PATH_DATA_CLASS:
        """
        paths: one file path or list of file path's elements
        Return absolute path of give file in context of base parent.
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
        """For order"""
        return hash(self.__fspath__())

    def __eq__(self, other):
        return self.__fspath__() == getattr(other, "__fspath__", lambda: other)()

    def __str__(self):
        return self.abspath

    def __iter__(self) -> Iterable[PATH_DATA_CLASS]:
        return self.iterator()

    @cached_property
    def path(self) -> pathlib.Path:
        """Always return path object"""
        return pathlib.Path(self.file_path)

    @cached_property
    def abspath(self) -> str:
        """
        Return absolute path of base directory
        """
        return os.path.abspath(self.file_path)

    @cached_property
    def name(self) -> str:
        return str(self.file_name or self.path.name)

    @cached_property
    def is_dir(self) -> bool:
        return self.path.is_dir()

    @cached_property
    def is_hidden(self) -> bool:
        return self.name[0] == '.'

    @cached_property
    def created_at(self) -> Optional[datetime.datetime]:
        system_time = self.path.stat().st_ctime
        return datetime.datetime.fromtimestamp(system_time)

    @cached_property
    def change_at(self) -> Optional[datetime.datetime]:
        system_time = self.path.stat().st_mtime
        return datetime.datetime.fromtimestamp(system_time)

    @cached_property
    def size(self) -> int:
        file_size = os.path.getsize(self)
        return file_size

    @cached_property
    def mime_type(self):
        return mimetypes.guess_type(self.path)[0]

    def join(self, *paths) -> str:

        if self.is_dir:
            __path = self.path
        else:
            "if is a file, join to parent"
            __path = self.parent.path

        return os.path.join(__path, *paths)

    @cached_property
    def check(self):
        return all(map(lambda filter_: filter_(self), self.filters))

    def iterator(self, patterns: Union[str, Iterable[str]] = None, **options) -> Iterable[PATH_DATA_CLASS]:
        """
        :param patterns: patterns as a list or in string separate by ';'
        :yield: PathData object for each file

        Return files in given directory where names pass one of given patterns
        as a default return all files pass one from pattern list.
        """

        assert self.is_dir

        patterns = patterns or self.patterns

        if isinstance(patterns, str):
            patterns = patterns.split(';')

        for path in self.all(**options):
            name = path.name
            for pattern in patterns:
                if fnmatch.fnmatch(name, pattern):
                    obj = replace(self, file_path=path)
                    if obj.check:
                        yield obj
                    break

    def all(
            self,
            dirs: bool = None,
            dirs_only: bool = None,
            recursive: bool = None,
    ) -> Iterable[PathLike]:
        """
        :param recursive: walk recursively through subdirectories
        :param dirs: yield directories too
        :param dirs_only: yield only directories
        :yield: name of each file

        Return directory names.
        """

        assert self.is_dir

        dirs = self.dirs if dirs is None else dirs
        dirs_only = self.dirs_only if dirs_only is None else dirs_only
        recursive = self.recursive if recursive is None else recursive

        dirs_list: list[PATH_DATA_CLASS] = [self]

        while dirs_list:
            dir_ = dirs_list.pop()
            assert dir_.is_dir
            for path in dir_.path.iterdir():
                if path.is_dir():
                    if recursive:
                        dirs_list.append(replace(dir_, file_path=path))
                    if not dirs:
                        continue
                else:
                    if dirs_only:
                        continue
                yield path

    def ls(self, patterns: Union[str, Iterable[str]] = None, **options) -> Optional[list[PATH_DATA_CLASS]]:
        return list(self.iterator(patterns, **options)) if self.is_dir else None

    def __len__(self):
        if not self.is_dir:
            return None
        assert self.is_dir
        return len(self.ls())
