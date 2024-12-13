//Draws a filled rectangle at top left screen
//Rectangle width is 16px and height is stored in RAM[0]

@16384
D=A 

@base
M=D

@32
D=A

@inc
M=D

@i 
M=0
D=0

@0
D=M

@n
M=D

@END
D;JLE

(LOOP)
@base
D=M

@i
D=D+M
A=D 
M=-1

@inc
D=M

@i
M=D+M

@n
M=M-1
D=M

@LOOP
D;JGT

(END)
@END
0;JMP



