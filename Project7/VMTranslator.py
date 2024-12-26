class Parser:
    def __init__(self, filename):
        self.filename=filename

    def __call__(self, str):
        self.VMInstruction = str
        self.commandType = self.getCommandType(str)
        self.arg1 = self.getArg1()
        self.arg2 = self.getArg2()
        self.memorySegment = self.getMemorySegment()
        self.assemblyInstruction = self.getAssemblyInstruction()
        return self.assemblyInstruction

    def getCommandType(self, str):
        if "push" in str:
            return "C_PUSH"
        elif "pop" in str:
            return "C_POP"
        else:
            return "C_ARITHMETIC"
        
    def getArg1(self):
        if self.commandType == "C_ARITHMETIC":
            return self.VMInstruction.strip()
        else:
            return self.VMInstruction.split(" ")[0].strip()
    
    def getArg2(self):
        if self.commandType == "C_ARITHMETIC":
            return None
        else:
            return int(self.VMInstruction.split(" ")[-1].strip())
        
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
                assemblyInstruction = "@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M-D\n@TRUE\nD;JEQ\n@SP\nA=M\nM=0\n@SP\nM=M+1\n@CONTINUE\n0;JMP\n(TRUE)\n@SP\nA=M\nM=-1\n@SP\nM=M+1\n(CONTINUE)"
            elif self.arg1 == "gt":
                assemblyInstruction = "@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M-D\n@TRUE\nD;JGT\n@SP\nA=M\nM=0\n@SP\nM=M+1\n@CONTINUE\n0;JMP\n(TRUE)\n@SP\nA=M\nM=-1\n@SP\nM=M+1\n(CONTINUE)"
            elif self.arg1 == "lt":
                assemblyInstruction = "@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M-D\n@TRUE\nD;JLT\n@SP\nA=M\nM=0\n@SP\nM=M+1\n@CONTINUE\n0;JMP\n(TRUE)\n@SP\nA=M\nM=-1\n@SP\nM=M+1\n(CONTINUE)"
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
                assemblyInstruction = f"@{self.arg2}\nD=A\n@{Abreviations[self.memorySegment]}\nA=M+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
            elif self.memorySegment == "temp":
                assemblyInstruction = f"@{self.arg2}\nD=A\n@5\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
            elif self.memorySegment == "pointer":
                assemblyInstruction = f"@{Abreviations[self.arg2]}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
            elif self.memorySegment == "static":
                assemblyInstruction = f"@{self.filename}.{self.arg2}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"

        elif self.commandType == "C_POP":
            if self.memorySegment == "local" or self.memorySegment == "argument" or self.memorySegment == "this" or self.memorySegment == "that":
                assemblyInstruction = f"@{self.arg2}\nD=A\n@{Abreviations[self.memorySegment]}\nD=M+D\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D\n"
            elif self.memorySegment == "temp":
                assemblyInstruction = f"@{self.arg2}\nD=A\n@5\nD=A+D\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D\n"
            elif self.memorySegment == "pointer":
                assemblyInstruction = f"@SP\nM=M-1\nA=M\nD=M\n@{Abreviations[self.arg2]}\nM=D"
            elif self.memorySegment == "static":
                assemblyInstruction = f"@SP\nM=M-1\nA=M\nD=M\n@{self.filename}.{self.arg2}\nM=D"

        return assemblyInstruction
    
class CodeWriter:
    def __init__(self,filename,relevantVMInstructions,assemblyInstructions):
        self.filename=filename+".asm"
        self.relevantVMInstructions=relevantVMInstructions
        self.assemblyInstructions=assemblyInstructions

    def write(self):
        with open(self.filename.split(".")[0]+".asm", "w") as file:
            for i, instruction in enumerate(self.assemblyInstructions):
                if i < len(self.assemblyInstructions) - 1:
                    file.write("//"+self.relevantVMInstructions[i] + "\n")
                    file.write(instruction + "\n\n")
                else:
                    file.write("//"+self.relevantVMInstructions[i] + "\n")
                    file.write(instruction)
        print(f"File {self.filename}.asm has been created successfully")

class VMTranslator:
    def __init__(self,filename):
        self.filename=filename.strip()
        self.content = self.readFile()
        self.relevantVMInstructions = self.getVMInstructions()
        self.assemblyInstructions = self.getAssemblyInstructions()
        self.writeAssemblyFile()

    def readFile(self):
        with open(self.filename, "r") as file:
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
        parser=Parser(self.filename.split(".")[0].strip())
        for line in self.relevantVMInstructions:
            assemblyInstructions.append(parser(line))
        return assemblyInstructions
    
    def writeAssemblyFile(self):
        writer = CodeWriter(self.filename.split(".")[0].strip(),self.relevantVMInstructions, self.assemblyInstructions)
        writer.write()

translator=VMTranslator("Project7/test.vm")