//Computes: if R0>0
//             R1=1
//          else
//             R1=0

@0
D=M

@8
D;JGT

@1
M=0
@10
0;JMP

@1
M=1

@10
0;JMP