class CompilationEngine:
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

        if(self.tokenizer.keyWord() in ["int", "char", "boolean"] or self.tokenizer.tokenType()=="IDENTIFIER"):
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

    #Statements
    def compileStatements(self):
        self.write("<statements>")
        self.indentation += 1

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

        self.indentation -= 1
        self.write("</statements>")

    def compileLet(self):
        self.write("<letStatement>")
        self.indentation += 1

        if(self.tokenizer.keyWord()!="let"):
            print("Error: Expected keyword let")
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

        if(self.tokenizer.symbol()!="="):
            print("Error: Expected symbol =")
            return
        else:
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()

        self.compileExpression()

        if(self.tokenizer.symbol()!=";"):
            print("Error: Expected symbol ;")
            return
        else:
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()

        self.indentation -= 1
        self.write("</letStatement>")

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
        self.write("<doStatement>")
        self.indentation += 1

        if(self.tokenizer.keyWord()!="do"):
            print("Error: Expected keyword do")
            return
        else:
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()

        self.compileSubroutineCall()

        if(self.tokenizer.symbol()!=";"):
            print("Error: Expected symbol ;")
            return
        else:
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()

        self.indentation -= 1
        self.write("</doStatement>")

    def compileReturn(self):
        self.write("<returnStatement>")
        self.indentation += 1

        if(self.tokenizer.keyWord()!="return"):
            print("Error: Expected keyword return")
            return
        else:
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()

        if(self.tokenizer.symbol()!=";"):
            self.compileExpression()

        if(self.tokenizer.symbol()!=";"):
            print("Error: Expected symbol ;")
            return
        else:
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()

        self.indentation -= 1
        self.write("</returnStatement>")

    #Expressions
    def compileExpression(self):
        self.write("<expression>")
        self.indentation += 1

        self.compileTerm()
        while self.tokenizer.symbol() in ["+", "-", "*", "/", "&amp;", "|", "&lt;", "&gt;", "="]:
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()
            self.compileTerm()

        self.indentation -= 1
        self.write("</expression>")

    def compileTerm(self):
        self.write("<term>")
        self.indentation += 1

        if(self.tokenizer.tokenType()=="INT_CONST"):
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()
        elif(self.tokenizer.tokenType()=="STRING_CONST"):
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()
        elif(self.tokenizer.keyWord() in ["true", "false", "null", "this"]):
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()
        elif(self.tokenizer.tokenType()=="IDENTIFIER"):
            self.write(self.tokenizer.get_xml())
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
                self.compileSubroutineCall()
        elif(self.tokenizer.symbol()=="("):
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()
            self.compileExpression()

            if(self.tokenizer.symbol()!=")"):
                print("Error: Expected symbol )")
                return
            else:
                self.write(self.tokenizer.get_xml())
                self.tokenizer.advance()
        elif(self.tokenizer.symbol() in ["-", "~"]):
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()
            self.compileTerm()

        self.indentation -= 1
        self.write("</term>")

    def compileSubroutineCall(self):
        if(self.tokenizer.symbol()=="."):
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()

            if(self.tokenizer.tokenType()!="IDENTIFIER"):
                print("Error: Expected subroutine name")
                return
            else:
                self.write(self.tokenizer.get_xml())
                self.tokenizer.advance()
        elif(self.tokenizer.tokenType()=="IDENTIFIER"):
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()
            if(self.tokenizer.symbol()=="."):
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

        self.compileExpressionList()

        if(self.tokenizer.symbol()!=")"):
            print("Error: Expected symbol )")
            return
        else:
            self.write(self.tokenizer.get_xml())
            self.tokenizer.advance()

    def compileExpressionList(self):
        self.write("<expressionList>")
        self.indentation += 1

        if(self.tokenizer.symbol()!=")"):
            self.compileExpression()

            while self.tokenizer.symbol()==",":
                self.write(self.tokenizer.get_xml())
                self.tokenizer.advance()
                self.compileExpression()

        self.indentation -= 1
        self.write("</expressionList>")
