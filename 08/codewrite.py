class CodeWriter:

    def __init__(self, filename: str) -> None:
        self.filename = filename.split("/")[-1].replace(".asm", "")
        self.fname = ""
        self.file = open(filename, "w")
        self.log_op_count = 0

    def __write(self, lines: list) -> None:
        for line in lines:
            self.file.write(line + "\n")

    def writeArithmetic(self, command: str) -> None:
        binary_ops = {
            "add": "D+M",
            "sub": "M-D",
            "and": "D&M",
            "or": "D|M"
        }
        unary_ops = {
            "neg": "-M",
            "not": "!M"
        }
        log_ops = {
            "eq": "JEQ",
            "gt": "JGT",
            "lt": "JLT"
        }

        self.__write(["// " + command])
        self.__write(["@SP"])

        if command in unary_ops:
            self.__write(["A=M-1", f"M={unary_ops[command]}"])
        else:
            self.__write(["AM=M-1", "D=M", "A=A-1"])
            if command in binary_ops:
                self.__write([f"M={binary_ops[command]}"])
            else: # Logical operations
                self.__write(
                    ["D=M-D", f"@logopTrue{self.log_op_count}", f"D;{log_ops[command]}",
                     "D=0", f"@logopFalse{self.log_op_count}", "0;JMP",
                     f"(logopTrue{self.log_op_count})", "D=-1",
                     f"(logopFalse{self.log_op_count})",
                     "@SP", "A=M-1", "M=D"]
                )
                self.log_op_count += 1

    def writePushPop(self, command: str, segment: str, index: int) -> None:
        def set_address() -> str:
            segment_map = {
                "local": "LCL",
                "argument": "ARG",
                "this": "THIS",
                "that": "THAT"
            }

            if segment in ["local", "argument", "this", "that"]:
                self.__write([f"@{segment_map[segment]}", "D=M", 
                                      f"@{index}", "A=D+A"])
            elif segment == "pointer":
                if index == 0:
                    self.__write(["@THIS"])
                else:
                    self.__write(["@THAT"])
            elif segment == "temp":
                self.__write([f"@{5+index}"])
            elif segment == "constant":
                self.__write([f"@{index}"])
            elif segment == "static":
                self.__write([f"@{self.filename+'.'+str(index)}"])
            else:
                raise ValueError(f"segment type {segment}")
            
        self.__write([f"// {command} {segment} {index}"])
        if command == "C_PUSH":
            set_address()
            if segment == "constant":
                self.__write(["D=A"])
            else:
                self.__write(["D=M"])
            self.__write(["@SP", "A=M", "M=D"])
            self.__write(["@SP", "M=M+1"])
        elif command == "C_POP":
            set_address()
            self.__write(["D=A", "@R13", "M=D"]) # R13 = address where to pop the value
            self.__write(["@SP", "AM=M-1", "D=M", "@R13", "A=M", "M=D"])
        else:
            raise ValueError(f"command {command}")

    def writeLabel(self, label: str) -> None:
        self.__write([f"// label {label}"])
        self.__write([f"({self.filename}.{self.fname}${label})"])

    def writeGoto(self, label: str) -> None:
        self.__write([f"// goto {label}"])
        self.__write([f"@{self.filename}.{self.fname}${label}", "0;JMP"])

    def writeIf(self, label: str) -> None:
        self.__write([f"// if-goto {label}"])
        self.__write(["@SP", "AM=M-1", "D=M", f"@{self.filename}.{self.fname}${label}", "D;JNE"])

    def writeFunction(self, functionName: str, nVars: int) -> None:
        self.fname = functionName
        # TODO
        pass

    def close(self) -> None:
        self.__write(["// End loop", "(END)", "@END", "0;JMP"])
        self.file.close()
