from .tail_recursion import tail_call_optimized


def rest(l):
    if len(l) > 1:
        return l[1:]
    else:
        return None


def raw_match(pattern, _str, star=False, at=False):
    if pattern is None:
        if _str is None or star:
            return True
        elif at:
            return len(_str) == 1
        else:
            return False

    if pattern[0] == '*':
        star = True
        return match(rest(pattern), _str, star)

    if pattern[0] == '@':
        if star:
            return match(rest(pattern), _str, star)
        else:
            at = True
            return match(rest(pattern), _str, star, at)

    if _str is None:
        return False

    if star:
        if match(pattern, _str, star=False, at=False):
            return True
        else:
            return match(pattern, rest(_str), star, at)

    if at:
        if match(pattern, _str, star=False, at=False):
            return True
        else:
            return match(pattern, rest(_str), star=False, at=False)

    if pattern[0] in ['?', _str[0]]:
        return match(rest(pattern), rest(_str), star, at)

    return False


def match(pattern, _str, star=False, at=False):
    return tail_call_optimized(raw_match)(pattern, _str, star, at)
