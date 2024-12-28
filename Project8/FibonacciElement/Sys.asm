//function Sys.init 0
(Sys.init)
@0
D=A
(Sys.init.LOOP)
@Sys.init.END
D;JEQ
@SP
A=M
M=0
@SP
M=M+1
D=D-1
@Sys.init.LOOP
0;JMP
(Sys.init.END)

//push constant 4
@4
D=A
@SP
A=M
M=D
@SP
M=M+1

//call Main.fibonacci 1
@Main.fibonacci$ret.3
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@5
D=A
@1
D=D+A
@SP
D=M-D
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(Main.fibonacci$ret.3)

//label END
(END)

//goto END
@END
0;JMP