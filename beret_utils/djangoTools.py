# -*- coding: utf-8 -*-
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


def _get_write(f):
    if f:
        _debug_file = open(DEBUG_FILE, 'a') if f == True else f
        return _debug_file.write
    return False


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def env(fun):
    def _fun_wrap(*args, **kwargs):
        import os
        import sys

        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coderside.settings")
        sys.path.append(BASE_DIR)

        return fun(*args, **kwargs)

    return _fun_wrap
