# -*- coding: utf-8 -*-

import json
import os
import pprint

__author__ = 'beret'

try:
    from django.conf import settings

    BASE_DIR = settings.BASE_DIR
    DEBUG_FILE = getattr(settings, 'DEBUG_FILE', os.path.join(BASE_DIR, '_debug_log.log'))
except ImportError:
    BASE_DIR = os.path.join(os.path.abspath(__file__), '..')
    DEBUG_FILE = os.path.join(BASE_DIR, '_debug_log.log')

_cout = True
_pp = pprint.PrettyPrinter(indent=2)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def try_int(data, default=None):
    try:
        if isinstance(data, (list, tuple)):
            return try_int(data[0], default)
        return int(data)
    except Exception:
        return default


def _get_write(f):
    if f:
        _debug_file = open(DEBUG_FILE, 'a') if f == True else f
        return _debug_file.write
    return False


def get_pp(*args, **kwargs):
    __p = p(*args, **kwargs)

    def __pp(*datas):
        return __p(*datas)

    return __pp


def pp(txt, parse=None, cout=_cout, f=True, string=None):
    if string is None:
        string = not cout
    if parse == 'json':
        _txt = json.loads(txt)
    elif parse:
        _txt = parse(txt)
    else:
        _txt = txt
    w = _get_write(f)
    if w:
        w(_txt)
    if cout:
        _pp.pprint(_txt)
    if string:
        return _pp.pformat(_txt)


def p(parse=None, cout=_cout, f=True, **kwargs):
    def __pp(*txts):
        return [pp(txt=txt, parse=parse, cout=cout, f=f, **kwargs) for txt in txts]

    return __pp


def jprint(json_txt, f=False):
    cout = False if f else True
    return pp(txt=json_txt, parse='json', cout=cout, f=f)


def del_key(dict, key):
    if key in dict:
        del dict[key]
        return True
    return False


def env(fun):
    def _fun_wrap(*args, **kwargs):
        import os
        import sys

        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coderside.settings")
        sys.path.append(BASE_DIR)

        return fun(*args, **kwargs)

    return _fun_wrap
