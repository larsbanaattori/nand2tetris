class Parser:
    
    def __init__(self, filename: str) -> None:
        self.file = open(filename, "r")
        self.line = [""]
        self.eof = False

    def hasMoreLines(self) -> bool:
        return not self.eof
    
    def advance(self) -> None:
        while True:
            self.line = self.file.readline()
            if self.line == "":
                self.line = [""]
                self.eof = True
                break
            self.line = self.line.strip().split()
            if len(self.line) > 0 and self.line[0][0] != "/":
                break

    def arg1(self) -> str:
        if self.commandType() == "C_ARITHMETIC":
            return self.__cmd()
        else:
            return self.line[1]
    
    def arg2(self) -> str:
        return self.line[2]
    
    def __cmd(self) -> str:
        return self.line[0]

    def commandType(self) -> str:
        command = self.__cmd()
        # C_PUSH
        if command == "push":
            return "C_PUSH"
        # C_POP
        elif command == "pop":
            return "C_POP"
        # C_ARITHMETIC
        elif command in ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]:
            return "C_ARITHMETIC"
        elif command == "label":
            return "C_LABEL"
        elif command == "goto":
            return "C_GOTO"
        elif command == "if-goto":
            return "C_IF"
        else:
            # TODO: finish other command types in p07
            return "SOMETHING_ELSE"
        # C_FUNCTION
        # C_RETURN
        # C_CALL
