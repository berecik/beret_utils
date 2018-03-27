from .tailRecursion import tail_call_optimized

def rest(l):
    if len(l)>1:
        return l[1:]
    else:
        return None

def raw_match(pattern, str, star = False, at = False):

    if pattern is None:
        if str is None:
            return True
        elif star:
            return True
        elif at:
            return len(str) == 1
        else:
            return False

    if pattern[0] == '*':
        star = True
        return match(rest(pattern), str, star)

    if pattern[0] == '@':
        if star:
            return match(rest(pattern), str, star)
        else:
            at = True
            return match(rest(pattern), str, star, at)

    if str is None:
        return False

    if star:
        if match(pattern, str, star=False, at=False):
            return True
        else:
            return match(pattern, rest(str), star, at)

    if at:
        if match(pattern, str, star=False, at=False):
            return True
        else:
            return match(pattern, rest(str), star=False, at=False)

    if pattern[0] == '?' or pattern[0] == str[0]:
        return match(rest(pattern), rest(str), star, at)

    return False

def match(pattern, str, star = False, at = False):
    return tail_call_optimized(raw_match)(pattern, str, star, at)