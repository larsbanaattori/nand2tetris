from parse import Parser

def test1() -> None:

    p = Parser("test_parser1.asm")
    assert p.hasMoreLines()

    p.advance()
    assert p.line == "@i"
    assert p.instructionType() == "A_INSTRUCTION"
    assert p.symbol() == "i"

    p.advance()
    assert p.hasMoreLines()
    assert p.instructionType() == "C_INSTRUCTION"
    assert p.line == "M=1"
    assert p.dest() == "M"
    assert p.comp() == "1"
    assert p.jump() == ""

    p.advance()
    p.advance()
    p.advance()
    p.advance()
    
    p.advance()
    assert p.hasMoreLines()
    assert p.line == "@STOP"
    assert p.instructionType() == "A_INSTRUCTION"
    assert p.symbol() == "STOP"

    p.advance()
    assert p.hasMoreLines()
    assert p.instructionType() == "C_INSTRUCTION"
    assert p.line == "D=D+1;JEQ"
    assert p.dest() == "D"
    assert p.comp() == "D+1"
    assert p.jump() == "JEQ"

    p.advance()
    assert p.hasMoreLines()
    assert p.instructionType() == "L_INSTRUCTION"
    assert p.symbol() == "LOOP"

    p.advance()
    p.advance()
    p.advance()

    p.advance()
    assert p.hasMoreLines()
    assert p.line == "D=D-M"
    assert p.instructionType() == "C_INSTRUCTION"
    assert p.dest() == "D"
    assert p.comp() == "D-M"
    assert p.jump() == ""

    p.advance()

    p.advance()
    assert p.hasMoreLines()
    assert p.line == "D;JGT"
    assert p.instructionType() == "C_INSTRUCTION"
    assert p.dest() == ""
    assert p.comp() == "D"
    assert p.jump() == "JGT"

    for _ in range(10):
        p.advance()

    assert p.hasMoreLines()
    assert p.line == "0;JMP"
    assert p.dest() == ""
    assert p.comp() == "0"
    assert p.jump() == "JMP"

    p.advance()
    assert p.hasMoreLines()
    assert p.instructionType() == "L_INSTRUCTION"
    assert p.symbol() == "STOP"

    for _ in range(7):
        p.advance()

    assert p.hasMoreLines()
    assert p.line == "0;JMP"
    assert p.instructionType() == "C_INSTRUCTION"
    assert p.dest() == ""
    assert p.comp() == "0"
    assert p.jump() == "JMP"

    p.advance()
    assert not p.hasMoreLines()
    assert p.line == ""
