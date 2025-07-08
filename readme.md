# Vulcan-16: A 16-bit Computer Built from Scratch

## Overview of the Project
I have always wondered, "What is a computer?" Since childhood, I’ve treated it as a black box. I knew its components: the CPU, input devices, output devices—and their purposes, but I never truly understood how a computer actually works. How does a CPU, which supposedly only understands 1s and 0s, handle code? How does typing `print("Hello World!")` light up thousands of pixels on the screen? What happens inside the CPU when you write something as simple as `x = 5`? To answer these questions, my curiosity led me to build Vulcan-16.

**Vulcan-16** is a fully functional 16-bit computer designed and implemented from the ground up. Starting with basic logic gates, this project explores the intersection of hardware and software. It’s far from perfect, but that’s the point. Vulcan-16 is my proof that with enough stubbornness, you can turn NAND gates into something that feels alive.

This project is my attempt to turn "How does this even work?!" into "Oh. That’s how." It’s also the longest project I’ve ever worked on, and the one I’ve spent the most time on(at least up to the point of writing this).


## Purpose and Goals
The goal of this project is simple yet ambitious: to understand how a computer works by building one from scratch. This means designing every hardware component—from logic gates to the CPU—using HDL (Hardware Description Language), writing software programs in assembly language, implementing a virtual machine and designing a compiler to translate high-level code into machine code.

But Vulcan-16 isn’t just about building a computer. It’s about bridging the gap between theory and practice. Through this project, I aimed to apply the concepts I learned in my university courses—Digital Logic Design (CS201n), Operating Systems Design (CS207n) and Computer System Architecture and Organization(CS206)—to a real, tangible system.

In short, Vulcan-16 is my way of answering the question: "Can I take what I’ve learned in the classroom and use it to create something that actually works?" Spoiler: It’s harder than it sounds, but infinitely more rewarding.

# Technical Specifications
- The 16-bit computer, I built, is based on Harvard Architecture (which is a variant of Von Neumann Architecture). 

## **Architecture of Computer:**
![Vulcan-16 Computer Architecture](https://i.sstatic.net/guKsKZIz.png)
- The computer consists of:
  - `32K x 16` ROM, in which any program can be loaded.
  - `24577 x 16` memory, composed of `16K x 16` RAM, `8K x 16` for the screen memory map, and `1 x 16` for keyboard input.
  - The CPU contains a `1 x 16` data register, a `1 x 16` address register, and an ALU capable of performing 18 specified operations.
## **Architecture of CPU:**
![CPU Architecture](https://i.sstatic.net/emWTfTvI.png)
## **Architecture of Memory:**
![Memory Architecture](https://i.sstatic.net/51MRItuH.png)
- Detailed specification can be found in the `readme.md` of sub folders.
## **Softwares:**
![Softwares](https://i.sstatic.net/CbKSHYDr.png)


# Project Structure
```bash
Vulcan-16/
├── Hardware/          # HDL implementations of CPU, memory, and peripherals
│   ├── LogicGates/    # Basic gates (AND, OR, NOT, etc.)
│   ├── ALU/           # Arithmetic Logic Unit
│   └── CPU/           # Central Processing Unit
│
├── Software/          # Tools to program Vulcan-16
│   ├── Assembler/     # Translates assembly to machine code
│   ├── Compiler/      # Compiles Jack to VM code
│   └── VMTranslator/  # Converts VM code to assembly
│
├── OS/                # Jack Operating System
│   ├── Sys/           # System services
│   ├── Screen/        # Graphics driver
│   ├── Keyboard/      # Input handling
│   ├── Memory/        # Memory management utilities
│   ├── Math/          # Mathematical operations
│   ├── String/        # String manipulation utilities
│   └── Array/         # Array handling and operations
│
└── Programs/          # Programs for Vulcan-16
    └── Games/         # GuessANumber
```

# Usage Instructions
## How to Run the Hardware Chips(.hdl)
1. Open the HDL files in the hardware simulator either in [legacy software package](https://drive.google.com/file/d/1IkIR8Pwq3PY49QgXpUJOkUUVht-TKIET/view) or [online IDE Hardware Simulator](https://nand2tetris.github.io/web-ide/chip)
2. Run the simulations.

## How to Load and Execute the Assembly Programs(.hack or .asm)
1. Load the assembly program into the CPU emulator either in [legacy software package](https://drive.google.com/file/d/1IkIR8Pwq3PY49QgXpUJOkUUVht-TKIET/view) or [online IDE CPU Emulator](https://nand2tetris.github.io/web-ide/cpu)
2. Set the initial values in the RAM.
3. Run the program and observe the results.

## How to Load and Execute the VM Programs(.vm)
1. Load the VM program into the VM emulator either in [legacy software package](https://drive.google.com/file/d/1IkIR8Pwq3PY49QgXpUJOkUUVht-TKIET/view) or [online IDE VM Emulator](https://nand2tetris.github.io/web-ide/vm)
2. Change the execution speed to Fast.
3. Run the program and observe the results.

## How to Load and Execute the Jack Programs(.jack)
1. Load the folder in which Jack programs exist into the Jack compiler either in [legacy software package](https://drive.google.com/file/d/1IkIR8Pwq3PY49QgXpUJOkUUVht-TKIET/view) or [online IDE Jack Compiler](https://nand2tetris.github.io/web-ide/jack)
2. Click on `Compile` to compile the Jack programs and then click on `Run` to load the generated VM code into the VM emulator.
3. Change the execution speed to Fast.
4. Run the program and observe the results.

# Future Roadmap
- Develop a web-based hardware simulator and IDE to test various architectures, enabling more flexible experimentation beyond the current setup.
- Translate key hardware chips into popular HDL languages such as Verilog and VHDL to broaden compatibility and integration.
- Port Vulcan-16 onto an FPGA platform to validate designs on actual hardware and enhance performance.

# References
## Books, Courses, and Other Resources Used
- "Code: The Hidden Language of Computer Hardware and Software" by Charles Petzold.
- "The Elements of Computing Systems: Building a Modern Computer from First Principles" by Noam Nisan and Shimon Schocken.
- "Digital Design" by M. Morris Mano.
- "Computer System Architecture" by M. Morris Mano.
- Nand2tetris course materials.

# License
This project is licensed under the MIT License. See the LICENSE file for more details.

# Acknowledgments
## Credits to Authors, Contributors, and Resources
- Noam Nisan and Shimon Schocken for the Nand2tetris course and book.
- Charles Petzold and M. Morris Mano for their respective books.
- Mark Armbrust for the Random.jack file.
- The Open Source community for support and resources.