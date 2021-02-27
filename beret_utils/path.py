import os
import fnmatch


def get_path_fun(depth=0):
    _dir = os.getcwd()
    while depth:
        _dir = os.path.dirname(_dir)
        depth -= 1
    BASE_DIR = _dir

    def __get_path(*paths):
        file_name = None
        if len(paths) == 1:
            if isinstance(paths[0], str):
                "if is one argument, and it is a string, get it as file_name"
                file_name = paths[0]
            else:
                "if is one argument, and it is not a string, get it as argument list to join"
                paths = paths[0]

        if file_name is None:
            file_name = os.path.join(*paths)

        file_name = os.path.expandvars(file_name)
        if file_name[0] != '/':
            return os.path.join(BASE_DIR, file_name)
        return os.path.abspath(file_name)

    return __get_path


def all_files(root, patterns="*", single_level=False, yield_folders=False):
    """return all files in given directory"""
    patterns = patterns.split(';')
    for path, subdirs, files in os.walk(root):
        if yield_folders:
            files.extend(subdirs)
        files.sort()
        for name in files:
            for pattern in patterns:
                if fnmatch.fnmatch(name, pattern):
                    yield os.path.join(path, name)
                    break
        if single_level:
            break
