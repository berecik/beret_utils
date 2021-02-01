import timeit

from beret_utils.trace import log_fun


@log_fun
def example(a, b, c):
    a = b + c
    b = a + c
    c = a + b
    d = "hi there"
    return a + b + c


example_patterns = [
    ("ala", "ala"),
    ("a***la*", "ala"),
    ("a*@*l*?*", "ala"),
    ("a*@*l?", "ala"),
    ("a*@*l@a", "ala"),
    ("abcd", "abcd"),
    ("abcd", "abzcd"),
    ("ab?cd", "abcd"),
    ("ab?cd", "abzcd"),
    ("ab*cd", "abcd"),
    ("ab*cd", "abzcd"),
    ("ab*cd", "abxyzcd"),
    ("ab*cd", "abzcdz"),
    ("ab@cd", "abcd"),
    ("ab@cd", "abzcd"),
    ("ab@cd", "abxyzcd"),
    ("ab*@cd", "abxyzcd"),
    ("ab*zcd", "abxycd")
]


def match_all_patterns(match_fun):
    for _ in (
            "match({},{})={}".format(
                pattern,
                str,
                log_fun(path=False, content=False, ret=False, call=False, log_fun=lambda x: x)(match_fun)(pattern, str)
            ) for pattern, str in example_patterns):
        pass


raw_match_time = timeit.timeit('match_all_patterns(raw_match)',
                               setup="from __main__ import match_all_patterns, raw_match",
                               number=10)

match_time = timeit.timeit('match_all_patterns(match)',
                           setup="from __main__ import match_all_patterns, match",
                           number=10)

print(raw_match_time, match_time)

print(example(5, 4, 3))
