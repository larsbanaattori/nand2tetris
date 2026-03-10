import sys
import os

class Parser:
    def __init__(self, fn: str) -> None:
        with open(fn, "r") as f:
            ls = [l.strip() for l in f.readlines()]
        ls = [l.split("/")[0].strip() for l in ls if len(l) > 0 and l[0] != "/"]
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
        elif c.split()[0] == "label":
            return "C_LABEL"
        elif c.split()[0] == "goto":
            return "C_GOTO"
        elif c.split()[0] == "if-goto":
            return "C_IF"
        elif c.split()[0] == "function":
            return "C_FUNCTION"
        elif c.split()[0] == "return":
            return "C_RETURN"
        elif c.split()[0] == "call":
            return "C_CALL"
        else:
            return "C_UNKNOWN" # TODO: finish in nect chapter
        
    def arg1(self) -> str:
        if self.commandType() == "C_ARITHMETIC":
            return self.curr_line
        else:
            return self.curr_line.split()[1]
    
    def arg2(self) -> int:
        return int(self.curr_line.split()[2])
    

"""
CodeWriter is given two names:
- pn = program name
- fn (through setFileName) = name of current VM code file

pn is used to name the .asm output file.

fn is used to set names of functions, labels and static variables
in the output .asm file.

fn can be updated and has to be initialized through setFileName
"""

class CodeWriter:
    def __init__(self, pn: str):
        self.pn = pn # path to which .asm output is written
        self.fn = None # name of current .vm file being handled
        self.f = None # the output file handle
        self.label_n = 0 # counter for labels used in logical arithmetic
        self.functionName = None # name of function being handled
        self.functionRetIndex = None # running count of return index in function

    def setFileName(self, fn: str) -> None:
        fn = fn.replace("/", "").replace(".vm", "")
        self.fn = fn

    def _setFunctionName(self, fn: str) -> None:
        self.functionName = fn
        self.functionRetIndex = 0

    def open(self) -> None:
        self.f = open(self.pn, "w")

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
            self._write(f"@{self.fn}.{index}")
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

    def _resolveLabel(self, label: str) -> str:
        """maps given VM code label to ASM code label"""
        if self.functionName is None:
            return label
        else:
            return self.functionName + "$" + label

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

    def writeLabel(self, label: str) -> None:
        self._write(f"({self._resolveLabel(label)})")

    def writeGoto(self, label: str) -> None:
        self._write(f"@{self._resolveLabel(label)}")
        self._write("0;JMP")

    def writeIf(self, label: str) -> None:
        # pop topmost value of stack to D
        self._popSPtoD()
        # jump to label if D != 0
        self._write(f"@{self._resolveLabel(label)}")
        self._write("D;JNE")

    def writeFunction(self, fName: str, nVars: int) -> None:
        # inject function entry label
        self._write(f"({fName})")
        # push nVars zeros to stack
        if nVars == 0: return
        self._write("D=0")
        for _ in range(nVars):
            self._pushDtoSP()

    def writeReturn(self) -> None:
        # frame (temporary variable) = LCL  // save to R13
        self._write("@LCL")
        self._write("D=M")
        self._write("@R13")
        self._write("M=D")
        # calculate retAddr = *(frame-5)    // save to R14
        self._write("@5")
        self._write("A=D-A")
        self._write("D=M")
        self._write("@R14")
        self._write("M=D")
        # *ARG = pop()          // return value to caller's stack
        self._popSPtoD()
        self._setA("argument", 0)
        self._write("M=D")
        # SP = ARG + 1          // repositions SP for caller
        self._write("D=A+1")
        self._write("@SP")
        self._write("M=D")
        # THAT = *(frame-1)     // restores THAT for caller
        # THIS = *(frame-2)     // restores THIS for caller
        # ARG = *(frame-3)      // restores ARG for the caller
        # LCL = *(frame-4)      // restores LCL for the caller
        for dest in ["THAT", "THIS", "ARG", "LCL"]:
            self._write("@R13")
            self._write("AM=M-1")
            self._write("D=M")
            self._write(f"@{dest}")
            self._write("M=D")
        # goto retAddr          // go to return address
        self._write("@R14")
        self._write("A=M")
        self._write("0;JMP")

    def writeCall(self, fName: str, nArgs: int) -> None:
        # push retAddress label to stack
        self._write(f"@{self.functionName}$ret.{self.functionRetIndex}")
        self._write("D=A")
        self._pushDtoSP()
        # push LCL
        # push ARG
        # push THIS
        # push THAT
        for src in ["LCL", "ARG", "THIS", "THAT"]:
            self._write(f"@{src}")
            self._write("D=M")
            self._pushDtoSP()
        # ARG = SP - 5 - nArgs
        self._write("@SP")
        self._write("D=M")
        self._write(f"@{5 + nArgs}")
        self._write("D=D-A")
        self._write("@ARG")
        self._write("M=D")
        # LCL = SP
        self._write("@SP")
        self._write("D=M")
        self._write("@LCL")
        self._write("M=D")
        # goto f
        self._write(f"@{fName}")
        self._write("0;JMP")
        # (returnAddress)
        self._write(f"({self.functionName}$ret.{self.functionRetIndex})")
        self.functionRetIndex += 1

if __name__ == "__main__":
    # get path containing the program
    path = sys.argv[1].strip()

    # is the program a multi-file one or not?
    path_is_dir = (".vm" not in path)

    # create list of files which we need to go through
    if path_is_dir:
        files = os.listdir(path)
        file_names = [f for f in files if ".vm" in f]
        prefix = path
        if prefix[-1] != "/": prefix = prefix + "/"
        file_paths = [prefix + f for f in file_names]
    else:
        file_names = [path.split("/")[-1]]
        file_paths = [path]

    # resolve the path of the output file
    path_out = path
    if path_out[-1] == "/": path_out = path_out[:-1]
    path_out = path_out.replace(".vm", "")
    path_out = path_out + ".asm"

    # set up the writer 
    w = CodeWriter(path_out)
    w.open()

    # loop over files
    for i in range(len(file_names)):
        fn, fp = file_names[i], file_paths[i]
        p = Parser(fp) # open the file being parsed
        w.setFileName(fn) # tell writer the name of current file
        # loop over lines in the file
        w._write("// ***")
        w._write("// source file: " + fn)
        w._write("// ***")
        while p.hasMoreLines():
            p.advance()
            cl = p.curr_line
            if "/" in cl:
                cl = cl.split("//")[0]
            w._write("// " + cl)
            if p.commandType() == "C_ARITHMETIC":
                w.writeArithmetic(p.arg1())
            elif p.commandType() in ["C_PUSH", "C_POP"]:
                w.writePushPop(p.commandType(), p.arg1(), p.arg2())
            elif p.commandType() == "C_LABEL":
                w.writeLabel(p.arg1())
            elif p.commandType() == "C_GOTO":
                w.writeGoto(p.arg1())
            elif p.commandType() == "C_IF":
                w.writeIf(p.arg1())
            elif p.commandType() == "C_FUNCTION":
                w.writeFunction(p.arg1(), int(p.arg2()))
                w._setFunctionName(p.arg1())
            elif p.commandType() == "C_RETURN":
                w.writeReturn()
            elif p.commandType() == "C_CALL":
                w.writeCall(p.arg1(), int(p.arg2()))
            else:
                print("Unknown command type", p.commandType())
                exit(1)
    # write the end loop
    w._write("// end loop")
    w._write("(THE$END$LOOP)")
    w._write("@THE$END$LOOP")
    w._write("0;JMP")
    w.close()
