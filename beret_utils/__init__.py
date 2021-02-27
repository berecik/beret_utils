import math
import json
import pprint

from .bereTools import *
from .config import get_config, EnvValue, join_path_value, join_path
from .imap import Imap
from .path import get_path_fun
from .patterns import match
from .singleton import Singleton
from .tail_recursion import tail_call_optimized
from .trace import info
from .trace import log_fun

SEND_TO_COUT = True
_pp = pprint.PrettyPrinter(indent=2)


def try_int(data, default=None):
    try:
        if isinstance(data, (list, tuple)):
            return try_int(data[0], default)
        return int(data)
    except Exception:
        return default


def get_pp(*args, **kwargs):
    __p = p(*args, **kwargs)

    def __pp(*datas):
        return __p(*datas)

    return __pp


def pp(txt, parse=None, cout=SEND_TO_COUT, string=None):
    if string is None:
        string = not cout
    if parse == 'json':
        _txt = json.loads(txt)
    elif parse:
        _txt = parse(txt)
    else:
        _txt = txt
    if cout:
        _pp.pprint(_txt)
    if string:
        return _pp.pformat(_txt)


def p(parse=None, cout=SEND_TO_COUT, **kwargs):
    def __pp(*txts):
        return [pp(txt=txt, parse=parse, cout=cout, **kwargs) for txt in txts]
    return __pp


def jprint(json_txt, cout=SEND_TO_COUT):
    return pp(txt=json_txt, parse='json', cout=cout)


def del_key(dict, key):
    if key in dict:
        del dict[key]
        return True
    return False


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
