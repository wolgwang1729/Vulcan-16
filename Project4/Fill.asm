// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.



(KBDLOOP)
@KBD
D=M 

(BLACKLOOP)
(LOOP1)
@SCREEN
D=A

@ib
D=D+M
A=D 
M=-1

@ib
M=D+1

@nb
M=M-1
D=M

@LOOP1
D;JGT

@KBD
D=M

@BLACKLOOP
D;JGT

(WHITELOOP)
(LOOP2)
@SCREEN
D=A

@iw
D=D+M
A=D 
M=0

@iw
M=D+1

@nw
M=M-1
D=M

@LOOP2
D;JGT

@KBD
D=M

@WHITELOOP
D;JEQ

@KBDLOOP
0;JMP