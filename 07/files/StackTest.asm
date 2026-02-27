// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
AM=M+1
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
AM=M+1
// eq
@SP
AM=M-1
D=M
@SP
A=M-1
D=M-D
@comp.0.true
D;JEQ
D=0
@comp.0.end
0;JMP
(comp.0.true)
D=-1
(comp.0.end)
@SP
A=M-1
M=D
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
AM=M+1
// push constant 16
@16
D=A
@SP
A=M
M=D
@SP
AM=M+1
// eq
@SP
AM=M-1
D=M
@SP
A=M-1
D=M-D
@comp.1.true
D;JEQ
D=0
@comp.1.end
0;JMP
(comp.1.true)
D=-1
(comp.1.end)
@SP
A=M-1
M=D
// push constant 16
@16
D=A
@SP
A=M
M=D
@SP
AM=M+1
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
AM=M+1
// eq
@SP
AM=M-1
D=M
@SP
A=M-1
D=M-D
@comp.2.true
D;JEQ
D=0
@comp.2.end
0;JMP
(comp.2.true)
D=-1
(comp.2.end)
@SP
A=M-1
M=D
// push constant 892
@892
D=A
@SP
A=M
M=D
@SP
AM=M+1
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
AM=M+1
// lt
@SP
AM=M-1
D=M
@SP
A=M-1
D=M-D
@comp.3.true
D;JLT
D=0
@comp.3.end
0;JMP
(comp.3.true)
D=-1
(comp.3.end)
@SP
A=M-1
M=D
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
AM=M+1
// push constant 892
@892
D=A
@SP
A=M
M=D
@SP
AM=M+1
// lt
@SP
AM=M-1
D=M
@SP
A=M-1
D=M-D
@comp.4.true
D;JLT
D=0
@comp.4.end
0;JMP
(comp.4.true)
D=-1
(comp.4.end)
@SP
A=M-1
M=D
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
AM=M+1
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
AM=M+1
// lt
@SP
AM=M-1
D=M
@SP
A=M-1
D=M-D
@comp.5.true
D;JLT
D=0
@comp.5.end
0;JMP
(comp.5.true)
D=-1
(comp.5.end)
@SP
A=M-1
M=D
// push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
AM=M+1
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
AM=M+1
// gt
@SP
AM=M-1
D=M
@SP
A=M-1
D=M-D
@comp.6.true
D;JGT
D=0
@comp.6.end
0;JMP
(comp.6.true)
D=-1
(comp.6.end)
@SP
A=M-1
M=D
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
AM=M+1
// push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
AM=M+1
// gt
@SP
AM=M-1
D=M
@SP
A=M-1
D=M-D
@comp.7.true
D;JGT
D=0
@comp.7.end
0;JMP
(comp.7.true)
D=-1
(comp.7.end)
@SP
A=M-1
M=D
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
AM=M+1
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
AM=M+1
// gt
@SP
AM=M-1
D=M
@SP
A=M-1
D=M-D
@comp.8.true
D;JGT
D=0
@comp.8.end
0;JMP
(comp.8.true)
D=-1
(comp.8.end)
@SP
A=M-1
M=D
// push constant 57
@57
D=A
@SP
A=M
M=D
@SP
AM=M+1
// push constant 31
@31
D=A
@SP
A=M
M=D
@SP
AM=M+1
// push constant 53
@53
D=A
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
// push constant 112
@112
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
// push constant 82
@82
D=A
@SP
A=M
M=D
@SP
AM=M+1
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
