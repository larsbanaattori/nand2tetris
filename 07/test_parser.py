from parse import Parser

def test1():

    p = Parser("ParseTest.vm")

    assert p.hasMoreLines()

    p.advance()
    assert p.commandType() == "C_POP"
    assert p.arg1() == "temp"
    assert p.arg2() == "6"

    p.advance()
    assert p.commandType() == "C_PUSH"
    assert p.arg1() == "local"
    assert p.arg2() == "0"

    p.advance()
    p.advance()
    assert p.commandType() == "C_ARITHMETIC"
    assert p.arg1() == "add"

    p.advance()
    p.advance()
    assert p.commandType() == "C_ARITHMETIC"
    assert p.arg1() == "sub"

    for _ in range(7):
        p.advance()

    assert p.commandType() == "C_ARITHMETIC"
    assert p.arg1() == "or"

    p.advance()
    assert not p.hasMoreLines()
