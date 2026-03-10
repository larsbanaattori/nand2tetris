// ***
// source file: SimpleFunction.vm
// ***
// function SimpleFunction.test 2
(SimpleFunction.test)
D=0
@SP
A=M
M=D
@SP
AM=M+1
@SP
A=M
M=D
@SP
AM=M+1
// push local 0
@LCL
A=M
D=M
@SP
A=M
M=D
@SP
AM=M+1
// push local 1
@LCL
A=M+1
D=M
@SP
A=M
M=D
@SP
AM=M+1
// add
@SP
AM=M-1
D=M
A=A-1
M=D+M
// not
@SP
A=M-1
M=!M
// push argument 0
@ARG
A=M
D=M
@SP
A=M
M=D
@SP
AM=M+1
// add
@SP
AM=M-1
D=M
A=A-1
M=D+M
// push argument 1
@ARG
A=M+1
D=M
@SP
A=M
M=D
@SP
AM=M+1
// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D
// return
@LCL
D=M
@R13
M=D
@5
A=D-A
D=M
@R14
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
D=A+1
@SP
M=D
@R13
AM=M-1
D=M
@THAT
M=D
@R13
AM=M-1
D=M
@THIS
M=D
@R13
AM=M-1
D=M
@ARG
M=D
@R13
AM=M-1
D=M
@LCL
M=D
@R14
A=M
0;JMP
// end loop
(THE$END$LOOP)
@THE$END$LOOP
0;JMP
