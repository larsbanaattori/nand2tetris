import sys
from parse import Parser
from codewrite import CodeWriter

if __name__ == "__main__":

    # TODO: needs rework when translating both files and folders

    filename = sys.argv[1]
    p = Parser(filename)
    w = CodeWriter(filename.replace(".vm", ".asm"))

    p.advance()
    while p.hasMoreLines():
        cmd = p.commandType()
        if cmd in ["C_PUSH", "C_POP"]:
            w.writePushPop(cmd, p.arg1(), int(p.arg2()))
        elif cmd == "C_ARITHMETIC":
            w.writeArithmetic(p.arg1())
        elif cmd == "C_LABEL":
            w.writeLabel(p.arg1())
        elif cmd == "C_GOTO":
            w.writeGoto(p.arg1())
        elif cmd == "C_IF":
            w.writeIf(p.arg1())
        else:
            ValueError(f"command {cmd}")
        p.advance()

    w.close()