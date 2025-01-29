// for(int i=0;i<n;i++){
//     arr[i]=-1;
// }
//Suppose that base address (arr) is 100 and n=10

@100
D=A 

@arr
M=D

@10
D=A

@n
M=D

@i
M=0
D=M

(LOOP)
@arr
D=M

@i
A=D+M
M=-1

@i
M=M+1

@n
M=M-1
D=M

@LOOP
D;JGT

(END)
@END
0;JMP


