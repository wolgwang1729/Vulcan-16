# Hardware

This folder contains the hardware implementation of Vulcan-16, a 16-bit computer built from scratch. The hardware is designed using HDL (Hardware Description Language) and is organized into subfolders based on the project's progression.

## Projects

### **Project 1: Building Basic Logic Gates**
- **Purpose**: Implement fundamental logic gates and multiplexers/demultiplexers.
- **Components**:
  - Basic gates: `And`, `Or`, `Not`, `Xor`.
  - Multi-bit gates: `And16`, `Or16`, `Not16`.
  - Multiplexers: `Mux`, `Mux16`, `Mux4Way16`, `Mux8Way16`.
  - Demultiplexers: `DMux`, `DMux4Way`, `DMux8Way`.
- **Outcome**: These gates form the foundation for more complex components in later projects.

---

### **Project 2: Constructing Adders and the ALU**
- **Purpose**: Build arithmetic components and the Arithmetic Logic Unit (ALU).
- **Components**:
  - Adders: `HalfAdder`, `FullAdder`, `Add16`, `Inc16`.
  - ALU: `ALU.hdl` (capable of 18 operations, including addition, subtraction, and logical operations).
- **Outcome**: The ALU is the core computational unit of the CPU.

---

### **Project 3: Developing Sequential Logic Elements**
- **Purpose**: Create memory and sequential logic components.
- **Components**:
  - Registers: `Bit`, `Register`.
  - Memory units: `RAM8`, `RAM64`, `RAM512`, `RAM4K`, `RAM16K`.
  - Program Counter: `PC`.
- **Outcome**: These components enable the computer to store data and execute programs sequentially.

---

### **Project 4: Writing Assembly Programs**
- **Purpose**: Write and test assembly programs for the Hack computer.
- **Programs**:
  - Arithmetic: `Add2`, `Mult`, `Sum`.
  - Screen manipulation: `Fill`, `Flip`, `Rectangle`.
  - Input handling: `Keyboard`.
  - Logic: `Signum`, `SignumLabels`.
- **Outcome**: These programs demonstrate the functionality of the hardware and serve as test cases for the CPU.

---

### **Project 5: Integrating Components into a Working Computer**
- **Purpose**: Combine all hardware components into a functional computer.
- **Components**:
  - CPU: `CPU.hdl`.
  - Memory: `Memory.hdl`.
  - Full Computer: `Computer.hdl`.
- **Outcome**: A fully functional 16-bit computer capable of executing programs.