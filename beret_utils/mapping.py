class MappingDict(dict):

    def __setitem__(self, key, item):
        self.__dict__[key] = item

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        return repr(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __delitem__(self, key):
        del self.__dict__[key]

    def clear(self):
        return self.__dict__.clear()

    def copy(self):
        return self.__dict__.copy()

    def has_key(self, k):
        return k in self.__dict__

    def update(self, *args, **kwargs):
        return self.__dict__.update(*args, **kwargs)

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()

    def pop(self, *args):
        return self.__dict__.pop(*args)

    def __cmp__(self, dict_):
        return self.__cmp__(self.__dict__, dict_)

    def __contains__(self, item):
        return item in self.__dict__

    def __iter__(self):
        return iter(self.__dict__)

    def __str__(self):
        return str(self.__dict__)


class MappingAttrs(MappingDict):

    def __getattr__(self, item):
        return self.__getitem__(item)

    def __setattr__(self, key, value):
        return self.__setitem__(key, value)

    def __delattr__(self, item):
        self.__delitem__(item)

class MappingDictDefault(MappingDict):

    DEFAULT_VALUE = None

    def __getitem__(self, key):
        return self.__dict__[key] if key in self.__dict__ else self.DEFAULT_VALUE


class MappingConst(MappingDictDefault):
    read_only_exception = PermissionError

    def __read_only(self, *args, **kwargs):
        raise self.read_only_exception

    def __init__(self):
        self.clear = self.__read_only
        self.update = self.__read_only
        self.pop = self.__read_only

        self.__delitem__ = self.__read_only
        self.__setitem__ = self.__read_only
        super().__init__()
