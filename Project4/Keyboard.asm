//Shows the Char code of pressed key in RAM[0]

(LOOP)
@KBD
D=M
@R0
M=D
@LOOP
0;JMP