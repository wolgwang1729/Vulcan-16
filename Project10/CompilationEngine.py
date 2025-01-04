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
            elif(self.currentToken in ["{","}","(",")","[","]",".",",",";","+","-","*","/","&","|","<",">","=","~"]):
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
            return self.currentToken.upper()
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
            if(self.currentToken[0]=="\""):
                self.currentToken = self.currentToken[1:-1]
            elif(self.currentToken==">"):
                self.currentToken = "&gt;"
            elif(self.currentToken=="<"):
                self.currentToken = "&lt;"
            elif(self.currentToken=="&"):
                self.currentToken = "&amp;"
            self.currNum+=1
        else:
            self.currentToken = None 

    def get_xml(self):
        return "<" + self.getTokenType() + "> " + self.currentToken + " </" + self.getTokenType() + ">"


class CompilationEngineFile:
    def __init__(self, tokenizer, output_file):
        self.tokenizer = tokenizer
        self.output_file = output_file
        self.indentation = 0

    def write(self, text):
        self.output_file.write("  " * self.indentation + text + "\n")

    #Program Structure
    def compileClass(self):
        self.write("<class>")
        self.indentation += 1
        self.tokenizer.advance()

        if(self.tokenizer.keyWord()!="class"):
            print("Error: Expected keyword class")
            return
        else:
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()
        
        if(self.tokenizer.tokenType()!="IDENTIFIER"):
            print("Error: Expected identifier")
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
        
        while self.tokenizer.keyWord() in ["static", "field"]:
            self.compileClassVarDec()

        while self.tokenizer.keyWord() in ["constructor", "function", "method"]:
            self.compileSubroutine()

        if(self.tokenizer.symbol()!="}"):
            print("Error: Expected symbol }")
            return
        else:
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()

        self.indentation -= 1
        self.write("</class>")

    def compileClassVarDec(self):
        self.write("<classVarDec>")
        self.indentation += 1

        if(self.tokenizer.keyWord() not in ["static", "field"]):
            print("Error: Expected keyword static or field")
            return
        else:
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()

        if(self.tokenizer.keyWord() not in ["int", "char", "boolean"] and self.tokenizer.tokenType()!="IDENTIFIER"):
            print("Error: Expected keyword int, char, boolean or class name")
            return
        else:
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()

        if(self.tokenizer.tokenType()!="IDENTIFIER"):
            print("Error: Expected variable name")
            return
        else:
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()

        while self.tokenizer.symbol()==",":
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()

            if(self.tokenizer.tokenType()!="IDENTIFIER"):
                print("Error: Expected variable name")
                return
            else:
                self.write(self.tokenizer.get_xml())
                self.tokenizer.advance()

        if(self.tokenizer.symbol()!=";"):
            print("Error: Expected symbol ;")
            return
        else:
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()

        self.indentation -= 1
        self.write("</classVarDec>")

    def compileSubroutine(self):
        self.write("<subroutineDec>")
        self.indentation += 1

        if(self.tokenizer.keyWord() not in ["constructor", "function", "method"]):
            print("Error: Expected keyword constructor, function or method")
            return
        else:
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()

        if(self.tokenizer.keyWord() not in ["void", "int", "char", "boolean"] and self.tokenizer.tokenType()!="IDENTIFIER"):
            print("Error: Expected keyword void, int, char, boolean or class name")
            return
        else:
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()

        if(self.tokenizer.tokenType()!="IDENTIFIER"):
            print("Error: Expected subroutine name")
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

        self.compileParameterList()

        if(self.tokenizer.symbol()!=")"):
            print("Error: Expected symbol )")
            return
        else:
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()

        self.compileSubroutineBody()

        self.indentation -= 1
        self.write("</subroutineDec>")

    def compileParameterList(self):
        self.write("<parameterList>")
        self.indentation += 1

        if(self.tokenizer.keyWord() not in ["int", "char", "boolean"] and self.tokenizer.tokenType()!="IDENTIFIER"):
            print("Error: Expected keyword int, char, boolean or class name")
            return
        else:
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()

        if(self.tokenizer.tokenType()!="IDENTIFIER"):
            print("Error: Expected variable name")
            return
        else:
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()

        while self.tokenizer.symbol()==",":
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()

            if(self.tokenizer.keyWord() not in ["int", "char", "boolean"] and self.tokenizer.tokenType()!="IDENTIFIER"):
                print("Error: Expected keyword int, char, boolean or class name")
                return
            else:
                self.write(self.tokenizer.get_xml())
                self.tokenizer.advance()

            if(self.tokenizer.tokenType()!="IDENTIFIER"):
                print("Error: Expected variable name")
                return
            else:
                self.write(self.tokenizer.get_xml())
                self.tokenizer.advance()

        self.indentation -= 1
        self.write("</parameterList>")

    def compileSubroutineBody(self):
        self.write("<subroutineBody>")
        self.indentation += 1

        if(self.tokenizer.symbol()!="{"):
            print("Error: Expected symbol {")
            return
        else:
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()

        while self.tokenizer.keyWord()=="var":
            self.compileVarDec()

        self.compileStatements()

        if(self.tokenizer.symbol()!="}"):
            print("Error: Expected symbol }")
            return
        else:
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()

        self.indentation -= 1
        self.write("</subroutineBody>")

    def compileVarDec(self):
        self.write("<varDec>")
        self.indentation += 1

        if(self.tokenizer.keyWord()!="var"):
            print("Error: Expected keyword var")
            return
        else:
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()

        if(self.tokenizer.keyWord() not in ["int", "char", "boolean"] and self.tokenizer.tokenType()!="IDENTIFIER"):
            print("Error: Expected keyword int, char, boolean or class name")
            return
        else:
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()

        if(self.tokenizer.tokenType()!="IDENTIFIER"):
            print("Error: Expected variable name")
            return
        else:
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()

        while self.tokenizer.symbol()==",":
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()

            if(self.tokenizer.tokenType()!="IDENTIFIER"):
                print("Error: Expected variable name")
                return
            else:
                self.write(self.tokenizer.get_xml())
                self.tokenizer.advance()

        if(self.tokenizer.symbol()!=";"):
            print("Error: Expected symbol ;")
            return
        else:
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()

        self.indentation -= 1
        self.write("</varDec>")

    