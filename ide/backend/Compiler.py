import os

#Assembly to Hack

class ASMParser:
    def __init__(self,symbolTable, assemblyInstruction=""):
        self.assemblyInstruction = assemblyInstruction
        self.instructionType = self.getInstructionType()
        self.symbolTable=symbolTable
        self.freeRAMptr=16

    def __call__(self, str):
        self.assemblyInstruction = str
        self.instructionType = self.getInstructionType()
        return self.getHackInstruction()

    def getInstructionType(self):
        if self.assemblyInstruction.startswith("@"):
            return 0
        else:
            return 1

    def convertToBinary(self, str):
        decNum = int(str)
        binaryNum = bin(decNum)[2:]
        zeros = "0" * (16 - len(binaryNum))
        return zeros + binaryNum

    def getHackInstruction(self):
        if self.instructionType == 0:
            if self.assemblyInstruction[1:].isnumeric():
                return self.convertToBinary(self.assemblyInstruction[1:])
            else:
                if self.assemblyInstruction[1:] in self.symbolTable:
                    return self.convertToBinary(str(self.symbolTable[self.assemblyInstruction[1:]]))
                else:
                    self.symbolTable[self.assemblyInstruction[1:]] = self.freeRAMptr
                    self.freeRAMptr+=1
                    return self.convertToBinary(str(self.symbolTable[self.assemblyInstruction[1:]]))
        else:
            destSym = "null"
            compSym = "null"
            jumpSym = "null"
            if "=" in self.assemblyInstruction:
                destSym = self.assemblyInstruction.split("=")[0]
                rem = self.assemblyInstruction.split("=")[1]
                if ";" in rem:
                    compSym = rem.split(";")[0].strip()
                    jumpSym = rem.split(";")[1].strip()
                else:
                    compSym = rem.strip()
            else:
                if ";" in self.assemblyInstruction:
                    compSym = self.assemblyInstruction.split(";")[0].strip()
                    jumpSym = self.assemblyInstruction.split(";")[1].strip()
            # print(f"destSym: {destSym}, compSym: {compSym}, jumpSym: {jumpSym}")
            return "111" + self.getCompCode(compSym) + self.getDestCode(destSym) + self.getJumpCode(jumpSym)

    def getCompCode(self, str):
        compTable = {
            "0": "0101010",
            "1": "0111111",
            "-1": "0111010",
            "D": "0001100",
            "A": "0110000",
            "!D": "0001101",
            "!A": "0110001",
            "-D": "0001111",
            "-A": "0110011",
            "D+1": "0011111",
            "A+1": "0110111",
            "D-1": "0001110",
            "A-1": "0110010",
            "D+A": "0000010",
            "D-A": "0010011",
            "A-D": "0000111",
            "D&A": "0000000",
            "D|A": "0010101",
            "M": "1110000",
            "!M": "1110001",
            "-M": "1110011",
            "M+1": "1110111",
            "M-1": "1110010",
            "D+M": "1000010",
            "D-M": "1010011",
            "M-D": "1000111",
            "D&M": "1000000",
            "D|M": "1010101",
        }
        return compTable[str]

    def getDestCode(self, str):
        destTable = {
            "null": "000",
            "M": "001",
            "D": "010",
            "MD": "011",
            "A": "100",
            "AM": "101",
            "AD": "110",
            "AMD": "111",
        }
        return destTable[str]

    def getJumpCode(self, str):
        jumpTable = {
            "null": "000",
            "JGT": "001",
            "JEQ": "010",
            "JGE": "011",
            "JLT": "100",
            "JNE": "101",
            "JLE": "110",
            "JMP": "111",
        }
        return jumpTable[str]

    def parse(self):
        return self.getHackInstruction()

class ASMFile:
    def __init__(self, fileName):
        self.fileName = fileName
        self.content = self.readFile()
        self.LinesFile = self.getLinesFile()
        # print(f"LinesFile: {self.LinesFile}")
        self.relevantLinesLabels = self.getRelevantLinesLabels()
        # print(f"relevantLinesLabels: {self.relevantLinesLabels}")
        self.symbolTable = self.getSymbolTable()
        self.relevantLines = self.getRelevantLines()
        # print(f"relevantLines: {self.relevantLines}")
        self.freeBinaryString=self.getFreeBinaryString()
        self.hackInstructions = self.getHackInstructions()

    def readFile(self):
        with open(self.fileName, "r") as file:
            return file.read()
        
    def getLinesFile(self):
        return self.content.split("\n")


    def getRelevantLines(self):
        relevantLines = []
        for line in self.LinesFile:
            line = line.strip()
            if line.startswith("("):
                continue
            elif line != "" and not line.startswith("//"):
                if("//" in line):
                    relevantLines.append(line.split("//")[0].strip())
                else:
                    relevantLines.append(line.strip())

        return relevantLines
    
    def getRelevantLinesLabels(self):
        relevantLinesLabels = []
        for line in self.LinesFile:
            line = line.strip()
            if(line.startswith("(")):
                relevantLinesLabels.append(line)
            elif line != "" and not line.startswith("//"):
                if("//" in line):
                    relevantLinesLabels.append(line.split("//")[0].strip())
                else:
                    relevantLinesLabels.append(line.strip())

        return relevantLinesLabels
    
    def getFreeBinaryString(self):
        freeBinaryString = "1"*16
        freeBinaryString+=("0"*(24577-16))
        return freeBinaryString

    def getSymbolTable(self):
        symbolTable = {
            "SP": 0,
            "LCL": 1,
            "ARG": 2,
            "THIS": 3,
            "THAT": 4,
            "R0": 0,
            "R1": 1,
            "R2": 2,
            "R3": 3,
            "R4": 4,
            "R5": 5,
            "R6": 6,
            "R7": 7,
            "R8": 8,
            "R9": 9,
            "R10": 10,
            "R11": 11,
            "R12": 12,
            "R13": 13,
            "R14": 14,
            "R15": 15,
            "SCREEN": 16384,
            "KBD": 24576,
        }
        parser = ASMParser(symbolTable)
        i=0
        for line in self.relevantLinesLabels:
            if line.startswith("("):
                symbolTable[line[1:-1]] = i
            else:
                i+=1
        return symbolTable

    def getHackInstructions(self):
        hackInstructions = []
        parser = ASMParser(self.symbolTable)
        for line in self.relevantLines:
            # print(f"line: {line}")
            hackInstructions.append(parser(line))
        return hackInstructions

    def writeHackFile(self):
        with open(self.fileName.split(".")[0] + ".hack", "w") as file:
            for i, instruction in enumerate(self.hackInstructions):
                if i < len(self.hackInstructions) - 1:
                    file.write(instruction + "\n")
                else:
                    file.write(instruction)

            print(f'{self.fileName.split(".")[0]}.hack file created successfully')

#VM to Assembly

class VMParser:
    def __init__(self, directory,counter=1,returnCounter=1,callCounter=1):
        self.directory=directory
        self.filename=self.getFilename()
        self.counter=counter
        self.returnCounter=returnCounter
        self.callCounter=callCounter
    
    def getFilename(self):
        if "\\" in self.directory:
            return self.directory.split("\\")[-1].split('.')[0].strip()
        elif "/" in self.directory:
            return self.directory.split("/")[-1].split('.')[0].strip()
        else:
            return self.directory.split('.')[0].strip()

    def __call__(self, str):
        self.VMInstruction = str
        self.commandType = self.getCommandType(str)
        self.arg1 = self.getArg1()
        self.arg2 = self.getArg2()
        self.memorySegment = self.getMemorySegment()
        self.assemblyInstruction = self.getAssemblyInstruction()
        return self.assemblyInstruction
    
    def getCounters(self):
        return self.counter,self.returnCounter,self.callCounter

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
        elif "call" in str:
            return "C_CALL"
        elif "function" in str:
            return "C_FUNCTION"
        elif "return" in str:
            return "C_RETURN"
        else:
            return "C_ARITHMETIC"
        
    def getArg1(self):
        if self.commandType == "C_ARITHMETIC":
            return self.VMInstruction.strip()
        elif self.commandType == "C_LABEL" or self.commandType == "C_GOTO" or self.commandType=="C_IF":
            return self.VMInstruction.split(" ")[1].strip()
        elif self.commandType == "C_FUNCTION" or self.commandType == "C_CALL":
            return self.VMInstruction.split(" ")[-2].strip()
        elif self.commandType == "C_RETURN":
            return None
        else:
            return self.VMInstruction.split(" ")[0].strip()
    
    def getArg2(self):
        if self.commandType=="C_PUSH" or self.commandType=="C_POP":
            return int(self.VMInstruction.split(" ")[-1].strip())
        elif self.commandType=="C_FUNCTION" or self.commandType=="C_CALL":
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
                self.counter+=1
            elif self.arg1 == "gt":
                assemblyInstruction = f"@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M-D\n@TRUE.{self.counter}\nD;JGT\n@SP\nA=M\nM=0\n@SP\nM=M+1\n@CONTINUE.{self.counter}\n0;JMP\n(TRUE.{self.counter})\n@SP\nA=M\nM=-1\n@SP\nM=M+1\n(CONTINUE.{self.counter})"
                self.counter+=1
            elif self.arg1 == "lt":
                assemblyInstruction = f"@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M-D\n@TRUE.{self.counter}\nD;JLT\n@SP\nA=M\nM=0\n@SP\nM=M+1\n@CONTINUE.{self.counter}\n0;JMP\n(TRUE.{self.counter})\n@SP\nA=M\nM=-1\n@SP\nM=M+1\n(CONTINUE.{self.counter})"
                self.counter+=1
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
            assemblyInstruction = f"@SP\nM=M-1\nA=M\nD=M\n@{self.arg1}\nD;JNE"

        elif self.commandType == "C_FUNCTION":
            assemblyInstruction = f"({self.arg1})\n@{self.arg2}\nD=A\n({self.arg1}.LOOP)\n@{self.arg1}.END\nD;JEQ\n@SP\nA=M\nM=0\n@SP\nM=M+1\nD=D-1\n@{self.arg1}.LOOP\n0;JMP\n({self.arg1}.END)"

        elif self.commandType == "C_CALL":
            assemblyInstruction=f"@{self.arg1}$ret.{self.returnCounter}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@5\nD=A\n@{self.arg2}\nD=D+A\n@SP\nD=M-D\n@ARG\nM=D\n@SP\nD=M\n@LCL\nM=D\n@{self.arg1}\n0;JMP\n({self.arg1}$ret.{self.returnCounter})"
            self.returnCounter+=1

        elif self.commandType == "C_RETURN":
            assemblyInstruction=f"@LCL\nD=M\n@endFrame.{self.callCounter}\nM=D\n@5\nA=D-A\nD=M\n@retAddrs.{self.callCounter}\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@ARG\nA=M\nM=D\n@ARG\nD=M+1\n@SP\nM=D\n@endFrame.{self.callCounter}\nM=M-1\nA=M\nD=M\n@THAT\nM=D\n@endFrame.{self.callCounter}\nM=M-1\nA=M\nD=M\n@THIS\nM=D\n@endFrame.{self.callCounter}\nM=M-1\nA=M\nD=M\n@ARG\nM=D\n@endFrame.{self.callCounter}\nM=M-1\nA=M\nD=M\n@LCL\nM=D\n@retAddrs.{self.callCounter}\nA=M\n0;JMP"
            self.callCounter+=1

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
        elif "/" in self.directory:
            return self.directory.split("/")[-1].split('.')[0].strip()
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
        # print(f"File {self.filename}.asm has been created successfully")

class VMTranslatorFile:
    def __init__(self,directory,counter=1,returnCounter=1,callCounter=1):
        self.directory=directory.strip()
        self.filename=self.getFilename()
        self.counter=counter
        self.returnCounter=returnCounter
        self.callCounter=callCounter
        self.content = self.readFile()
        self.relevantVMInstructions = self.getVMInstructions()
        self.assemblyInstructions = self.getAssemblyInstructions()
        self.writeAssemblyFile()

    def getCounters(self):
        return self.counter,self.returnCounter,self.callCounter
    
    def getFilename(self):
        if "\\" in self.directory:
            return self.directory.split("\\")[-1].split('.')[0].strip()
        elif "/" in self.directory:
            return self.directory.split("/")[-1].split('.')[0].strip()
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
        parser=VMParser(self.directory.split(".")[0].strip(),self.counter,self.returnCounter,self.callCounter)
        for line in self.relevantVMInstructions:
            assemblyInstructions.append(parser(line))
        self.counter,self.returnCounter,self.callCounter=parser.getCounters()
        return assemblyInstructions
    
    def writeAssemblyFile(self):
        writer = CodeWriter(self.directory.split('.')[0].strip(),self.relevantVMInstructions, self.assemblyInstructions)
        writer.write()

class VMTranslator:
    def __init__(self,directory):
        self.directory=directory.strip()
        self.filename=self.getFilename()
        self.isFile=self.getIsFile()
        self.counter=1
        self.returnCounter=1
        self.callCounter=1
        self.handleFile()
        self.handleFolder()
        self.concatenateFiles()

    def getIsFile(self):
        if self.directory.endswith(".vm"):
            return True
        return False

    def getFilename(self):
        if "\\" in self.directory:
            return self.directory.split("\\")[-1].split('.')[0].strip()
        elif "/" in self.directory:
            return self.directory.split("/")[-1].split('.')[0].strip()
        else:
            return self.directory.split('.')[0].strip()    
        
    def handleFile(self):
        if self.isFile:
            vmt=VMTranslatorFile(self.directory,self.counter,self.returnCounter,self.callCounter)
    
    def handleFolder(self):
        if not self.isFile:
            for file in os.listdir(self.directory):
                if file.endswith(".vm"):
                    vmt=VMTranslatorFile(os.path.join(self.directory, file),self.counter,self.returnCounter,self.callCounter)
                    self.counter,self.returnCounter,self.callCounter=vmt.getCounters()

    def concatenateFiles(self):
        if not self.isFile:
            with open(f"{os.path.join(self.directory,self.filename)}.asm", "w") as outfile:
                outfile.write("//BootstrapCode\n@256\nD=A\n@SP\nM=D\n\n//call Sys.init\n@Sys.init$ret.0\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@5\nD=A\n@0\nD=D+A\n@SP\nD=M-D\n@ARG\nM=D\n@SP\nD=M\n@LCL\nM=D\n@Sys.init\n0;JMP\n(Sys.init$ret.0)\n\n")
                for file in os.listdir(self.directory):
                    if file.endswith(".asm") and file!=f"{self.filename}.asm":
                        with open(os.path.join(self.directory, file), "r") as infile:
                            outfile.write(infile.read())
                        outfile.write("\n\n")
                        os.remove(os.path.join(self.directory, file))
            print(f"File {os.path.join(self.directory,self.filename)}.asm has been created successfully")

# Code to VM
class JackTokenizerFile:
    def __init__(self,filePath):
        self.filePath = filePath
        self.fileContent = self.getFileContent()
        # print(repr(self.fileContent))
        self.multiLinesCommentsRemovedContent = self.removeMultiLinesComments()
        # print(repr(self.multiLinesCommentsRemovedContent))
        self.commentsRemovedContent=self.removeInlineComments()
        # print(repr(self.commentsRemovedContent))
        self.tokens = self.getTokens()
        # print(self.tokens)
        self.lenTokens = len(self.tokens)
        self.currNum = 0
        self.currentToken = None

    def getFileContent(self):
        with open(self.filePath) as file:
            return file.read()

    def removeMultiLinesComments(self):
        fileContent = self.fileContent
        CommentsRemovedContent = ""
        i = 0
        f = 0
        fstr=0
        n=len(fileContent)
        while(i<n):
            if(fileContent[i]=="\"" and fstr==0):
                fstr=1
            elif(fileContent[i]=="\"" and fstr==1):
                fstr=0

            if(f==0):
                if(i+2<n):
                    if(fileContent[i]=='/' and fileContent[i+1]=='*' and fileContent[i+2]=='*' and not fstr):
                        f=1
                        i+=3
                    else:
                        CommentsRemovedContent+=fileContent[i]
                        i+=1

                elif(i+1<n):
                    if(fileContent[i]=='/' and fileContent[i+1]=='*' and not fstr):
                        f=1
                        i+=2
                    else:
                        CommentsRemovedContent+=fileContent[i]
                        i+=1
                else:
                    CommentsRemovedContent+=fileContent[i]
                    i+=1
            else:
                if(i+2<n):
                    if(fileContent[i]=='*' and fileContent[i+1]=='/' and not fstr):
                        f=0
                        i+=2
                    else:
                        i+=1
                else:
                    i+=1
        return CommentsRemovedContent
    
    def removeInlineComments(self):
        fileContent = self.multiLinesCommentsRemovedContent
        CommentsRemovedContent = ""
        i = 0
        f = 0
        fstr=0
        n=len(fileContent)
        while(i<n):
            if(fileContent[i]=="\"" and fstr==0):
                fstr=1
            elif(fileContent[i]=="\"" and fstr==1):
                fstr=0

            if(f==0):
                if(i+1<n):
                    if(fileContent[i]=='/' and fileContent[i+1]=='/' and not fstr):
                        f=1
                        i+=2
                    else:
                        CommentsRemovedContent+=fileContent[i]
                        i+=1
                else:
                    CommentsRemovedContent+=fileContent[i]
                    i+=1
            else:
                if(i<n):
                    if(fileContent[i]=='\n' and not fstr):
                        f=0
                        i+=1
                    else:
                        i+=1
                else:
                    i+=1
        return CommentsRemovedContent

    def getTokens(self):
        fileContent = self.commentsRemovedContent
        tokens = []
        i = 0
        fstr=0
        n=len(fileContent)
        while(i<n):
            if(fileContent[i]=="\"" and fstr==0):
                fstr=1
            elif(fileContent[i]=="\"" and fstr==1):
                fstr=0

            if(fileContent[i] in ["{","}","(",")","[","]",".",",",";","+","-","*","/","&","|","<",">","=","~"]):
                tokens.append(fileContent[i])
                i+=1
            elif(fileContent[i]==" "):
                i+=1
            elif(fileContent[i]=="\n"):
                i+=1
            elif(fileContent[i]=="\t"):
                i+=1
            elif(fileContent[i]=="\""):
                j=i+1
                while(j<n and fileContent[j]!="\""):
                    j+=1
                tokens.append(fileContent[i:j+1])
                i=j+1
            else:
                j=i
                while(j<n and fileContent[j] not in ["{","}","(",")","[","]",".",",",";","+","-","*","/","&","|","<",">","=","~"," ","\n","\t","\r"]):
                    j+=1
                tokens.append(fileContent[i:j])
                i=j
        return tokens

    def tokenType(self):
            if(self.currentToken in ["class","constructor","function","method","field","static","var","int","char","boolean","void","true","false","null","this","let","do","if","else","while","return"]):
                return "KEYWORD"
            elif(self.currentToken in ["{","}","(",")","[","]",".",",",";","+","-","*","/","&amp;","|","&lt;","&gt;","=","~"]):
                return "SYMBOL"
            elif(self.currentToken[0]=="\""):
                return "STRING_CONST"
            elif(self.currentToken.isdigit()):
                return "INT_CONST"
            else:
                return "IDENTIFIER"
            
    #Method to get the token type in lowercase to be used in the xml file       
    def getTokenType(self):
        if(self.tokenType()=="KEYWORD"):
            return "keyword"
        elif(self.tokenType()=="SYMBOL"):
            return "symbol"
        elif(self.tokenType()=="STRING_CONST"):
            return "stringConstant"
        elif(self.tokenType()=="INT_CONST"):
            return "integerConstant"
        elif(self.tokenType()=="IDENTIFIER"):
            return "identifier"
        else:
            return None

    def keyWord(self):
        if(self.tokenType()=="KEYWORD"):
            return self.currentToken
        else:
            return None
        
    def symbol(self):
        if(self.tokenType()=="SYMBOL"):
            return self.currentToken
        else:
            return None
    
    def identifier(self):
        if(self.tokenType()=="IDENTIFIER"):
            return self.currentToken
        else:
            return None
        
    def intVal(self):
        if(self.tokenType()=="INT_CONST"):
            return int(self.currentToken)
        else:
            return None
        
    def stringVal(self):
        if(self.tokenType()=="STRING_CONST"):
            return self.currentToken[1:-1]
        else:
            return None

    def hasMoreTokens(self):
        return self.currNum<self.lenTokens

    def advance(self):
        if(self.hasMoreTokens()):
            self.currentToken = self.tokens[self.currNum]
            if(self.currentToken==">"):
                self.currentToken = "&gt;"
            elif(self.currentToken=="<"):
                self.currentToken = "&lt;"
            elif(self.currentToken=="&"):
                self.currentToken = "&amp;"
            self.currNum+=1
        else:
            self.currentToken = None 

    def get_xml(self, stringSymbolTable=None):
        currentToken=""
        if(self.currentToken[0]=="\""):
            currentToken = self.currentToken[1:-1]
        else:
            currentToken = self.currentToken
        if(self.tokenType()=="IDENTIFIER" and stringSymbolTable!=None):
            return "<" + self.getTokenType() +" "+ stringSymbolTable +" " + "> " + currentToken + " </" + self.getTokenType() + ">"    
        return "<" + self.getTokenType() + "> " + currentToken + " </" + self.getTokenType() + ">"
    
class SymbolTable:
    def __init__(self):
        self.classScope = {}
        self.subroutineScope = {}
        self.staticIndex = 0
        self.fieldIndex = 0
        self.argIndex = 0
        self.varIndex = 0

    def startSubroutine(self):
        self.subroutineScope = {}
        self.argIndex = 0
        self.varIndex = 0

    def define(self,name,type,kind):
        if(kind=="static"):
            self.classScope[name] = [type,kind,self.staticIndex]
            self.staticIndex+=1
        elif(kind=="field"):
            self.classScope[name] = [type,kind,self.fieldIndex]
            self.fieldIndex+=1
        elif(kind=="arg"):
            self.subroutineScope[name] = [type,kind,self.argIndex]
            self.argIndex+=1
        elif(kind=="var"):
            self.subroutineScope[name] = [type,kind,self.varIndex]
            self.varIndex+=1

    def varCount(self,kind):
        if(kind=="static"):
            return self.staticIndex
        elif(kind=="field"):
            return self.fieldIndex
        elif(kind=="arg"):
            return self.argIndex
        elif(kind=="var"):
            return self.varIndex

    def kindOf(self,name):
        if(name in self.subroutineScope):
            if(self.subroutineScope[name][1]=="arg"):
                return "argument"
            elif(self.subroutineScope[name][1]=="var"):
                return "local"
            elif(self.subroutineScope[name][1]=="field"):
                return "this"
            else:
                return self.subroutineScope[name][1]
        elif(name in self.classScope):
            if(self.classScope[name][1]=="field"):
                return "this"
            else:
                return self.classScope[name][1]
        else:
            return None

    def typeOf(self,name):
        if(name in self.subroutineScope):
            return self.subroutineScope[name][0]
        elif(name in self.classScope):
            return self.classScope[name][0]
        else:
            return None

    def indexOf(self,name):
        if(name in self.subroutineScope):
            return self.subroutineScope[name][2]
        elif(name in self.classScope):
            return self.classScope[name][2]
        else:
            return None

class VMWriter:
    def __init__(self,output_file):
        self.output_file = output_file
    
    def writePush(self,segment,index):
        self.output_file.write(f"    push {segment} {index}\n")

    def writePop(self,segment,index):
        self.output_file.write(f"    pop {segment} {index}\n")

    def writeArithmetic(self,command):
        self.output_file.write(f"    {command}\n")
    
    def writeLabel(self,label):
        self.output_file.write(f"label {label}\n")

    def writeGoto(self,label):
        self.output_file.write(f"    goto {label}\n")
    
    def writeIf(self,label):
        self.output_file.write(f"    if-goto {label}\n")

    def writeCall(self,name,nArgs):
        self.output_file.write(f"    call {name} {nArgs}\n")

    def writeFunction(self,name,nLocals):
        self.output_file.write(f"function {name} {nLocals}\n")

    def writeReturn(self):
        self.output_file.write(f"    return\n")

    def close(self):
        self.output_file.close()

class CompilationEngine:
    def __init__(self,tokenizer , vmWriter ,symbolTable):
        self.tokenizer = tokenizer
        self.vmWriter = vmWriter
        self.symbolTable = symbolTable
        self.className = None
        self.functionName = None
        self.nParams = 0
        self.nArgs = 0
        self.subroutineCallName=""
        self.labelCount=0
        self.subroutineKind=None

    #Program Structure
    def compileClass(self):
        self.tokenizer.advance()

        if(self.tokenizer.keyWord()!="class"):
            print("Error: Expected keyword class")
            return
        else:
            self.tokenizer.advance()
        
        if(self.tokenizer.tokenType()!="IDENTIFIER"):
            print("Error: Expected identifier")
            return
        else:
            self.className = self.tokenizer.currentToken
            self.tokenizer.advance()

        if(self.tokenizer.symbol()!="{"):
            print("Error: Expected symbol {")
            return
        else:
            self.tokenizer.advance()
        
        while self.tokenizer.keyWord() in ["static", "field"]:
            self.compileClassVarDec()

        while self.tokenizer.keyWord() in ["constructor", "function", "method"]:
            self.compileSubroutine()

        if(self.tokenizer.symbol()!="}"):
            print("Error: Expected symbol }")
            return
        else:
            self.tokenizer.advance()

        # print(self.symbolTable.classScope)

    def compileClassVarDec(self):
        currkind=None
        currType=None

        if(self.tokenizer.keyWord() not in ["static", "field"]):
            print("Error: Expected keyword static or field")
            return
        else:
            currkind = self.tokenizer.keyWord()
            self.tokenizer.advance()

        if(self.tokenizer.keyWord() not in ["int", "char", "boolean"] and self.tokenizer.tokenType()!="IDENTIFIER"):
            print("Error: Expected keyword int, char, boolean or class name")
            return
        else:
            currType = self.tokenizer.keyWord() or self.tokenizer.identifier()
            self.tokenizer.advance()

        if(self.tokenizer.tokenType()!="IDENTIFIER"):
            print("Error: Expected variable name")
            return
        else:
            self.symbolTable.define(self.tokenizer.currentToken,currType,currkind)
            self.tokenizer.advance()

        while self.tokenizer.symbol()==",":
            self.tokenizer.advance()

            if(self.tokenizer.tokenType()!="IDENTIFIER"):
                print("Error: Expected variable name")
                return
            else:
                self.symbolTable.define(self.tokenizer.currentToken,currType,currkind)
                self.tokenizer.advance()

        if(self.tokenizer.symbol()!=";"):
            print("Error: Expected symbol ;")
            return
        else:
            self.tokenizer.advance()

    def compileSubroutine(self):

        isVoid=False

        if(self.tokenizer.keyWord() not in ["constructor", "function", "method"]):
            print("Error: Expected keyword constructor, function or method")
            return
        else:
            self.symbolTable.startSubroutine()
            self.subroutineKind=self.tokenizer.keyWord()
            if(self.tokenizer.keyWord()=="method"):
                self.symbolTable.define("this",self.className,"arg")
                self.nParams = 1
            else:
                self.nParams = 0
            self.tokenizer.advance()

        if(self.tokenizer.keyWord() not in ["void", "int", "char", "boolean"] and self.tokenizer.tokenType()!="IDENTIFIER"):
            print("Error: Expected keyword void, int, char, boolean or class name")
            return
        else:
            if(self.tokenizer.keyWord()=="void"):
                isVoid=True
            self.tokenizer.advance()

        if(self.tokenizer.tokenType()!="IDENTIFIER"):
            print("Error: Expected subroutine name")
            return
        else:
            self.functionName = self.tokenizer.currentToken
            self.tokenizer.advance()


        if(self.tokenizer.symbol()!="("):
            print("Error: Expected symbol (")
            return
        else:
            self.tokenizer.advance()

        self.compileParameterList()

        if(self.tokenizer.symbol()!=")"):
            print("Error: Expected symbol )")
            return
        else:
            self.tokenizer.advance()

        self.compileSubroutineBody()


        if(isVoid):
            self.vmWriter.writePush("constant",0)
            self.vmWriter.writeReturn()

        # print(self.symbolTable.subroutineScope)

    def compileParameterList(self):

        currType=None

        if(self.tokenizer.keyWord() in ["int", "char", "boolean"] or self.tokenizer.tokenType()=="IDENTIFIER"):
            if(self.tokenizer.keyWord() not in ["int", "char", "boolean"] and self.tokenizer.tokenType()!="IDENTIFIER"):
                print("Error: Expected keyword int, char, boolean or class name")
                return
            else:
                currType = self.tokenizer.keyWord() or self.tokenizer.identifier()
                self.tokenizer.advance()

            if(self.tokenizer.tokenType()!="IDENTIFIER"):
                print("Error: Expected variable name")
                return
            else:
                self.symbolTable.define(self.tokenizer.currentToken,currType,"arg")
                self.nParams+=1
                self.tokenizer.advance()

            while self.tokenizer.symbol()==",":
                self.tokenizer.advance()

                if(self.tokenizer.keyWord() not in ["int", "char", "boolean"] and self.tokenizer.tokenType()!="IDENTIFIER"):
                    print("Error: Expected keyword int, char, boolean or class name")
                    return
                else:
                    currType = self.tokenizer.keyWord()
                    self.tokenizer.advance()

                if(self.tokenizer.tokenType()!="IDENTIFIER"):
                    print("Error: Expected variable name")
                    return
                else:
                    self.symbolTable.define(self.tokenizer.currentToken,currType,"arg")
                    self.nParams+=1
                    self.tokenizer.advance()

    def compileSubroutineBody(self):

        if(self.tokenizer.symbol()!="{"):
            print("Error: Expected symbol {")
            return
        else:
            self.tokenizer.advance()

        while self.tokenizer.keyWord()=="var":
            self.compileVarDec()

        self.vmWriter.writeFunction(f"{self.className}.{self.functionName}",self.symbolTable.varCount("var"))
        if(self.subroutineKind=="constructor"):
                self.vmWriter.writePush("constant",self.symbolTable.varCount("field"))
                self.vmWriter.writeCall("Memory.alloc",1)
                self.vmWriter.writePop("pointer",0)
        elif(self.subroutineKind=="method"):
            self.vmWriter.writePush("argument",0)
            self.vmWriter.writePop("pointer",0)
        

        self.compileStatements()

        if(self.tokenizer.symbol()!="}"):
            print("Error: Expected symbol }")
            return
        else:
            self.tokenizer.advance()

    def compileVarDec(self):
        currKind=None
        currType=None

        if(self.tokenizer.keyWord()!="var"):
            print("Error: Expected keyword var")
            return
        else:
            currKind = self.tokenizer.keyWord()
            self.tokenizer.advance()

        if(self.tokenizer.keyWord() not in ["int", "char", "boolean"] and self.tokenizer.tokenType()!="IDENTIFIER"):
            print("Error: Expected keyword int, char, boolean or class name")
            return
        else:
            currType = self.tokenizer.keyWord() or self.tokenizer.identifier()
            self.tokenizer.advance()

        if(self.tokenizer.tokenType()!="IDENTIFIER"):
            print("Error: Expected variable name")
            return
        else:
            self.symbolTable.define(self.tokenizer.currentToken,currType,currKind)
            self.tokenizer.advance()

        while self.tokenizer.symbol()==",":
            self.tokenizer.advance()

            if(self.tokenizer.tokenType()!="IDENTIFIER"):
                print("Error: Expected variable name")
                return
            else:
                self.symbolTable.define(self.tokenizer.currentToken,currType,currKind)
                self.tokenizer.advance()

        if(self.tokenizer.symbol()!=";"):
            print("Error: Expected symbol ;")
            return
        else:
            self.tokenizer.advance()

    #Statements
    def compileStatements(self):

        while self.tokenizer.keyWord() in ["let", "if", "while", "do", "return"]:
            if(self.tokenizer.keyWord()=="let"):
                self.compileLet()
            elif(self.tokenizer.keyWord()=="if"):
                self.compileIf()
            elif(self.tokenizer.keyWord()=="while"):
                self.compileWhile()
            elif(self.tokenizer.keyWord()=="do"):
                self.compileDo()
            elif(self.tokenizer.keyWord()=="return"):
                self.compileReturn()

    def compileLet(self):

        letLHS=None
        fArr=False

        if(self.tokenizer.keyWord()!="let"):
            print("Error: Expected keyword let")
            return
        else:
            self.tokenizer.advance()

        if(self.tokenizer.tokenType()!="IDENTIFIER"):
            print("Error: Expected variable name")
            return
        else:
            letLHS = self.tokenizer.currentToken
            self.tokenizer.advance()

        if(self.tokenizer.symbol()=="["):
            self.tokenizer.advance()
            self.compileExpression()

            if(self.symbolTable.typeOf(letLHS)=="Array"):
                self.vmWriter.writePush(self.symbolTable.kindOf(letLHS),self.symbolTable.indexOf(letLHS))
                self.vmWriter.writeArithmetic("add")
                fArr=True

            if(self.tokenizer.symbol()!="]"):
                print("Error: Expected symbol ]")
                return
            else:
                self.tokenizer.advance()

        if(self.tokenizer.symbol()!="="):
            print("Error: Expected symbol =")
            return
        else:
            self.tokenizer.advance()

        self.compileExpression()

        if(fArr):
            self.vmWriter.writePop("temp",0)
            self.vmWriter.writePop("pointer",1)
            self.vmWriter.writePush("temp",0)
            self.vmWriter.writePop("that",0)
        else:
            self.vmWriter.writePop(self.symbolTable.kindOf(letLHS),self.symbolTable.indexOf(letLHS))

        if(self.tokenizer.symbol()!=";"):
            print("Error: Expected symbol ;")
            return
        else:
            self.tokenizer.advance()

    def compileIf(self):
        if(self.tokenizer.keyWord()!="if"):
            print("Error: Expected keyword if")
            return
        else:
            self.tokenizer.advance()

        if(self.tokenizer.symbol()!="("):
            print("Error: Expected symbol (")
            return
        else:
            self.tokenizer.advance()

        self.compileExpression()
        self.vmWriter.writeArithmetic("not")

        if(self.tokenizer.symbol()!=")"):
            print("Error: Expected symbol )")
            return
        else:
            self.tokenizer.advance()

        if(self.tokenizer.symbol()!="{"):
            print("Error: Expected symbol {")
            return
        else:
            self.tokenizer.advance()

        tempLabelCount1=self.labelCount
        tempLabelCount2=self.labelCount+1
        self.labelCount+=2


        self.vmWriter.writeIf(f"{self.className}_{tempLabelCount2}")
        self.compileStatements()
        self.vmWriter.writeGoto(f"{self.className}_{tempLabelCount1}")

        if(self.tokenizer.symbol()!="}"):
            print("Error: Expected symbol }")
            return
        else:
            self.tokenizer.advance()

        self.vmWriter.writeLabel(f"{self.className}_{tempLabelCount2}")
        if(self.tokenizer.keyWord()=="else"):
            self.tokenizer.advance()

            if(self.tokenizer.symbol()!="{"):
                print("Error: Expected symbol {")
                return
            else:
                self.tokenizer.advance()

            self.compileStatements()

            if(self.tokenizer.symbol()!="}"):
                print("Error: Expected symbol }")
                return
            else:
                self.tokenizer.advance()

        self.vmWriter.writeLabel(f"{self.className}_{tempLabelCount1}")

    def compileWhile(self):

        tempLabelCount1=self.labelCount
        tempLabelCount2=self.labelCount+1
        self.labelCount+=2
        self.vmWriter.writeLabel(f"{self.className}_{tempLabelCount1}")

        if(self.tokenizer.keyWord()!="while"):
            print("Error: Expected keyword while")
            return
        else:
            self.tokenizer.advance()

        if(self.tokenizer.symbol()!="("):
            print("Error: Expected symbol (")
            return
        else:
            self.tokenizer.advance()

        self.compileExpression()

        self.vmWriter.writeArithmetic("not")

        if(self.tokenizer.symbol()!=")"):
            print("Error: Expected symbol )")
            return
        else:
            self.tokenizer.advance()

        if(self.tokenizer.symbol()!="{"):
            print("Error: Expected symbol {")
            return
        else:
            self.tokenizer.advance()

        self.vmWriter.writeIf(f"{self.className}_{tempLabelCount2}")
        self.compileStatements()
        self.vmWriter.writeGoto(f"{self.className}_{tempLabelCount1}")

        self.vmWriter.writeLabel(f"{self.className}_{tempLabelCount2}")

        if(self.tokenizer.symbol()!="}"):
            print("Error: Expected symbol }")
            return
        else:
            self.tokenizer.advance()
        
    def compileDo(self):

        if(self.tokenizer.keyWord()!="do"):
            print("Error: Expected keyword do")
            return
        else:
            self.tokenizer.advance()

        self.compileSubroutineCall()

        if(self.tokenizer.symbol()!=";"):
            print("Error: Expected symbol ;")
            return
        else:
            self.tokenizer.advance()

        self.vmWriter.writePop("temp",0)

    def compileReturn(self):
        if(self.tokenizer.keyWord()!="return"):
            print("Error: Expected keyword return")
            return
        else:
            self.tokenizer.advance()

        if(self.tokenizer.symbol()!=";"):
            self.compileExpression()
            self.vmWriter.writeReturn()

        if(self.tokenizer.symbol()!=";"):
            print("Error: Expected symbol ;")
            return
        else:
            self.tokenizer.advance()


    #Expressions
    def compileExpression(self):

        self.compileTerm()

        while self.tokenizer.symbol() in ["+", "-", "*", "/", "&amp;", "|", "&lt;", "&gt;", "="]:
            op=""
            if(self.tokenizer.symbol()=="+"):
                op="add"
            elif(self.tokenizer.symbol()=="-"):
                op="sub"
            elif(self.tokenizer.symbol()=="*"):
                op="call Math.multiply 2"
            elif(self.tokenizer.symbol()=="/"):
                op="call Math.divide 2"
            elif(self.tokenizer.symbol()=="&amp;"):
                op="and"
            elif(self.tokenizer.symbol()=="|"):
                op="or"
            elif(self.tokenizer.symbol()=="&lt;"):
                op="lt"
            elif(self.tokenizer.symbol()=="&gt;"):
                op="gt"
            elif(self.tokenizer.symbol()=="="):
                op="eq"
            self.tokenizer.advance()
            self.compileTerm()
            self.vmWriter.writeArithmetic(op)

    def compileTerm(self):

        if(self.tokenizer.tokenType()=="INT_CONST"):
            self.vmWriter.writePush("constant",self.tokenizer.intVal())
            self.tokenizer.advance()
        elif(self.tokenizer.tokenType()=="STRING_CONST"):
            str=self.tokenizer.stringVal()
            length=len(str)
            self.vmWriter.writePush("constant",length)
            self.vmWriter.writeCall("String.new",1)
            for i in range(length):
                self.vmWriter.writePush("constant",ord(str[i]))
                self.vmWriter.writeCall("String.appendChar",2)
            self.tokenizer.advance()
        elif(self.tokenizer.keyWord() in ["true", "false", "null", "this"]):
            if(self.tokenizer.keyWord()=="true"):
                self.vmWriter.writePush("constant",1)
                self.vmWriter.writeArithmetic("neg")
            elif(self.tokenizer.keyWord()=="false" or self.tokenizer.keyWord()=="null"):
                self.vmWriter.writePush("constant",0)
            elif(self.tokenizer.keyWord()=="this"):
                self.vmWriter.writePush("pointer",0)
            self.tokenizer.advance()
        elif(self.tokenizer.tokenType()=="IDENTIFIER"):
            tempName=self.tokenizer.identifier()
            self.tokenizer.advance()

            if(self.tokenizer.symbol()=="["):
                self.tokenizer.advance()
                self.compileExpression()
                if(self.symbolTable.typeOf(tempName)=="Array"):
                    self.vmWriter.writePush(self.symbolTable.kindOf(tempName),self.symbolTable.indexOf(tempName))
                    self.vmWriter.writeArithmetic("add")
                    self.vmWriter.writePop("pointer",1)
                    self.vmWriter.writePush("that",0)
                if(self.tokenizer.symbol()!="]"):
                    print("Error: Expected symbol ]")
                    return
                else:
                    self.tokenizer.advance()

            elif(self.tokenizer.symbol()=="(" or self.tokenizer.symbol()=="."):
                self.subroutineCallName+=tempName
                self.compileSubroutineCall()
            else:
                self.vmWriter.writePush(self.symbolTable.kindOf(tempName),self.symbolTable.indexOf(tempName))


        elif(self.tokenizer.symbol()=="("):
            self.tokenizer.advance()
            self.compileExpression()

            if(self.tokenizer.symbol()!=")"):
                print("Error: Expected symbol )")
                return
            else:
                self.tokenizer.advance()
        elif(self.tokenizer.symbol() in ["-", "~"]):
            op=self.tokenizer.symbol()
            self.tokenizer.advance()
            self.compileTerm()
            if(op=="-"):
                self.vmWriter.writeArithmetic("neg")
            elif(op=="~"):
                self.vmWriter.writeArithmetic("not")

    def compileSubroutineCall(self):

        callName=""
        flagNArgs=False

        if(self.tokenizer.symbol()=="."):
            callName+=self.subroutineCallName
            if(callName in self.symbolTable.classScope or callName in self.symbolTable.subroutineScope):
                if(callName in self.symbolTable.classScope):
                    self.vmWriter.writePush("this",self.symbolTable.indexOf(callName))
                else:
                    self.vmWriter.writePush("local",self.symbolTable.indexOf(callName))
                callName=self.symbolTable.typeOf(callName)
                flagNArgs=True
            self.subroutineCallName=""
            callName+="."
            self.tokenizer.advance()

            if(self.tokenizer.tokenType()!="IDENTIFIER"):
                print("Error: Expected subroutine name")
                return
            else:
                callName+=self.tokenizer.currentToken
                self.tokenizer.advance()
        elif(self.tokenizer.tokenType()=="IDENTIFIER"):
            callName+=self.tokenizer.currentToken
            if(self.subroutineKind=="method" or self.subroutineKind=="function" or self.subroutineKind=="constructor"):
                if(callName in self.symbolTable.classScope or callName in self.symbolTable.subroutineScope):
                    if(callName in self.symbolTable.classScope):
                        self.vmWriter.writePush("this",self.symbolTable.indexOf(callName))
                    else:
                        self.vmWriter.writePush("local",self.symbolTable.indexOf(callName))
                    callName=self.symbolTable.typeOf(callName)
                    flagNArgs=True
            self.tokenizer.advance()
            if(self.tokenizer.symbol()=="."):
                callName+="."
                self.tokenizer.advance()
                if(self.tokenizer.tokenType()!="IDENTIFIER"):
                    print("Error: Expected subroutine name")
                    return
                else:
                    callName+=self.tokenizer.currentToken
                    self.tokenizer.advance()
            else:
                callName=f"{self.className}.{callName}"
                self.vmWriter.writePush("pointer",0)
                flagNArgs=True
                
        if(self.tokenizer.symbol()!="("):
            print("Error: Expected symbol (")
            return
        else:
            self.tokenizer.advance()

        self.compileExpressionList()

        if(self.tokenizer.symbol()!=")"):
            print("Error: Expected symbol )")
            return
        else:
            self.tokenizer.advance()
        if(flagNArgs):
            self.vmWriter.writeCall(callName,self.nArgs+1)
        else:
            self.vmWriter.writeCall(callName,self.nArgs)

    def compileExpressionList(self):

        self.nArgs = 0

        if(self.tokenizer.symbol()!=")"):
            self.nArgs+=1
            self.compileExpression()

            while self.tokenizer.symbol()==",":
                self.tokenizer.advance()
                self.nArgs+=1
                self.compileExpression()

class JackCompiler:
    def __init__(self,directoryPath):
        self.directoryPath = directoryPath
        self.filesJack = self.getFilesJack()
        self.createVM()
        self.createASM()
        self.filesASM = self.getFilesASM()
        self.creatHack()

    def getFilesJack(self):
        files=[]
        for file in os.listdir(self.directoryPath):
            if file.endswith(".jack"):
                files.append(file)
        return files
    
    def getFilesVM(self):
        files=[]
        for file in os.listdir(self.directoryPath):
            if file.endswith(".vm"):
                files.append(file)
        return files

    def createVM(self):
        for file in self.filesJack:
            # print(file)
            tokenizer = JackTokenizerFile(self.directoryPath + "/" + file)
            output_file = open(self.directoryPath + "/" + file[:-5] + ".vm", "w")
            output_file.write(f"// Compiled {file}:\n")
            vmWriter = VMWriter(output_file)
            symbolTable=SymbolTable()
            compilationEngine = CompilationEngine(tokenizer,vmWriter,symbolTable)
            compilationEngine.compileClass()
            output_file.close()

    def createASM(self):
        # print(self.directoryPath)
        VMTranslator(self.directoryPath)

    def getFilesASM(self):
        files=[]
        for file in os.listdir(self.directoryPath):
            if file.endswith(".asm"):
                files.append(file)
        return files
    
    def creatHack(self):
        for file in self.filesASM:
            # print(file)
            asmFile=ASMFile(os.path.join(self.directoryPath, file))
            asmFile.writeHackFile()
