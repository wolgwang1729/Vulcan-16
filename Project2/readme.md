# Project 2: Arithmetic and Logical Units

## API HDL Files

### [Add16.hdl](Add16.hdl)
- **Description**: Implements a 16-bit adder.
- **Functionality**: Adds two 16-bit two's complement values. The most significant carry bit is ignored.

### [ALU.hdl](ALU.hdl)
- **Description**: Implements the Arithmetic Logic Unit (ALU).
- **Functionality**: Computes various functions on the 16-bit inputs `x` and `y` according to the control bits `zx`, `nx`, `zy`, `ny`, `f`, and `no`. Outputs the result and sets the `zr` and `ng` flags based on the result.

$$
\begin{array}{|c|c|c|c|c|c|c|}
\hline zx & nx & zy & ny & f & no & out = \\
\hline \text{if } zx \text{ then } &\text{if } nx \text{ then } x&\text{if } zy \text{ then } &\text{if } ny \text{ then }&\text{if } f \text{ then } out=x+y &\text{if } no \text{ then }&f(x,y)=\\
\ x=0 & x=!x & y=0 & y=!y &\text{ else } out=!out&out=!out \\
\hline 1 & 0 & 1 & 0 & 1 & 0 & 0 \\
\hline 1 & 1 & 1 & 1 & 1 & 1 & 1 \\
\hline 1 & 1 & 1 & 0 & 1 & 0 & -1 \\
\hline 0 & 0 & 1 & 1 & 0 & 0 & x \\
\hline 1 & 1 & 0 & 0 & 0 & 0 & y \\
\hline 0 & 0 & 1 & 1 & 0 & 1 & ! x \\
\hline 1 & 1 & 0 & 0 & 0 & 1 & !y \\
\hline 0 & 0 & 1 & 1 & 1 & 1 & -x \\
\hline 1 & 1 & 0 & 0 & 1 & 1 & -y \\
\hline 0 & 1 & 1 & 1 & 1 & 1 & x+1 \\
\hline 1 & 1 & 0 & 1 & 1 & 1 & y+1 \\
\hline 0 & 0 & 1 & 1 & 1 & 0 & x-1 \\
\hline 1 & 1 & 0 & 0 & 1 & 0 & y-1 \\
\hline 0 & 0 & 0 & 0 & 1 & 0 & x+y \\
\hline 0 & 1 & 0 & 0 & 1 & 1 & x-y\\
\hline 0 & 0 & 0 & 1 & 1 & 1 & y-x \\
\hline 0 & 0 & 0 & 0 & 0 & 0 & x\wedge y \\
\hline 0 & 1 & 0 & 1 & 0 & 1 & x \mid y \\
\hline \end{array}
$$

### [FullAdder.hdl](FullAdder.hdl)
- **Description**: Implements a full adder.
- **Functionality**: Computes the sum of three bits (`a`, `b`, and `c`). Outputs the sum and the carry bit.

### [HalfAdder.hdl](HalfAdder.hdl)
- **Description**: Implements a half adder.
- **Functionality**: Computes the sum of two bits (`a` and `b`). Outputs the sum and the carry bit.

### [Inc16.hdl](Inc16.hdl)
- **Description**: Implements a 16-bit incrementer.
- **Functionality**: Increments the 16-bit input `in` by 1 and outputs the result.