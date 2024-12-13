//Computes: if R0>0
//             R1=1
//          else
//             R1=0

@0
D=M

@POSITIVE
D;JGT

@1
M=0
@END
0;JMP

(POSITIVE)
@1
M=1

(END)
@10
0;JMP