class Parser:
    def __init__(self, directory):
        self.directory=directory
        self.filename=self.getFilename()
        self.counter=1
    
    def getFilename(self):
        if "\\" in self.directory:
            return self.directory.split("\\")[-1].split('.')[0].strip()
        else:
            return self.directory.split('.')[0].strip()

    def __call__(self, str):
        self.VMInstruction = str
        self.commandType = self.getCommandType(str)
        self.arg1 = self.getArg1()
        self.arg2 = self.getArg2()
        self.memorySegment = self.getMemorySegment()
        self.assemblyInstruction = self.getAssemblyInstruction()
        self.counter+=1
        return self.assemblyInstruction

    def getCommandType(self, str):
        if "push" in str:
            return "C_PUSH"
        elif "pop" in str:
            return "C_POP"
        elif "label" in str:
            return "C_LABEL"
        elif "if-goto" in str:
            return "C_IF"
        elif "goto" in str:
            return "C_GOTO"
        else:
            return "C_ARITHMETIC"
        
    def getArg1(self):
        if self.commandType == "C_ARITHMETIC":
            return self.VMInstruction.strip()
        elif self.commandType == "C_LABEL" or self.commandType == "C_GOTO" or self.commandType=="C_IF":
            return self.VMInstruction.split(" ")[1].strip()
        else:
            return self.VMInstruction.split(" ")[0].strip()
    
    def getArg2(self):
        if self.commandType=="C_PUSH" or self.commandType=="C_POP":
            return int(self.VMInstruction.split(" ")[-1].strip())
        else:
            return None
        
    def getMemorySegment(self):
        if self.commandType == "C_PUSH" or self.commandType == "C_POP":
            return self.VMInstruction.split(" ")[1].strip()
        else:
            return None
        
    def getAssemblyInstruction(self):
        assemblyInstruction = ""
        Abreviations = {
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT",
            0: "THIS",
            1: "THAT",
        }
        if self.commandType == "C_ARITHMETIC":
            if self.arg1 == "add":
                assemblyInstruction = "@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=D+M\n@SP\nM=M+1"
            elif self.arg1 == "sub":
                assemblyInstruction = "@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=M-D\n@SP\nM=M+1"
            elif self.arg1 == "neg":
                assemblyInstruction = "@SP\nM=M-1\nA=M\nM=-M\n@SP\nM=M+1"
            elif self.arg1 == "eq":
                assemblyInstruction = f"@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M-D\n@TRUE.{self.counter}\nD;JEQ\n@SP\nA=M\nM=0\n@SP\nM=M+1\n@CONTINUE.{self.counter}\n0;JMP\n(TRUE.{self.counter})\n@SP\nA=M\nM=-1\n@SP\nM=M+1\n(CONTINUE.{self.counter})"
            elif self.arg1 == "gt":
                assemblyInstruction = f"@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M-D\n@TRUE.{self.counter}\nD;JGT\n@SP\nA=M\nM=0\n@SP\nM=M+1\n@CONTINUE.{self.counter}\n0;JMP\n(TRUE.{self.counter})\n@SP\nA=M\nM=-1\n@SP\nM=M+1\n(CONTINUE.{self.counter})"
            elif self.arg1 == "lt":
                assemblyInstruction = f"@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M-D\n@TRUE.{self.counter}\nD;JLT\n@SP\nA=M\nM=0\n@SP\nM=M+1\n@CONTINUE.{self.counter}\n0;JMP\n(TRUE.{self.counter})\n@SP\nA=M\nM=-1\n@SP\nM=M+1\n(CONTINUE.{self.counter})"
            elif self.arg1 == "and":
                assemblyInstruction = "@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=D&M\n@SP\nM=M+1"
            elif self.arg1 == "or":
                assemblyInstruction = "@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=D|M\n@SP\nM=M+1"
            elif self.arg1 == "not":
                assemblyInstruction = "@SP\nM=M-1\nA=M\nM=!M\n@SP\nM=M+1"

        elif self.commandType == "C_PUSH":
            if self.memorySegment == "constant":
                assemblyInstruction = f"@{self.arg2}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1"
            elif self.memorySegment == "local" or self.memorySegment == "argument" or self.memorySegment == "this" or self.memorySegment == "that":
                assemblyInstruction = f"@{self.arg2}\nD=A\n@{Abreviations[self.memorySegment]}\nA=D+M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
            elif self.memorySegment == "temp":
                assemblyInstruction = f"@{self.arg2}\nD=A\n@5\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
            elif self.memorySegment == "pointer":
                assemblyInstruction = f"@{Abreviations[self.arg2]}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
            elif self.memorySegment == "static":
                assemblyInstruction = f"@{self.filename}.{self.arg2}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"

        elif self.commandType == "C_POP":
            if self.memorySegment == "local" or self.memorySegment == "argument" or self.memorySegment == "this" or self.memorySegment == "that":
                assemblyInstruction = f"@{self.arg2}\nD=A\n@{Abreviations[self.memorySegment]}\nD=D+M\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D"
            elif self.memorySegment == "temp":
                assemblyInstruction = f"@{self.arg2}\nD=A\n@5\nD=D+A\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D"
            elif self.memorySegment == "pointer":
                assemblyInstruction = f"@SP\nM=M-1\nA=M\nD=M\n@{Abreviations[self.arg2]}\nM=D"
            elif self.memorySegment == "static":
                assemblyInstruction = f"@SP\nM=M-1\nA=M\nD=M\n@{self.filename}.{self.arg2}\nM=D"

        elif self.commandType == "C_LABEL":
            assemblyInstruction = f"({self.arg1})"

        elif self.commandType == "C_GOTO":
            assemblyInstruction = f"@{self.arg1}\n0;JMP"

        elif self.commandType == "C_IF":
            assemblyInstruction = f"@SP\nM=M-1\nA=M\nD=M\n@{self.arg1}\nD;JGT"

        return assemblyInstruction
    
class CodeWriter:
    def __init__(self,directory,relevantVMInstructions,assemblyInstructions):
        self.directory=directory+".asm"
        self.filename=self.getFilename()
        self.relevantVMInstructions=relevantVMInstructions
        self.assemblyInstructions=assemblyInstructions
    
    def getFilename(self):
        if "\\" in self.directory:
            return self.directory.split("\\")[-1].split('.')[0].strip()
        else:
            return self.directory.split('.')[0].strip()

    def write(self):
        with open(self.directory.split(".")[0]+".asm", "w") as file:
            for i, instruction in enumerate(self.assemblyInstructions):
                if i < len(self.assemblyInstructions) - 1:
                    file.write("//"+self.relevantVMInstructions[i] + "\n")
                    file.write(instruction + "\n\n")
                else:
                    file.write("//"+self.relevantVMInstructions[i] + "\n")
                    file.write(instruction)
        print(f"File {self.filename}.asm has been created successfully")

class VMTranslator:
    def __init__(self,directory):
        self.directory=directory.strip()
        self.filename=self.getFilename()
        self.content = self.readFile()
        self.relevantVMInstructions = self.getVMInstructions()
        self.assemblyInstructions = self.getAssemblyInstructions()
        self.writeAssemblyFile()

    def getFilename(self):
        if "\\" in self.directory:
            return self.directory.split("\\")[-1].split('.')[0].strip()
        else:
            return self.directory.split('.')[0].strip()

    def readFile(self):
        with open(self.directory, "r") as file:
            return file.read()
        
    def getVMInstructions(self):
        LinesFile = self.content.split("\n")
        relevantVMInstructions = []
        for line in LinesFile:
            line = line.strip()
            if line != "" and not line.startswith("//"):
                if("//" in line):
                    relevantVMInstructions.append(line.split("//")[0].strip())
                else:
                    relevantVMInstructions.append(line.strip())
        return relevantVMInstructions
    
    def getAssemblyInstructions(self):
        assemblyInstructions = []
        parser=Parser(self.directory.split(".")[0].strip())
        for line in self.relevantVMInstructions:
            assemblyInstructions.append(parser(line))
        return assemblyInstructions
    
    def writeAssemblyFile(self):
        writer = CodeWriter(self.directory.split('.')[0].strip(),self.relevantVMInstructions, self.assemblyInstructions)
        writer.write()

VMTranslator("Project8\FibonacciSeries.vm")

