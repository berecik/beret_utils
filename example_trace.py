from python_tools.trace import log_fun
from python_tools.patterns import match

@log_fun
def example(a, b, c):
    a = b + c
    b = a + c
    c = a + b
    d = "hi there"
    result = a + b + c
    return result


print(example(5,4,3))



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

for txt in ("match({},{})={}".format(pattern, str, log_fun(path=False, content=False, ret=False)(match)(pattern, str)) for pattern, str in example_patterns):
    print(txt)