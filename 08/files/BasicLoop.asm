// ***
// source file: BasicLoop.vm
// ***
// push constant 0
@0
D=A
@SP
A=M
M=D
@SP
AM=M+1
// pop local 0
@LCL
A=M
D=A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
// label LOOP
(LOOP)
// push argument 0
@ARG
A=M
D=M
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
// add
@SP
AM=M-1
D=M
A=A-1
M=D+M
// pop local 0
@LCL
A=M
D=A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
// push argument 0
@ARG
A=M
D=M
@SP
A=M
M=D
@SP
AM=M+1
// push constant 1
@1
D=A
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
// pop argument 0
@ARG
A=M
D=A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
// push argument 0
@ARG
A=M
D=M
@SP
A=M
M=D
@SP
AM=M+1
// if-goto LOOP
@SP
AM=M-1
D=M
@LOOP
D;JNE
// push local 0
@LCL
A=M
D=M
@SP
A=M
M=D
@SP
AM=M+1
// end loop
(THE$END$LOOP)
@THE$END$LOOP
0;JMP
