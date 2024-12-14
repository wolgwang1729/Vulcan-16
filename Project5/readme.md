# Project 5: The Hack Computer

## API HDL Files

### [CPU.hdl](Project5/CPU.hdl)
- **Description**: Implements the Central Processing Unit (CPU) of the Hack computer.
- **Functionality**: Parses and executes instructions according to the Hack machine language specification. It interacts with the memory and the ALU to perform computations and control operations. The CPU handles both A-instructions and C-instructions, updating the program counter and managing data flow between registers and memory.

### [Memory.hdl](Project5/Memory.hdl)
- **Description**: Implements the complete address space of the Hack computer's memory, including RAM and memory-mapped I/O.
- **Functionality**: Facilitates read and write operations to the memory. It includes RAM, screen memory, and keyboard memory. The chip outputs the value stored at the memory location specified by the address input and updates the memory location if the load signal is asserted.

### [Computer.hdl](Project5/Computer.hdl)
- **Description**: Integrates the CPU, memory, and ROM to form the complete Hack computer.
- **Functionality**: Executes programs stored in the ROM. The computer can be reset to restart the execution of the program. It coordinates the interactions between the CPU, memory, and ROM, enabling the execution of machine language programs.