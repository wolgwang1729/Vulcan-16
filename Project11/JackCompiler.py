import os

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
            return self.subroutineScope[name][1]
        elif(name in self.classScope):
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
            currType = self.tokenizer.keyWord()
            self.tokenizer.advance()

        if(self.tokenizer.tokenType()!="IDENTIFIER"):
            print("Error: Expected variable name")
            return
        else:
            self.symbolTable.define(self.tokenizer.currentToken,currType,currkind)
            self.tokenizer.advance()

        while self.tokenizer.symbol()==",":
            self.write(self.tokenizer.get_xml())
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

    def compileParameterList(self):

        currType=None

        if(self.tokenizer.keyWord() in ["int", "char", "boolean"] or self.tokenizer.tokenType()=="IDENTIFIER"):
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

            while self.tokenizer.symbol()==",":
                self.write(self.tokenizer.get_xml())
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
            currType = self.tokenizer.keyWord()
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

        self.vmWriter.writePop(self.symbolTable.kindOf(letLHS),self.symbolTable.indexOf(letLHS))

        if(self.tokenizer.symbol()!=";"):
            print("Error: Expected symbol ;")
            return
        else:
            self.tokenizer.advance()

        print(self.symbolTable.subroutineScope)

    def compileIf(self):
        self.write("<ifStatement>")
        self.indentation += 1

        if(self.tokenizer.keyWord()!="if"):
            print("Error: Expected keyword if")
            return
        else:
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()

        if(self.tokenizer.symbol()!="("):
            print("Error: Expected symbol (")
            return
        else:
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()

        self.compileExpression()

        if(self.tokenizer.symbol()!=")"):
            print("Error: Expected symbol )")
            return
        else:
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()

        if(self.tokenizer.symbol()!="{"):
            print("Error: Expected symbol {")
            return
        else:
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()

        self.compileStatements()

        if(self.tokenizer.symbol()!="}"):
            print("Error: Expected symbol }")
            return
        else:
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()

        if(self.tokenizer.keyWord()=="else"):
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()

            if(self.tokenizer.symbol()!="{"):
                print("Error: Expected symbol {")
                return
            else:
                self.write(self.tokenizer.get_xml())
                self.tokenizer.advance()

            self.compileStatements()

            if(self.tokenizer.symbol()!="}"):
                print("Error: Expected symbol }")
                return
            else:
                self.write(self.tokenizer.get_xml())
                self.tokenizer.advance()

        self.indentation -= 1
        self.write("</ifStatement>")

    def compileWhile(self):
        self.write("<whileStatement>")
        self.indentation += 1

        if(self.tokenizer.keyWord()!="while"):
            print("Error: Expected keyword while")
            return
        else:
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()

        if(self.tokenizer.symbol()!="("):
            print("Error: Expected symbol (")
            return
        else:
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()

        self.compileExpression()

        if(self.tokenizer.symbol()!=")"):
            print("Error: Expected symbol )")
            return
        else:
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()

        if(self.tokenizer.symbol()!="{"):
            print("Error: Expected symbol {")
            return
        else:
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()

        self.compileStatements()

        if(self.tokenizer.symbol()!="}"):
            print("Error: Expected symbol }")
            return
        else:
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()

        self.indentation -= 1
        self.write("</whileStatement>")

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
            self.tokenizer.advance()
        elif(self.tokenizer.keyWord() in ["true", "false", "null", "this"]):
            if(self.tokenizer.keyWord()=="true"):
                self.vmWriter.writePush("constant",-1)
            elif(self.tokenizer.keyWord()=="false" or self.tokenizer.keyWord()=="null"):
                self.vmWriter.writePush("constant",0)
            elif(self.tokenizer.keyWord()=="this"):
                self.vmWriter.writePush("pointer",0)
            self.tokenizer.advance()
        elif(self.tokenizer.tokenType()=="IDENTIFIER"):
            tempName=self.tokenizer.identifier()
            self.tokenizer.advance()

            if(self.tokenizer.symbol()=="["):
                self.write(self.tokenizer.get_xml())
                self.tokenizer.advance()
                self.compileExpression()

                if(self.tokenizer.symbol()!="]"):
                    print("Error: Expected symbol ]")
                    return
                else:
                    self.write(self.tokenizer.get_xml())
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

        if(self.tokenizer.symbol()=="."):
            callName+=self.subroutineCallName
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
        self.files = self.getFiles()
        self.createVM()

    def getFiles(self):
        files=[]
        for file in os.listdir(self.directoryPath):
            if file.endswith(".jack"):
                files.append(file)
        return files

    def createVM(self):
        for file in self.files:
            print(file)
            tokenizer = JackTokenizerFile(self.directoryPath + "/" + file)
            output_file = open(self.directoryPath + "/" + file[:-5] + ".vm", "w")
            vmWriter = VMWriter(output_file)
            symbolTable=SymbolTable()
            compilationEngine = CompilationEngine(tokenizer,vmWriter,symbolTable)
            compilationEngine.compileClass()
            output_file.close()

JackCompiler("Project11\TestFiles\seven")
