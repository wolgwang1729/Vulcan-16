# Project 5: The Hack Computer

## API HDL Files

### [CPU.hdl](CPU.hdl)
- **Description**: Implements the Central Processing Unit (CPU) of the Hack computer.
- **Functionality**: Parses and executes instructions according to the Hack machine language specification. It interacts with the memory and the ALU to perform computations and control operations. The CPU handles both A-instructions and C-instructions, updating the program counter and managing data flow between registers and memory.
- **Architecture of CPU:**
![CPU Architecture](https://i.sstatic.net/emWTfTvI.png)

### [Memory.hdl](Memory.hdl)
- **Description**: Implements the complete address space of the Hack computer's memory, including RAM and memory-mapped I/O.
- **Functionality**: Facilitates read and write operations to the memory. It includes RAM, screen memory, and keyboard memory. The chip outputs the value stored at the memory location specified by the address input and updates the memory location if the load signal is asserted.
- **Architecture of Memory:**
![CPU Architecture](https://i.sstatic.net/51MRItuH.png)

### [Computer.hdl](Computer.hdl)
- **Description**: Integrates the CPU, memory, and ROM to form the complete Hack computer.
- **Functionality**: Executes programs stored in the ROM. The computer can be reset to restart the execution of the program. It coordinates the interactions between the CPU, memory, and ROM, enabling the execution of machine language programs.
- **Architecture of Computer:**
![Hack Computer Architecture](https://i.sstatic.net/cwLb8LVg.png)

# Translating Instructions:

### A Instructions:

- Symbolic Symbol: `@value`
- Binary Syntax:  `0 {15 bits binary equivalent of value}`    
   - Example: Symbolic Symbol: `@21` 

   - Binary Syntax:  `0 0 0 0 0 0 0 0 0 0 0 1 0 1 0 1`
   

### C Instructions:

- Symbolic Symbol: `dest=comp ; jump`
- Binary Syntax:  `1 1 1 a c1 c2 c3 c4 c5 c6 d1 d2 d3 j1 j2 j3`

| c1 | c2 | c3 | c4 | c5 | c6 | comp (a=0) | comp (a=1) |
|----|----|----|----|----|----|-------------|-------------|
| 1  | 0  | 1  | 0  | 1  | 0  | 0           |             |
| 1  | 1  | 1  | 1  | 1  | 1  | 1           |             |
| 1  | 1  | 1  | 0  | 1  | 0  | -1          |             |
| 0  | 0  | 1  | 1  | 0  | 0  | D           |             |
| 1  | 1  | 0  | 0  | 0  | 0  | A           | M           |
| 0  | 0  | 1  | 1  | 0  | 1  | !D          |             |
| 1  | 1  | 0  | 0  | 0  | 1  | !A          | !M          |
| 0  | 0  | 1  | 1  | 1  | 1  | -D          |             |
| 1  | 1  | 0  | 0  | 1  | 1  | -A          | -M          |
| 0  | 1  | 1  | 1  | 1  | 1  | D+1         |             |
| 1  | 1  | 0  | 1  | 1  | 1  | A+1         | M+1         |
| 0  | 0  | 1  | 1  | 1  | 0  | D-1         |             |
| 1  | 1  | 0  | 0  | 1  | 0  | A-1         | M-1         |
| 0  | 0  | 0  | 0  | 1  | 0  | D+A         | D+M         |
| 0  | 1  | 0  | 0  | 1  | 1  | D-A         | D-M         |
| 0  | 0  | 0  | 1  | 1  | 1  | A-D         | M-D         |
| 0  | 0  | 0  | 0  | 0  | 0  | D & A       | D & M       |
| 0  | 1  | 0  | 1  | 0  | 1  | D \| A      | D \| M      |


| Dest   | d1 | d2 | d3 | Effect: The value is stored in:         |
|--------|----|----|----|-----------------------------------------|
| null   | 0  | 0  | 0  | The value is not stored                |
| M      | 0  | 0  | 1  | RAM[A]                                 |
| D      | 0  | 1  | 0  | D register                             |
| MD     | 0  | 1  | 1  | RAM[A] and D register                  |
| A      | 1  | 0  | 0  | A register                             |
| AM     | 1  | 0  | 1  | A register and RAM[A]                  |
| AD     | 1  | 1  | 0  | A register and D register              |
| AMD    | 1  | 1  | 1  | A register, RAM[A], and D register      |


| Jump   | j1 | j2 | j3 | Effect                      |
|--------|----|----|----|-----------------------------|
| null   | 0  | 0  | 0  | no jump                    |
| JGT    | 0  | 0  | 1  | if `out > 0` jump          |
| JEQ    | 0  | 1  | 0  | if `out = 0` jump          |
| JGE    | 0  | 1  | 1  | if `out ≥ 0` jump          |
| JLT    | 1  | 0  | 0  | if `out < 0` jump          |
| JNE    | 1  | 0  | 1  | if `out ≠ 0` jump          |
| JLE    | 1  | 1  | 0  | if `out ≤ 0` jump          |
| JMP    | 1  | 1  | 1  | Unconditional jump         |

   - Example: Symbolic Symbol: `MD=D+1` 

   - Binary Syntax:  `1 1 1 0 0 1 1 1 1 1 0 1 1 0 0 0`
