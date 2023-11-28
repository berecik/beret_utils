__author__ = 'beret'

from threading import local

# to fix Django >= 1.10
try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

import urllib

_local = local()


class GlobalRequestMiddleware(MiddlewareMixin):
    def process_request(self, request):
        _local.request = request


def get_current_request():
    return getattr(_local, "request", None)


def get_current_user():
    request = get_current_request()
    if request and request.user:
        return request.user


def get_current_state():
    request = get_current_request()
    return urllib.urlencode(request.GET)


def get_client_ip(request=None):
    if not request:
        request = get_current_request()
    remote_address = request.META.get('REMOTE_ADDR')
    # set the default value of the ip to be the REMOTE_ADDR if available
    # else None
    ip = remote_address
    # try to get the first non-proxy ip (not a private ip) from the
    # HTTP_X_FORWARDED_FOR
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        proxies = x_forwarded_for.split(',')
        PRIVATE_IPS_PREFIX = ('10.', '172.', '192.', '127.')
        # remove the private ips from the beginning
        while (len(proxies) > 0 and
               proxies[0].startswith(PRIVATE_IPS_PREFIX)):
            proxies.pop(0)
        # take the first ip which is not a private one (of a proxy)
        if len(proxies) > 0:
            ip = proxies[0]

    return ip
