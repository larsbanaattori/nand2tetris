'''
- // (comments) and blank lines ignored
- push segment index = push segment[index] to stack
- pop segment index = pop from stack to segment[index]
- arithmetics: add, sub, neg
- comparisons: eq. gt, lt
- logical: and, or, not
- operations pop the required amount of values off the stack,
  evaluate the operation, and push result to stack
- SP = stack pointer = memory address just in front of stack top
    - push -> SP++
    - pop -> SP--
- memory mapping
    - 0-15: R0,...,R15 i.e. virtual registers
    - 16-255: static variables
    - 256-2047: stack
- virtual registers
    - 0 = SP; stack pointer
    - 1 = LCL; base address of local segment
    - 2 = ARG; base address of argument segment
    - 3 = THIS; base of this segment
    - 4 = THAT; base of that segment
    - 5-12 = TEMP segment
    - (R)13-15 = variables VM translator might need
- example: RAM[SP++] = D
    - @SP
    - A=M (easy to ignore this!)
    - M=D
    - @SP
    - M=M+1
- pointer segment = THIS and THAT
    - pointer 0 = THIS
    - pointer 1 = THAT
- if VM program foo refers to variable i -> assembly symbol foo.i, which
  gets mapped automatically to RAM address 16+ as per how the assembler
  works (see previous chapter)
'''
import sys

class Parser:
    def __init__(self, fn: str) -> None:
        with open(fn, "r") as f:
            ls = [l.strip() for l in f.readlines()]
        ls = [l for l in ls if len(l) > 0 and l[0] != "/"]
        ls.reverse()
        self.lines = ls
        self.curr_line = None

    def hasMoreLines(self) -> bool:
        return len(self.lines) > 0
        
    def advance(self) -> None:
        self.curr_line = self.lines.pop()

    def commandType(self) -> str:
        c = self.curr_line
        if c in ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]:
            return "C_ARITHMETIC"
        elif c.split()[0] == "push":
            return "C_PUSH"
        elif c.split()[0] == "pop":
            return "C_POP"
        else:
            return "C_UNKNOWN" # TODO: finish in nect chapter
        
    def arg1(self) -> str:
        if self.commandType() == "C_ARITHMETIC":
            return self.curr_line
        else:
            return self.curr_line.split()[1]
    
    def arg2(self) -> int:
        return int(self.curr_line.split()[2])
    

class CodeWriter:
    def __init__(self, fn: str):
        self.fn = fn
        self.fn_tail = (fn if "/" not in fn else fn.split("/")[-1]).split(".")[0]
        self.f = None
        self.label_n = 0

    def open(self) -> None:
        self.f = open(self.fn, "w")

    def close(self) -> None:
        if self.f is not None:
            self.f.close()
            self.f = None

    def _write(self, s: str) -> None:
        if self.f is None: return
        self.f.write(s + "\n")

    def _setA(self, segment: str, index: int) -> None:
        """
        Set A register to segment index. 
        Effectively maps VM memory segments to actual memory segments.
        """
        if segment == "constant":
            self._write(f"@{index}") # constants are simple
        elif segment in ["local", "argument", "this", "that"]:
            d = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT"}
            self._write(f"@{d[segment]}")
            if index == 0:
                self._write("A=M")
            elif index == 1:
                self._write("A=M+1")
            else:
                self._write("D=M")
                self._write(f"@{index}")
                self._write("A=D+A")
        elif segment == "pointer":
            self._write("@" + ("THIS" if index == 0 else "THAT"))
        elif segment == "temp":
            self._write(f"@{5 + index}")
        elif segment == "static":
            self._write(f"@{self.fn_tail}.{index}")
        else:
            ValueError("Illegal segment type:", segment)
            
    def _pushDtoSP(self) -> None:
        """
        Push value from D register to ram(SP).
        Side effect: increment SP.
        """
        self._write("@SP")
        self._write("A=M") # set A to value of SP
        self._write("M=D") # write value to memory
        self._write("@SP")
        self._write("AM=M+1") # increment SP

    def _popSPtoD(self) -> None:
        """
        Pop value from ram(SP-1) to D register.
        Side effect: decrement SP.
        """
        self._write("@SP")
        self._write("AM=M-1")
        self._write("D=M")

    def writeArithmetic(self, cmd: str) -> None:
        """Write given arithmetic command cmd to file"""
        '''
        - comparisons: eq. gt, lt
        '''
        if cmd in ["add", "sub", "and", "or"]:
            op = {"add": "D+M", "sub": "M-D", "and": "D&M", "or": "D|M"}
            self._popSPtoD()
            self._write("A=A-1")
            self._write(f"M={op[cmd]}")
        elif cmd in ["neg", "not"]:
            op = {"neg": "-M", "not": "!M"}
            self._write("@SP")
            self._write("A=M-1")
            self._write(f"M={op[cmd]}")
        elif cmd in ["eq", "gt", "lt"]:
            op = {"eq": "JEQ", "gt": "JGT", "lt": "JLT"}
            # get SP ("y") to D
            self._popSPtoD()
            # point to "x"
            self._write("@SP")
            self._write("A=M-1")
            # the logical test
            self._write("D=M-D")
            self._write(f"@comp.{self.label_n}.true")
            self._write(f"D;{op[cmd]}")
            # if false -> prepare to write 0 to stack
            self._write("D=0")
            self._write(f"@comp.{self.label_n}.end")
            self._write("0;JMP")
            # if true -> prepare to write -1 to stack
            self._write(f"(comp.{self.label_n}.true)")
            self._write("D=-1")
            self._write(f"(comp.{self.label_n}.end)")
            # write to top of stack
            self._write("@SP")
            self._write("A=M-1")
            self._write("M=D")
            # increment the label index
            self.label_n += 1
        else:
            ValueError("Unknown arithmetic command:", cmd)

    
    def writePushPop(self, cmd: str, segment: int, index: int) -> None:
        """Write command push/pop segment index to file"""
        if cmd == "C_PUSH":
            self._setA(segment, index) # set A to address from which to fetch
            if segment == "constant": # get the right value to D
                self._write("D=A") # constant = shortcut
            else:
                self._write("D=M") # other cases = fetch from memory
            self._pushDtoSP()
        elif cmd == "C_POP":
            self._setA(segment, index) # resolve destination address
            self._write("D=A")
            self._write("@R13") # ...and stash it in R13
            self._write("M=D")
            self._popSPtoD() # pop ram(SP) to D
            self._write("@R13") # get the destination addr back to A
            self._write("A=M")
            self._write("M=D") # ...and move value from D there

        else:
            ValueError("Forbidden input command type", cmd)


if __name__ == "__main__":
    fn = sys.argv[1].strip()
    p = Parser(fn)
    w = CodeWriter(fn.replace(".vm", ".asm"))
    w.open()
    while p.hasMoreLines():
        p.advance()
        w._write("// " + p.curr_line)
        if p.commandType() == "C_ARITHMETIC":
            w.writeArithmetic(p.arg1())
        elif p.commandType() in ["C_PUSH", "C_POP"]:
            w.writePushPop(p.commandType(), p.arg1(), p.arg2())
        else:
            print("Unknown command type", p.commandType())
            exit(1)
    w.close()
