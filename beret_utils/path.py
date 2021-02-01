import os


def path_fun(depth=0):

    BASE_DIR = os.getcwd()
    for _ in range(depth):
        BASE_DIR = os.path.dirname(BASE_DIR)

    def __get_path(file_name):
        file_name = os.path.expandvars(file_name)
        if file_name[0] != '/':
            return os.path.join(BASE_DIR, file_name)
        return os.path.abspath(file_name)

    return __get_path
