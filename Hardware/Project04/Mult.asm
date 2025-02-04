// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// The algorithm is based on repetitive addition.

@R0 
D=M
@a 
M=D

@R1
D=M
@b
M=D

@result
M=0

(LOOP)
@b
D=M
@AFTERLOOP
D;JEQ

@a 
D=M

@result
M=D+M

@b
M=M-1

@LOOP
0;JMP

(AFTERLOOP)
@result
D=M
@R2
M=D

(END)
@END
0;JMP


