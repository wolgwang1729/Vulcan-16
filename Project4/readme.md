# Project 4: Assembly Programs

## Explanation of Each File

### [Add2.asm](Add2.asm)
- **Description**: Computes the sum of two values stored in RAM[0] and RAM[1], and stores the result in RAM[2].
- **Usage**: Put values in RAM[0] and RAM[1] before running the program.

### [ArrInitialisation.asm](ArrInitialisation.asm)
- **Description**: Initializes an array of size `n` with the value -1. The base address of the array is 100, and `n` is set to 10.
- **Usage**: The program sets all elements of the array to -1.

### [Fill.asm](Fill.asm)
- **Description**: Runs an infinite loop that listens to the keyboard input. When a key is pressed, the program blackens the screen. When no key is pressed, the screen is cleared.
- **Usage**: The program continuously checks for keyboard input and updates the screen accordingly.

### [Flip.asm](Flip.asm)
- **Description**: Flips the values of RAM[0] and RAM[1].
- **Usage**: The program swaps the values stored in RAM[0] and RAM[1].

### [Keyboard.asm](Keyboard.asm)
- **Description**: Displays the character code of the pressed key in RAM[0].
- **Usage**: The program continuously reads the keyboard input and updates RAM[0] with the character code.

### [Mult.asm](Mult.asm)
- **Description**: Multiplies the values stored in RAM[0] and RAM[1], and stores the result in RAM[2]. The algorithm is based on repetitive addition.
- **Usage**: Put values in RAM[0] and RAM[1] before running the program.

### [Rectangle.asm](Rectangle.asm)
- **Description**: Draws a filled rectangle at the top left of the screen. The rectangle's width is 16 pixels, and its height is stored in RAM[0].
- **Usage**: Set the height of the rectangle in RAM[0] before running the program.

### [Signum.asm](Signum.asm)
- **Description**: Computes the sign of the value in RAM[0]. If RAM[0] > 0, sets RAM[1] to 1; otherwise, sets RAM[1] to 0.
- **Usage**: The program checks the value in RAM[0] and updates RAM[1] accordingly.

### [SignumLabels.asm](SignumLabels.asm)
- **Description**: Computes the sign of the value in RAM[0] using labels. If RAM[0] > 0, sets RAM[1] to 1; otherwise, sets RAM[1] to 0.
- **Usage**: The program checks the value in RAM[0] and updates RAM[1] accordingly.

### [Sum.asm](Sum.asm)
- **Description**: Computes the sum of all integers from 1 to the value stored in RAM[0], and stores the result in RAM[1].
- **Usage**: Set the value in RAM[0] before running the program. The result will be stored in RAM[1].