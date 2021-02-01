from .bereTools import today, addLine, all_files, div, getchar, isFloat, makeFindFun, makeFun, replace, tags, toType, url2txt

from .tail_recursion import tail_call_optimized

from .imap import Imap

from .trace import log_fun, info

from .patterns import match
import math

from .singleton import Singleton
from .tail_recursion import tail_call_optimized
from .path import get_path
from .config import get_config, EnvValue


def none_on_error(fun):

    def __wrap_fun(*args, **kwargs):
        try:
            return fun(*args, **kwargs)
        except Exception as e:
            fun.error = e
            return None

    return __wrap_fun


def isNan(val):
    try:
        return math.isnan(val)
    except TypeError:
        return False


def isInf(val):
    try:
        return math.isinf(val)
    except TypeError:
        return False


def parse_float(val):

    val = float(val)

    if isNan(val):
        return None
    elif isInf(val):
        return None

    return val