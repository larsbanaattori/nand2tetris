class Parser:

    def __init__(self, filename: str) -> None:
        self.file = open(filename, "r")
        self.line = None
        self.eof = False

    def hasMoreLines(self) -> bool:
        return not self.eof

    def advance(self) -> None:
        while True:
            self.line = self.file.readline()
            if self.line == "":
                self.eof = True
                break
            self.line = self.line.strip().replace(" ", "")
            if len(self.line) > 0 and self.line[0:2] != "//":
                break

    def instructionType(self) -> str:
        if self.line[0] == "@":
            return "A_INSTRUCTION"
        elif self.line[0] == "(" and self.line[-1] == ")":
            return "L_INSTRUCTION"
        else:
            return "C_INSTRUCTION"
        
    def symbol(self) -> str:
        return self.line.replace("@","")\
                        .replace("(", "")\
                        .replace(")", "")
    
    def dest(self) -> str:
        if "=" in self.line:
            return self.line.split("=")[0]
        else:
            return ""
        
    def comp(self) -> str:
        if "=" in self.line:
            return self.line.split("=")[1]\
                            .split(";")[0]
        else:
            return self.line.split(";")[0]
        
    def jump(self) -> str:
        if ";" in self.line:
            return self.line.split(";")[1]
        else:
            return ""

    def __print__(self) -> None:
        print(self.line)
