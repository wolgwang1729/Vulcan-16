//push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

//eq
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@TRUE.3
D;JEQ
@SP
A=M
M=0
@SP
M=M+1
@CONTINUE.3
0;JMP
(TRUE.3)
@SP
A=M
M=-1
@SP
M=M+1
(CONTINUE.3)

//push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1

//eq
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@TRUE.6
D;JEQ
@SP
A=M
M=0
@SP
M=M+1
@CONTINUE.6
0;JMP
(TRUE.6)
@SP
A=M
M=-1
@SP
M=M+1
(CONTINUE.6)

//push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

//eq
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@TRUE.9
D;JEQ
@SP
A=M
M=0
@SP
M=M+1
@CONTINUE.9
0;JMP
(TRUE.9)
@SP
A=M
M=-1
@SP
M=M+1
(CONTINUE.9)

//push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

//lt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@TRUE.12
D;JLT
@SP
A=M
M=0
@SP
M=M+1
@CONTINUE.12
0;JMP
(TRUE.12)
@SP
A=M
M=-1
@SP
M=M+1
(CONTINUE.12)

//push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1

//lt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@TRUE.15
D;JLT
@SP
A=M
M=0
@SP
M=M+1
@CONTINUE.15
0;JMP
(TRUE.15)
@SP
A=M
M=-1
@SP
M=M+1
(CONTINUE.15)

//push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

//lt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@TRUE.18
D;JLT
@SP
A=M
M=0
@SP
M=M+1
@CONTINUE.18
0;JMP
(TRUE.18)
@SP
A=M
M=-1
@SP
M=M+1
(CONTINUE.18)

//push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

//gt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@TRUE.21
D;JGT
@SP
A=M
M=0
@SP
M=M+1
@CONTINUE.21
0;JMP
(TRUE.21)
@SP
A=M
M=-1
@SP
M=M+1
(CONTINUE.21)

//push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1

//gt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@TRUE.24
D;JGT
@SP
A=M
M=0
@SP
M=M+1
@CONTINUE.24
0;JMP
(TRUE.24)
@SP
A=M
M=-1
@SP
M=M+1
(CONTINUE.24)

//push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

//gt
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@TRUE.27
D;JGT
@SP
A=M
M=0
@SP
M=M+1
@CONTINUE.27
0;JMP
(TRUE.27)
@SP
A=M
M=-1
@SP
M=M+1
(CONTINUE.27)

//push constant 57
@57
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 31
@31
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 53
@53
D=A
@SP
A=M
M=D
@SP
M=M+1

//add
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=D+M
@SP
M=M+1

//push constant 112
@112
D=A
@SP
A=M
M=D
@SP
M=M+1

//sub
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=M-D
@SP
M=M+1

//neg
@SP
M=M-1
A=M
M=-M
@SP
M=M+1

//and
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=D&M
@SP
M=M+1

//push constant 82
@82
D=A
@SP
A=M
M=D
@SP
M=M+1

//or
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=D|M
@SP
M=M+1

//not
@SP
M=M-1
A=M
M=!M
@SP
M=M+1