import math

from .bereTools import addLine
from .bereTools import all_files
from .bereTools import div
from .bereTools import getchar
from .bereTools import isFloat
from .bereTools import makeFindFun
from .bereTools import makeFun
from .bereTools import replace
from .bereTools import tags
from .bereTools import today
from .bereTools import toType
from .bereTools import url2txt
from .config import EnvValue
from .config import get_config
from .imap import Imap
from .path import get_path
from .patterns import match
from .singleton import Singleton
from .tail_recursion import tail_call_optimized
from .trace import info
from .trace import log_fun


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

    if isNan(val) or isInf(val):
        return None

    return val
