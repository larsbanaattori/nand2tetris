import sys
import parse
from coder import comp, dest, jump

if __name__ == "__main__":
    filename = sys.argv[1]

    # Initializes the symbol table
    symbols = {}
    for i in range(16):
        symbols["R"+str(i)] = i
    symbols["SP"] = 0
    symbols["LCL"] = 1
    symbols["ARG"] = 2
    symbols["THIS"] = 3
    symbols["THAT"] = 4
    symbols["SCREEN"] = 16384
    symbols["KBD"] = 24576

    # First pass to complete symbol table
    p = parse.Parser(filename)
    p.advance()
    line_number = 0
    while p.hasMoreLines():
        type = p.instructionType()
        if type == "C_INSTRUCTION" or type == "A_INSTRUCTION":
            line_number += 1
        else:
            symbol = p.symbol()
            if symbol not in symbols:
                symbols[symbol] = line_number
        p.advance()

    # Second pass to assemble machine code
    ram_count = 16
    with open(filename.replace(".asm", ".hack"), "w") as f_out:
        p = parse.Parser(filename)
        p.advance()
        while p.hasMoreLines():
            type = p.instructionType()
            if type == "A_INSTRUCTION":
                symbol = p.symbol()
                if symbol[0].isdigit():
                    code = int(p.symbol())
                else:
                    if symbol not in symbols:
                        symbols[symbol] = ram_count
                        ram_count += 1
                    code = symbols[symbol]
                line = format(code, "016b") + "\n"
            elif type == "C_INSTRUCTION":
                line = "111" + comp(p.comp()) + dest(p.dest()) + jump(p.jump()) + "\n"
            else:
                # Note: nothing is done in case of an L_INSTRUCTION
                line = ""
            f_out.write(line)
            p.advance()
