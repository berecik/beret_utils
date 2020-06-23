from python_utils.trace import log_fun

@log_fun
def example(a, b, c):
    a = b + c
    b = a + c
    c = a + b
    d = "hi there"
    return a + b + c


def test_log_content_working():
    assert example(5,4,3) == 34


@log_fun
def fun_a_10():
    return 10

@log_fun
def fun_b_20():
    b = 20


def test_fun_a_10(capsys):
    fun_a_10()
    out, err = capsys.readouterr()
    assert "a=10" in out


def test_fun_b_20(capsys):
    fun_b_20()
    out, err = capsys.readouterr()
    assert "b=20" in out


def test_example(capsys):
    global a
    a = 1
    global b
    b = 2
    global c
    c = 3
    global d
    d = 4
    global e
    e = 5
    assert example(5, 4, 3) == 34
    out, err = capsys.readouterr()
    assert "a=5" in out
    assert "b=4" in out
    assert "c=3" in out
    assert "a=7" in out
    assert "b=10" in out
    assert "c=17" in out
    assert "d='hi there'" in out
    assert "result=34" in out
    assert "e=5" not in out