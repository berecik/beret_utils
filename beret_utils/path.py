import os


def get_path(depth=0):

    BASE_DIR = os.getcwd()
    for i in range(depth):
        BASE_DIR = os.path.dirname(BASE_DIR)

    def __get_path(file_name):
        file_name = os.path.expandvars(file_name)
        if file_name[0] != '/':
            return os.path.join(BASE_DIR, file_name)
        return file_name

    return __get_path
