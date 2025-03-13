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

asmFile = ASMFile("Project6\ASM Files\Max.asm")
asmFile.writeHackFile()