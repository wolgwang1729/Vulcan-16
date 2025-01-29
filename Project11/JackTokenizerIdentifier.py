import os

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
        self.st=self.buildSymbolTable()
        # print(self.st.subroutineScope)
        # print(self.st.classScope)
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
    
    def buildSymbolTable(self):
        tokens=self.tokens
        st=SymbolTable()
        for i in range(len(tokens)):
            if(tokens[i]=="static" or tokens[i]=="field" or tokens[i]=="var"):
                st.define(tokens[i+2],tokens[i+1],tokens[i])
        return st

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
            if(self.st.subroutineScope.get(self.currentToken) or self.st.classScope.get(self.currentToken)):
                return f"identifier {self.st.kindOf(self.currentToken)} {self.st.indexOf(self.currentToken)}"
            else:
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
            self.currNum+=1
        else:
            self.currentToken = None 

class JackTokenizer:
    def __init__(self,directory):
        self.directory=directory
        self.createTXML()

    def createTXML(self):
        for file in os.listdir(self.directory):
            if file.endswith(".jack"):
                jt=JackTokenizerFile(self.directory+"\\"+file)
                with open(self.directory+"\\"+file[:-5]+"T.xml","w") as file:
                    file.write("<tokens>\n")
                    while(jt.hasMoreTokens()):
                        jt.advance()
                        if(jt.currentToken[0]=="\""):
                            file.write(f'<{jt.getTokenType()}> {jt.stringVal()} </{jt.getTokenType()}>\n')
                        elif(jt.currentToken==">"):
                            file.write(f'<{jt.getTokenType()}> &gt; </{jt.getTokenType()}>\n')
                        elif(jt.currentToken=="<"):
                            file.write(f'<{jt.getTokenType()}> &lt; </{jt.getTokenType()}>\n')
                        elif(jt.currentToken=="&"):
                            file.write(f'<{jt.getTokenType()}> &amp; </{jt.getTokenType()}>\n')
                        else:
                            file.write(f'<{jt.getTokenType()}> {jt.currentToken} </{jt.getTokenType()}>\n')
                    file.write("</tokens>")
                    file.write("\n")



JackTokenizer("Project11\TestFiles\Average")