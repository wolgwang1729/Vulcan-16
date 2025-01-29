# Project 1: Basic Logic Gates

## API HDL Files

### [And.hdl](And.hdl)
- **Description**: Implements the AND gate.
- **Functionality**: If both inputs `a` and `b` are 1, the output `out` is 1; otherwise, the output is 0.

### [And16.hdl](And16.hdl)
- **Description**: Implements a 16-bit AND gate.
- **Functionality**: Performs bitwise AND operation on two 16-bit inputs `a` and `b`, producing a 16-bit output `out`.

### [DMux.hdl](DMux.hdl)
- **Description**: Implements a 1-to-2 demultiplexer.
- **Functionality**: Routes the input `in` to one of the two outputs `a` or `b` based on the selector `sel`.

### [DMux4Way.hdl](DMux4Way.hdl)
- **Description**: Implements a 1-to-4 demultiplexer.
- **Functionality**: Routes the input `in` to one of the four outputs `a`, `b`, `c`, or `d` based on the 2-bit selector `sel`.

### [DMux8Way.hdl](DMux8Way.hdl)
- **Description**: Implements a 1-to-8 demultiplexer.
- **Functionality**: Routes the input `in` to one of the eight outputs `a`, `b`, `c`, `d`, `e`, `f`, `g`, or `h` based on the 3-bit selector `sel`.

### [Mux.hdl](Mux.hdl)
- **Description**: Implements a 2-to-1 multiplexer.
- **Functionality**: Selects one of the two inputs `a` or `b` to be the output `out` based on the selector `sel`.

### [Mux16.hdl](Mux16.hdl)
- **Description**: Implements a 16-bit 2-to-1 multiplexer.
- **Functionality**: Selects one of the two 16-bit inputs `a` or `b` to be the 16-bit output `out` based on the selector `sel`.

### [Mux4Way16.hdl](Mux4Way16.hdl)
- **Description**: Implements a 16-bit 4-to-1 multiplexer.
- **Functionality**: Selects one of the four 16-bit inputs `a`, `b`, `c`, or `d` to be the 16-bit output `out` based on the 2-bit selector `sel`.

### [Mux8Way16.hdl](Mux8Way16.hdl)
- **Description**: Implements a 16-bit 8-to-1 multiplexer.
- **Functionality**: Selects one of the eight 16-bit inputs `a`, `b`, `c`, `d`, `e`, `f`, `g`, or `h` to be the 16-bit output `out` based on the 3-bit selector `sel`.

### [Not.hdl](Not.hdl)
- **Description**: Implements the NOT gate.
- **Functionality**: Inverts the input `in`, producing the output `out`.

### [Not16.hdl](Not16.hdl)
- **Description**: Implements a 16-bit NOT gate.
- **Functionality**: Performs bitwise NOT operation on the 16-bit input `in`, producing a 16-bit output `out`.

### [Or.hdl](Or.hdl)
- **Description**: Implements the OR gate.
- **Functionality**: If either input `a` or `b` is 1, the output `out` is 1; otherwise, the output is 0.

### [Or16.hdl](Or16.hdl)
- **Description**: Implements a 16-bit OR gate.
- **Functionality**: Performs bitwise OR operation on two 16-bit inputs `a` and `b`, producing a 16-bit output `out`.

### [Or8Way.hdl](Or8Way.hdl)
- **Description**: Implements an 8-way OR gate.
- **Functionality**: If any of the 8 inputs `in[0]` to `in[7]` is 1, the output `out` is 1; otherwise, the output is 0.

### [Xor.hdl](Xor.hdl)
- **Description**: Implements the XOR gate.
- **Functionality**: If the inputs `a` and `b` are different, the output `out` is 1; otherwise, the output is 0.