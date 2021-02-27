#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import urllib

# fixed point Y combinator
Y = (lambda g: (lambda f: g(lambda *arg: f(f)(*arg)))(lambda f: g(lambda *arg: f(f)(*arg))))
# example of using Y combinator to calculate greatest common divisor by euliclean algoritm
# gcd=lambda a,b: a if not b else nwd(b,a%b)
gcd = lambda a, b: Y(lambda f: lambda a, b: not b and a or f(b, a % b))(a, b)
# function for division of rational numbers
div = lambda a, b: (int(a) / int(b), (a % b) / gcd((a % b), b), b / gcd((a % b), b))

anonim_div = lambda a, b: (int(a) / int(b), (a % b) / (
    lambda a, b: (lambda g: (lambda f: g(lambda *arg: f(f)(*arg)))(lambda f: g(lambda *arg: f(f)(*arg))))(
        lambda f: lambda a, b: not b and a or f(b, a % b))(a, b))((a % b), b), b / (lambda a, b: (
    lambda g: (lambda f: g(lambda *arg: f(f)(*arg)))(lambda f: g(lambda *arg: f(f)(*arg))))(
    lambda f: lambda a, b: not b and a or f(b, a % b))(a, b))((a % b), b))

"""
encode and decode given number to text value
"""
A = "23456789abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ"
_be = lambda x, ret: _be(x // len(A), "%s%s" % (ret, A[x % len(A)])) if x >= len(A) else "%s%s" % (ret, A[x])
base_encoding = lambda x: Y(
    lambda f: lambda x, ret: f(x // len(A), "%s%s" % (ret, A[x % len(A)])) if x >= len(A) else "%s%s" % (ret, A[x]))(x,
                                                                                                                     "")
_bd = lambda x, ret: _bd(x[:-1], len(A) * ret + A.index(x[-1])) if len(x) else ret
base_decoding = lambda x: Y(lambda f: lambda x, ret: f(x[:-1], len(A) * ret + A.index(x[-1])) if len(x) else ret)(x, 0)

default_if_null = lambda obj, name, default: (lambda x, y: x if x else y)(getattr(obj, name, default), default)


def makeFun(data):
    """
    check with the argument's data is a function, else generate function for return given data
    """
    if callable(data):
        return data
    else:
        return lambda x: data


def makeFindFun(data):
    """
    check witch the argument's data is a function, else generate function for finding in their argument a given data
    """
    if callable(data):
        return data
    else:
        return lambda x, i: (x.find(data, i), len(data))


def replace(beg, end, new):
    """
    generate function for replacing any data in given text
    * beg - string of begin area to replace or function who given data and index and return new index, after given to begin area to replace
    * end - string of end area to replace or function who given data and index and return new index, after given to end area to replace
    * new - string to replace instead of finding area or function who given area's data and return a new value for this place
    """
    beg, end = map(makeFindFun, (beg, end))
    new = makeFun(new)

    def func(txt):
        e = 0
        while (True):
            le = e
            b, l = beg(txt, e)
            if b == -1:
                break
            b = b + l
            e, l = end(txt, b)
            if e == -1:
                break
            yield "%s%s" % (txt[le:b], new(txt[b:e]))
        yield txt[le:]

    return func


def addLine(msg, line, sep='\n'):
    """
    just add new line to text variable
    """
    msg = "%s%s" % (msg, sep) if msg else ""
    msg = "%s%s" % (msg, line)
    return msg


def today():
    """
    just take date
    """
    from datetime import date
    t = date.today()
    return (t.day, t.month, t.year)


def getchar():
    '''
    is a UNIX function replacement, working on true UNIX console only (not under any windows game systems like Vista, XP or 7)
    '''
    try:
        import termios

        fd = sys.stdin.fileno()

        if os.isatty(fd):

            old = termios.tcgetattr(fd)
            new = termios.tcgetattr(fd)
            new[3] = new[3] & ~termios.ICANON & ~termios.ECHO
            new[6][termios.VMIN] = 1
            new[6][termios.VTIME] = 0

            try:
                termios.tcsetattr(fd, termios.TCSANOW, new)
                termios.tcsendbreak(fd, 0)
                ch = os.read(fd, 7)

            finally:
                termios.tcsetattr(fd, termios.TCSAFLUSH, old)
        else:
            ch = os.read(fd, 7)

    except IOError:
        ch = input()
    return ch


def url2txt(url, coding=False):
    """
    simple return text data from given url
    """

    try:
        request = urllib.Request(url)
        response = urllib.urlopen(request)
        #        if coding=='auto':
        #            re_coding=re.compile(r'encoding="Windows-1250"')
        if coding:
            return response.read().decode(coding)
        else:
            return response.read()
    except Exception:
        return False


def tags(tag, text, lista=False):
    """
    return given sgml like tag's values in given text
    """
    tag = tag.lower()
    if not lista:
        lista = []
    if "<%s" % tag not in text.lower():
        return lista
    else:
        row_begin = text.lower().find("<%s" % tag)
        row_begin = text.lower().find('>', row_begin) + 1
        row_end = text.lower().find("</%s" % tag, row_begin)
        lista.append(text[row_begin:row_end])
        return tags(tag, text[text.lower().find('>', row_end):], lista)


def isFloat(s):
    try:
        float(s)
    except (ValueError, TypeError):
        return False
    else:
        return True


def toType(s, to_type=int):
    try:
        x = to_type(s)
    except (ValueError, TypeError):
        return x
    else:
        return True