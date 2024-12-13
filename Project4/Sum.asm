// Computes: RAM[1]=1+2+3+...+RAM[0]

@0
D=M

@i
M=1

@n
M=D

@sum
M=0
D=0

(LOOP)
@i
D=M
@sum
M=D+M
@i
M=M+1

@n
M=M-1
D=M

@LOOP
D;JGT

@sum
D=M
@1
M=D

(END)
@END
0;JMP