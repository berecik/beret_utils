import os


def get_path(i=0):
    if i > 0:
        def __wrap(file_name):
            __get_path = get_path(i-1)
            path = __get_path(file_name)
            return os.path.dirname(path)
        return __wrap

    BASE_DIR = os.getcwd()

    def __get_path(file_name):
        file_name = os.path.expandvars(file_name)
        if file_name[0] != '/':
            return os.path.join(BASE_DIR, file_name)
        return file_name

    return __get_path
