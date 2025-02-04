# Project 3: Sequential Logic Components

## API HDL Files

### [Bit.hdl](Bit.hdl)
- **Description**: Implements a 1-bit register.
- **Functionality**: If `load` is asserted, the register's value is set to `in`; otherwise, the register maintains its current value.

### [Register.hdl](Register.hdl)
- **Description**: Implements a 16-bit register.
- **Functionality**: If `load` is asserted, the register's value is set to `in`; otherwise, the register maintains its current value.


### [RAM8.hdl](RAM8.hdl)
- **Description**: Implements a memory of eight 16-bit registers.
- **Functionality**: If `load` is asserted, the value of the register selected by `address` is set to `in`; otherwise, the value does not change. The value of the selected register is emitted by `out`.

### [RAM64.hdl](RAM64.hdl)
- **Description**: Implements a memory of sixty-four 16-bit registers.
- **Functionality**: If `load` is asserted, the value of the register selected by `address` is set to `in`; otherwise, the value does not change. The value of the selected register is emitted by `out`.

### [RAM512.hdl](RAM512.hdl)
- **Description**: Implements a memory of 512 16-bit registers.
- **Functionality**: If `load` is asserted, the value of the register selected by `address` is set to `in`; otherwise, the value does not change. The value of the selected register is emitted by `out`.

### [RAM4K.hdl](RAM4K.hdl)
- **Description**: Implements a memory of 4K 16-bit registers.
- **Functionality**: If `load` is asserted, the value of the register selected by `address` is set to `in`; otherwise, the value does not change. The value of the selected register is emitted by `out`.

### [RAM16K.hdl](RAM16K.hdl)
- **Description**: Implements a memory of 16K 16-bit registers.
- **Functionality**: If `load` is asserted, the value of the register selected by `address` is set to `in`; otherwise, the value does not change. The value of the selected register is emitted by `out`.

### [PC.hdl](PC.hdl)
- **Description**: Implements a 16-bit program counter.
- **Functionality**: If `reset` is asserted, the counter is set to 0. If `load` is asserted, the counter is set to `in`. If `inc` is asserted, the counter is incremented by 1. Otherwise, the counter maintains its current value.