from python_tools.patterns import match


def test_patterns_match_01():
    assert match("ala", "ala")


def test_patterns_match_02():
    assert match("a***la*", "ala")


def test_patterns_match_03():
    assert match("a*@*l*?*", "ala")


def test_patterns_match_04():
    assert match("a*@*l?", "ala")


def test_patterns_match_05():
    assert match("a*@*l@a", "ala")


def test_patterns_match_06():
    assert match("abcd", "abcd")


def test_patterns_match_07():
    assert not match("abcd", "abzcd")


def test_patterns_match_08():
    assert not match("ab?cd", "abcd")


def test_patterns_match_09():
    assert match("ab?cd", "abzcd")


def test_patterns_match_10():
    assert match("ab*cd", "abcd")


def test_patterns_match_11():
    assert match("ab*cd", "abzcd")


def test_patterns_match_12():
    assert match("ab*cd", "abxyzcd")


def test_patterns_match_13():
    assert not match("ab*cd", "abzcdz")


def test_patterns_match_14():
    assert match("ab@cd", "abcd")


def test_patterns_match_15():
    assert match("ab@cd", "abzcd")


def test_patterns_match_16():
    assert not match("ab@cd", "abxyzcd")


def test_patterns_match_17():
    assert match("ab*@cd", "abxyzcd")


def test_patterns_match_18():
    assert not match("ab*zcd", "abxycd")
