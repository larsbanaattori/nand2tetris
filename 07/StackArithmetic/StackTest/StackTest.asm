// C_PUSH constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
@SP
AM=M-1
D=M
A=A-1
D=M-D
@logopTrue0
D;JEQ
D=0
@logopFalse0
0;JMP
(logopTrue0)
D=-1
(logopFalse0)
@SP
A=M-1
M=D
// C_PUSH constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
@SP
AM=M-1
D=M
A=A-1
D=M-D
@logopTrue1
D;JEQ
D=0
@logopFalse1
0;JMP
(logopTrue1)
D=-1
(logopFalse1)
@SP
A=M-1
M=D
// C_PUSH constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
@SP
AM=M-1
D=M
A=A-1
D=M-D
@logopTrue2
D;JEQ
D=0
@logopFalse2
0;JMP
(logopTrue2)
D=-1
(logopFalse2)
@SP
A=M-1
M=D
// C_PUSH constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@logopTrue3
D;JLT
D=0
@logopFalse3
0;JMP
(logopTrue3)
D=-1
(logopFalse3)
@SP
A=M-1
M=D
// C_PUSH constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@logopTrue4
D;JLT
D=0
@logopFalse4
0;JMP
(logopTrue4)
D=-1
(logopFalse4)
@SP
A=M-1
M=D
// C_PUSH constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@logopTrue5
D;JLT
D=0
@logopFalse5
0;JMP
(logopTrue5)
D=-1
(logopFalse5)
@SP
A=M-1
M=D
// C_PUSH constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@logopTrue6
D;JGT
D=0
@logopFalse6
0;JMP
(logopTrue6)
D=-1
(logopFalse6)
@SP
A=M-1
M=D
// C_PUSH constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@logopTrue7
D;JGT
D=0
@logopFalse7
0;JMP
(logopTrue7)
D=-1
(logopFalse7)
@SP
A=M-1
M=D
// C_PUSH constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@logopTrue8
D;JGT
D=0
@logopFalse8
0;JMP
(logopTrue8)
D=-1
(logopFalse8)
@SP
A=M-1
M=D
// C_PUSH constant 57
@57
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 31
@31
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 53
@53
D=A
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
AM=M-1
D=M
A=A-1
M=D+M
// C_PUSH constant 112
@112
D=A
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D
// neg
@SP
A=M-1
M=-M
// and
@SP
AM=M-1
D=M
A=A-1
M=D&M
// C_PUSH constant 82
@82
D=A
@SP
A=M
M=D
@SP
M=M+1
// or
@SP
AM=M-1
D=M
A=A-1
M=D|M
// not
@SP
A=M-1
M=!M
// End loop
(END)
@END
0;JMP
