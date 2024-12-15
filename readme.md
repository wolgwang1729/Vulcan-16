# Introduction
## Brief Overview of the Project
This project involves building a Hack computer using the Nand2tetris course and the book "The Elements of Computing Systems: Building a Modern Computer from First Principles" by Noam Nisan and Shimon Schocken. The project includes both hardware and software components, demonstrating the construction of a modern computer from basic logic gates.

## Purpose and Goals
The goal of this project is to understand the inner workings of a computer by constructing one from scratch. This includes designing the hardware components using HDL (Hardware Description Language) and writing software programs in assembly language to run on the constructed computer.
The goal is also to implement the things I learned in University's third semester curriculum in course Digital Logic Design(CS201n) and Operating Systems Design(CS207n).

# Technical Specifications
- The 16-bit computer, I built, is based on Harvard Architecture (which is a variant of Von Neumann Architecture). 
- **Architecture of Computer:**
![Hack Computer Architecture](https://i.sstatic.net/cwLb8LVg.png)
- **Architecture of CPU:**
![CPU Architecture](https://i.sstatic.net/emWTfTvI.png)
- **Architecture of Memory:**
![CPU Architecture](https://i.sstatic.net/51MRItuH.png)
- The computer consists of:
  - `32K x 16` ROM, in which any program can be loaded.
  - `24577 x 16` memory, composed of `16K x 16` RAM, `8K x 16` for the screen memory map, and `1 x 16` for keyboard input.
  - The CPU contains a `1 x 16` data register, a `1 x 16` address register, and an ALU capable of performing 18 specified operations.
- Detailed specification can be found in the `readme.md` of sub folders.


# Project Structure
## Description of the Directory Layout
- [`Project1/`](Project1/): Contains basic logic gates implementations.
- [`Project2/`](Project2/): Contains arithmetic and logical units.
- [`Project3/`](Project3/): Contains sequential logic components.
- [`Project4/`](Project4/): Contains the machine language programs.
- [`Project5/`](Project5/): Contains the CPU and overall computer architecture.
- [`Project6/`](Project6/): Contains the assembler which is implemented in Python.

## Explanation of Each Project's Purpose
- **Project1**: Building basic gates like And, Or, Not, Xor, Mux, Dmux.
- **Project2**: Constructing adders and ALU.
- **Project3**: Developing sequential logic elements like program counter and registers of various sizes.
- **Project4**: Writing assembly programs for the Hack computer.
- **Project5**: Integrating all components into a working computer.
- **Project6**: Developing an assembler to translate assembly language programs into machine code.

# Hardware Components
## List and Description of All Hardware Components
- **ALU**: Arithmetic Logic Unit, performs arithmetic and logical operations.
- **RAM**: Random Access Memory, stores data.
- **CPU**: Central Processing Unit, executes instructions.
- **Screen**: Displays output.
- **Keyboard**: Inputs data.

# Usage Instructions
## How to Run the Hardware Simulations
1. Open the HDL files in the hardware simulator either in [legacy software package](https://drive.google.com/file/d/1IkIR8Pwq3PY49QgXpUJOkUUVht-TKIET/view) or [online IDE](https://nand2tetris.github.io/web-ide/chip)
2. Run the simulations.

## How to Load and Execute the Assembly Programs
1. Load the assembly program into the CPU emulator either in [legacy software package](https://drive.google.com/file/d/1IkIR8Pwq3PY49QgXpUJOkUUVht-TKIET/view) or [online IDE](https://nand2tetris.github.io/web-ide/chip)
2. Set the initial values in the RAM.
3. Run the program and observe the results.

# Testing and Validation
## Description of the Testing Process
Each hardware component and software program is tested using predefined test scripts provided in the Nand2tetris course. These scripts automate the testing process and verify the correctness of the implementations.

## How to Verify the Correctness of the Hardware Components and Software Programs
1. Load the test script in the hardware simulator.
2. Run the script and check the output against the expected results.
3. Debug and fix any issues that arise.

# References
## Books, Courses, and Other Resources Used
- "The Elements of Computing Systems: Building a Modern Computer from First Principles" by Noam Nisan and Shimon Schocken.
- Nand2tetris course materials.

## Links to Additional Reading Materials
- [Book](https://www.nand2tetris.org/book)
- [Nand2tetris Official Website](https://www.nand2tetris.org/)
- [Course on Coursera](https://www.coursera.org/learn/build-a-computer)

# Contributing
## Guidelines for Contributing to the Project
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed description of your changes.

## How to Report Issues and Suggest Improvements
- Open an issue on the project's GitHub repository.
- Provide a detailed description of the issue or suggestion.

# License
## Information About the Project's License
This project is licensed under the MIT License. See the LICENSE file for more details.

# Acknowledgments
## Credits to Authors, Contributors, and Resources
- Noam Nisan and Shimon Schocken for the Nand2tetris course and book.
- The Nand2tetris community for support and resources.