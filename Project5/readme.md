# Project 5: The Hack Computer

## API HDL Files

### [CPU.hdl](Project5/CPU.hdl)
- **Description**: Implements the Central Processing Unit (CPU) of the Hack computer.
- **Functionality**: Parses and executes instructions according to the Hack machine language specification. It interacts with the memory and the ALU to perform computations and control operations. The CPU handles both A-instructions and C-instructions, updating the program counter and managing data flow between registers and memory.
- **Architecture of CPU:**
![CPU Architecture](https://i.sstatic.net/emWTfTvI.png)

### [Memory.hdl](Project5/Memory.hdl)
- **Description**: Implements the complete address space of the Hack computer's memory, including RAM and memory-mapped I/O.
- **Functionality**: Facilitates read and write operations to the memory. It includes RAM, screen memory, and keyboard memory. The chip outputs the value stored at the memory location specified by the address input and updates the memory location if the load signal is asserted.
- **Architecture of Memory:**
![CPU Architecture](https://i.sstatic.net/51MRItuH.png)

### [Computer.hdl](Project5/Computer.hdl)
- **Description**: Integrates the CPU, memory, and ROM to form the complete Hack computer.
- **Functionality**: Executes programs stored in the ROM. The computer can be reset to restart the execution of the program. It coordinates the interactions between the CPU, memory, and ROM, enabling the execution of machine language programs.
- **Architecture of Computer:**
![Hack Computer Architecture](https://i.sstatic.net/cwLb8LVg.png)

# Translating Instructions:

### A Instructions:

- Symbolic Symbol: `@value`
- Bindary Syntax:  `0 {15 bits binary equivalent of value}`    
   - Example: Symbolic Symbol: `@21` 

   - Bindary Syntax:  `0 0 0 0 0 0 0 0 0 0 0 1 0 1 0 1`
   

### C Instructions:

- Symbolic Symbol: `dest=comp ; jump`
- Bindary Syntax:  `1 1 1 a c1 c2 c3 c4 c5 c6 d1 d2 d3 j1 j2 j3`

$$
\begin{array}{|c|c|c|c|c|c|c|c|}
\hline c1 & c2 & c3 & c4 & c5 & c6 & comp(a=0)& comp(a=1)\\
\hline 1 & 0 & 1 & 0 & 1 & 0 & 0 \\
\hline 1 & 1 & 1 & 1 & 1 & 1 & 1 \\
\hline 1 & 1 & 1 & 0 & 1 & 0 & -1 \\
\hline 0 & 0 & 1 & 1 & 0 & 0 & D \\
\hline 1 & 1 & 0 & 0 & 0 & 0 & A &M \\
\hline 0 & 0 & 1 & 1 & 0 & 1 & ! D \\
\hline 1 & 1 & 0 & 0 & 0 & 1 & !A & !M \\
\hline 0 & 0 & 1 & 1 & 1 & 1 & -D \\
\hline 1 & 1 & 0 & 0 & 1 & 1 & -A &-M \\
\hline 0 & 1 & 1 & 1 & 1 & 1 & D+1 \\
\hline 1 & 1 & 0 & 1 & 1 & 1 & A+1 & M+1\\
\hline 0 & 0 & 1 & 1 & 1 & 0 & D-1 \\
\hline 1 & 1 & 0 & 0 & 1 & 0 & A-1 & M-1\\
\hline 0 & 0 & 0 & 0 & 1 & 0 & D+A &D+M \\
\hline 0 & 1 & 0 & 0 & 1 & 1 & D-A  &D-M\\
\hline 0 & 0 & 0 & 1 & 1 & 1 & A-D & M-D \\
\hline 0 & 0 & 0 & 0 & 0 & 0 & D\wedge  A& D \wedge M \\
\hline 0 & 1 & 0 & 1 & 0 & 1 & D \mid A & D \mid M\\
\hline \end{array}
$$

$$
\begin{array}{|c|ccc|l|}
\hline { dest } & d1 & d 2 & d 3 & \text { effect: the value is stored in: } \\
\hline  { null } & 0 & 0 & 0 & \text { The value is not stored } \\
\hline { M } & 0 & 0 & 1 & \text { RAM[A] } \\
\hline { D } & 0 & 1 & 0 & \text { D register } \\
\hline { MD } & 0 & 1 & 1 & \text { RAM[A] and D register } \\
\hline { A } & 1 & 0 & 0 & \text { A register } \\
\hline { AM } & 1 & 0 & 1 & \text { A register and RAM[A] } \\
\hline { AD } & 1 & 1 & 0 & \text { A register and D register } \\
\hline { AMD } & 1 & 1 & 1 & \text { A register, RAM[A], and D register } \\
\hline
\end{array}
$$

$$
\begin{array}{|c|ccc|l|}
\hline { \text{jump} } & j1 & j 2 & j 3 & \text { effect } \\
\hline  { null } & 0 & 0 & 0 & \text { no jump } \\
\hline { JGT } & 0 & 0 & 1 & \text { if } out\gt0 \text{ jump }\\
\hline { JEQ} & 0 & 1 & 0 & \text{ if } out= 0 \text{ jump } \\
\hline { JGE } & 0 & 1 & 1 & \text { if } out\ge0 \text{ jump } \\
\hline { JLT } & 1 & 0 & 0 & \text{ if } out\le0 \text{ jump } \\
\hline { JNE} & 1 & 0 & 1 & \text { if } out\ne0 \text{ jump } \\
\hline { JLE} & 1 & 1 & 0 & \text { if } out\le0 \text{ jump } \\
\hline { JMP } & 1 & 1 & 1 & \text { Unconditional jump} \\
\hline
\end{array}
$$

   - Example: Symbolic Symbol: `MD=D+1` 

   - Bindary Syntax:  `1 1 1 0 0 1 1 1 1 1 0 1 1 0 0 0`
