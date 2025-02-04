# Software

This folder contains the software tools used to program Vulcan-16. These tools include an assembler, a virtual machine translator, and a compiler for the Jack programming language.

## Projects

### **Project 6: Building the Assembler**
- **Purpose**: Translate assembly language into machine code.
- **Components**:
  - `Assembler.py`: Translates assembly code to binary.
  - `AssemblerL.py`: Supports symbolic labels in assembly code.
- **Outcome**: Enables the computer to execute assembly programs.

---

### **Project 7: Implementing the Virtual Machine Translator**
- **Purpose**: Translate VM (Virtual Machine) code into assembly language.
- **Components**:
  - `VMTranslator.py`: Converts VM commands (e.g., arithmetic, memory access) into assembly.
- **Outcome**: Bridges the gap between high-level programming and machine code.

---

### **Project 8: Extending the Virtual Machine Translator**
- **Purpose**: Add support for advanced VM features like function calls and static variables.
- **Components**:
  - `VMTranslator.py`: Handles function calls, return statements, and static memory.
- **Outcome**: Enables the execution of more complex programs.

---

### **Project 10: Building the Jack Analyzer**
- **Purpose**: Compile the Jack high-level language into XML.
- **Components**:
  - `JackTokenizer.py`: Tokenizes Jack code.
  - `CompilationEngine.py`: Parses and compiles Jack code.
  - `JackAnalyzer.py`: Analyzes Jack code for syntax and structure and gives XML.
- **Outcome**: Foundation for Jack Compiler

---

### **Project 11: Extending the Jack Compiler**
- **Purpose**: Add support for identifiers and advanced language features.
- **Components**:
  - `JackCompiler.py`: Compiles Jack code with identifier support.
  - `JackTokenizerIdentifier.py`: Tokenizes Jack code with advanced features.
- **Outcome**: Enables more sophisticated programming in Jack.

### Note:
While Vulcan-16 aims to be a self-contained computer system, the software tools (VM translator, compiler) are written in Python, this might seem counter inuitive as we are building the Vulcan-16 from scratch. This is a deliberate choice, mirroring the historical development of compilers.  Just as early compilers were often hand-written or built using simpler languages, Python serves as our initial tool to create the software infrastructure for Vulcan-16.  This allows for more efficient development and testing.  Ultimately, these tools could theoretically be rewritten in Jack and run on Vulcan-16 itself.