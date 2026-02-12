import sys
import os

class Parser:
    def __init__(self, fname: str):
        with open(fname, "r") as f:
            self.lines = f.read().splitlines()
        self.lines.reverse()
        self.lines = [l.strip() for l in self.lines]
        self.lines = [l.strip() for l in self.lines if len(l) > 0 and l[0] != "/"]
        self.curr_instr = None

    def hasMoreLines(self) -> bool:
        return len(self.lines) > 0
    
    def advance(self) -> None:
        self.curr_instr = self.lines.pop()

    def instructionType(self) -> str:
        if self.curr_instr[0] == "@":
            return "A_INSTRUCTION"
        elif self.curr_instr[0] == "(" and self.curr_instr[-1] == ")":
            return "L_INSTRUCTION"
        else:
            return "C_INSTRUCTION"
        
    def symbol(self) -> str:
        return self.curr_instr.replace("(", "").replace(")", "").replace("@", "")
    
    def dest(self) -> str:
        x = self.curr_instr.split("=")
        if len(x) == 1:
            return ""
        else:
            return x[0]
    
    def comp(self) -> str:
        x = self.curr_instr
        if "=" in x:
            x = x.split("=")[1]
        if ";" in x:
            x = x.split(";")[0]
        return x
    
    def jump(self) -> str:
        x = self.curr_instr.split(";")
        if len(x) == 1:
            return ""
        else:
            return x[1]

def dest(s: str) -> str:
    return (
        ("1" if "A" in s else "0") +
        ("1" if "D" in s else "0") + 
        ("1" if "M" in s else "0")
    )

def comp(s: str) -> str:
    a = "1" if "M" in s else "0" # first bit = use A (=0) or M(=1)
    s = s.replace("D", "x").replace("A", "y").replace("M", "y")
    d = {
        "0": "101010",
        "1": "111111",
        "-1": "111010",
        "x": "001100",
        "y": "110000",
        "!x": "001101",
        "!y": "110001",
        "-x": "001111",
        "-y": "110011",
        "x+1": "011111",
        "y+1": "110111",
        "x-1": "001110",
        "y-1": "110010",
        "x+y": "000010",
        "x-y": "010011",
        "y-x": "000111",
        "x&y": "000000",
        "x|y": "010101"
    }
    return a + d[s]

def jump(s: str) -> str:
    d = {
        "": "000",
        "JGT": "001",
        "JEQ": "010",
        "JGE": "011",
        "JLT": "100",
        "JNE": "101",
        "JLE": "110",
        "JMP": "111"
    }
    return d[s]

def assemble(fn: str) -> None:
    fn_out = fn.replace(".asm", ".hack")
    lines_out = []

    # initialize symtable
    symtable = {
        "SP": 0,
        "LCL": 1,
        "ARG": 2,
        "THIS": 3,
        "THAT": 4,
        "SCREEN": 16384,
        "KBD": 24576
    }
    for i in range(16):
        symtable[f"R{i}"] = i

    # first pass
    rom = 0
    p = Parser(fn)
    while p.hasMoreLines():
        p.advance()
        if p.instructionType() == "L_INSTRUCTION":
            sym = p.symbol()
            symtable[sym] = rom
            continue
        rom += 1

    # second pass
    p = Parser(fn)
    ram = 16
    while p.hasMoreLines():
        p.advance()
        if p.instructionType() == "C_INSTRUCTION":
            l = "111" + comp(p.comp()) + dest(p.dest()) + jump(p.jump())
            lines_out.append(l)
        elif p.instructionType() == "A_INSTRUCTION":
            symbol = p.symbol()
            if symbol in symtable:
                symbol = symtable[symbol]
            elif not symbol.isnumeric():
                symtable[symbol] = ram
                symbol = ram
                ram += 1
            symbol = str(bin(int(symbol)))[2:]
            symbol = ("0" * (15 - len(symbol))) + symbol
            lines_out.append("0" + symbol)
    with open(fn_out, "w") as f:
        f.write("\n".join(lines_out))

if __name__ == "__main__":
    fn = sys.argv[1]
    assert ".asm" in fn
    assemble(fn)
