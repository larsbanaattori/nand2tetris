import sys
import parse
from coder import comp, dest, jump

if __name__ == "__main__":
    filename = sys.argv[1]
    with open(filename.replace(".asm", ".hack"), "w") as f_out:
        p = parse.Parser(filename)
        p.advance()
        while p.hasMoreLines():
            type = p.instructionType()
            if type == "A_INSTRUCTION":
                # TODO: handle variables
                line = format(int(p.symbol()), "016b")
            elif type == "C_INSTRUCTION":
                line = "111" + comp(p.comp()) + dest(p.dest()) + jump(p.jump())
            else:
                # TODO: handle L_INSTRUCTIONS
                line = "TODO"
            f_out.write(line + "\n")
            p.advance()
