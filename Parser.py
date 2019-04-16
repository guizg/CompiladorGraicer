from Tokenizer import Tokenizer
from Token import Token
from PrePro import PrePro
from Node import *

class Parser:
    def parseProgram():
        
        if Parser.tokens.actual.type != 'SUB':
            raise Exception("Cade o SUB amigao? Line: {0}".format(str(Parser.line)))
        Parser.tokens.selectNext()

        if Parser.tokens.actual.type != 'MAIN':
            raise Exception("Cade o MAIN amigao? Line: {0}".format(str(Parser.line)))
        Parser.tokens.selectNext()

        if Parser.tokens.actual.type != 'OPEN_PAR':
            raise Exception("Cade o '(' amigao? Line: {0}".format(str(Parser.line)))
        Parser.tokens.selectNext()

        if Parser.tokens.actual.type != 'CLOSE_PAR':
            raise Exception("Cade o ')' amigao? Line: {0}".format(str(Parser.line)))
        Parser.tokens.selectNext()

        if Parser.tokens.actual.type != 'BREAK':
            raise Exception("Faltou quebrar a linha. Line: "+str(Parser.line))
        Parser.line += 1
        Parser.tokens.selectNext()

        children = []

        while Parser.tokens.actual.type != 'END':
            children.append(Parser.parseStatement())
            Parser.line +=1
            Parser.tokens.selectNext()

        if Parser.tokens.actual.type != 'END':
            raise Exception("Cade o END amigao? Line: "+str(Parser.line))
        Parser.tokens.selectNext()

        if Parser.tokens.actual.type != 'SUB':
            raise Exception("Cade o SUB amigao? Line: {0}".format(str(Parser.line)))
        Parser.tokens.selectNext()
        
        return Program("program", children)

    def parseStatement():

        if Parser.tokens.actual.type == 'ID':
           child0 = Id(Parser.tokens.actual.value, [])
           Parser.tokens.selectNext()
           if Parser.tokens.actual.value != '=':
               raise Exception("Excpected a '=' here. Line: {0}".format(str(Parser.line)))
           Parser.tokens.selectNext()
           return Assignment("=", [child0, Parser.parseRelExpression()])
        
        if Parser.tokens.actual.type == 'PRINT':
            Parser.tokens.selectNext()
            return Print("print", [Parser.parseExpression()])

        if Parser.tokens.actual.type == 'WHILE':
            Parser.tokens.selectNext()
            child0 = Parser.parseRelExpression()

            if Parser.tokens.actual.type != 'BREAK':
                raise Exception("Faltou quebrar a linha. Line: "+str(Parser.line))
            Parser.line += 1
            Parser.tokens.selectNext()

            staments = []

            while Parser.tokens.actual.type != 'WEND':
                staments.append(Parser.parseStatement())
                Parser.line +=1
                Parser.tokens.selectNext()

            if Parser.tokens.actual.type != 'WEND':
                raise Exception("Cade o WEND amigao? Line: "+str(Parser.line))
            Parser.tokens.selectNext()


            return WhileNode("while", [child0, Program("program_while", staments)])

        if Parser.tokens.actual.type == 'IF':
            Parser.tokens.selectNext()
            children = [Parser.parseRelExpression()]
            
            if Parser.tokens.actual.type != 'THEN':
                raise Exception("Cade o THEN amigao? Line: "+str(Parser.line))
            Parser.tokens.selectNext()

            if Parser.tokens.actual.type != 'BREAK':
                raise Exception("Faltou quebrar a linha. Line: "+str(Parser.line))
            Parser.line += 1
            Parser.tokens.selectNext()

            staments = []

            while Parser.tokens.actual.type != 'END' and Parser.tokens.actual.type != 'ELSE':
                staments.append(Parser.parseStatement())
                Parser.line +=1
                Parser.tokens.selectNext()
            
            children.append(Program("program_if", staments))

            if Parser.tokens.actual.type == "ELSE":
                Parser.tokens.selectNext()

                if Parser.tokens.actual.type != 'BREAK':
                    raise Exception("Faltou quebrar a linha. Line: "+str(Parser.line))
                Parser.line += 1
                Parser.tokens.selectNext()
                
                staments_else = []

                while Parser.tokens.actual.type != 'END':
                    staments_else.append(Parser.parseStatement())
                    Parser.line +=1
                    Parser.tokens.selectNext()
            
                children.append(Program("program_else", staments_else))
            
            if Parser.tokens.actual.type != 'END':
                raise Exception("Cade o END amigao? Line: "+str(Parser.line))
            Parser.tokens.selectNext()

            if Parser.tokens.actual.type != 'IF':
                raise Exception("Cade o IF amigao? Line: "+str(Parser.line))
            Parser.tokens.selectNext()

            return IfNode("if", children)

        if Parser.tokens.actual.type == 'DIM':
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type != 'ID':
                raise Exception("Tava esperando um ID aqui. Line: "+str(Parser.line))
            id = Id(Parser.tokens.actual.value, [])
            Parser.tokens.selectNext()
            
            if Parser.tokens.actual.type != 'AS':
                raise Exception("Cade o AS amigao? Line: "+str(Parser.line))
            Parser.tokens.selectNext()

            return VarDec("vardec", [id, Parser.parseType()])
        
        return NoOp('', [])

    def parseType():
        if Parser.tokens.actual.type == "INTEGER":
            return Type('INTEGER', [])
        if Parser.tokens.actual.type == "BOOLEAN":
            return Type('BOOLEAN', [])
        raise Exception(f"Type {Parser.tokens.actual.type} not reconhecated. Line: {Parser.line}")
        
            
    def parseRelExpression():
        exp = Parser.parseExpression()

        if Parser.tokens.actual.type == 'EQUAL':
            Parser.tokens.selectNext()
            return BinOp("=", [exp, Parser.parseExpression()])
        
        if Parser.tokens.actual.type == 'BIGGER':
            Parser.tokens.selectNext()
            return BinOp(">", [exp, Parser.parseExpression()])
        
        if Parser.tokens.actual.type == 'SMALLER':
            Parser.tokens.selectNext()
            return BinOp("<", [exp, Parser.parseExpression()])
        
        return exp

        

    def parseExpression():
        result = Parser.parseTerm()

        while(Parser.tokens.actual.type == 'PLUS' or Parser.tokens.actual.type == 'MINUS' or Parser.tokens.actual.type == 'OR'):
            if(Parser.tokens.actual.type == 'PLUS'):
                actual = Parser.tokens.selectNext()
                child1 = Parser.parseTerm()
                result = BinOp("+", [result, child1])
            elif(Parser.tokens.actual.type == 'MINUS'):
                actual = Parser.tokens.selectNext()
                child1 = Parser.parseTerm()
                result = BinOp("-", [result, child1])
            elif(Parser.tokens.actual.type == 'OR'):
                actual = Parser.tokens.selectNext()
                child1 = Parser.parseTerm()
                result = BinOp("or", [result, child1])
        
        return result

    def parseTerm():
        result = Parser.parseFactor()

        while(Parser.tokens.actual.type == 'DIV' or Parser.tokens.actual.type == 'MULT' or Parser.tokens.actual.type == 'AND'):
            if(Parser.tokens.actual.type == 'MULT'):
                actual = Parser.tokens.selectNext()
                child1 = Parser.parseFactor()
                result = BinOp("*", [result, child1])
                
            elif(Parser.tokens.actual.type == 'DIV'):
                actual = Parser.tokens.selectNext()
                child1 = Parser.parseFactor()
                result = BinOp("/", [result, child1])
            
            elif(Parser.tokens.actual.type == 'AND'):
                actual = Parser.tokens.selectNext()
                child1 = Parser.parseFactor()
                result = BinOp("and", [result, child1])

        return result

    def parseFactor():
        actual = Parser.tokens.actual
        result = 0

        if actual.type == 'INT':
            result = IntVal(actual.value, [])
            actual = Parser.tokens.selectNext()
            return result

        if actual.type == 'ID':
            result = Id(actual.value, [])
            actual = Parser.tokens.selectNext()
            return result

        if actual.type == 'PLUS':
            actual = Parser.tokens.selectNext()
            child = Parser.parseFactor()
            return UnOp("+", [child])

        if actual.type == 'MINUS':
            actual = Parser.tokens.selectNext()
            child = Parser.parseFactor()
            return UnOp("-", [child])

        if actual.type == 'NOT':
            actual = Parser.tokens.selectNext()
            child = Parser.parseFactor()
            return UnOp("not", [child])
        
        if actual.type == 'INPUT':
            res = Input(actual.value, [])
            actual = Parser.tokens.selectNext()
            return res

        if actual.type == 'TRUE' or actual.type == 'FALSE':
            res = Boolean(actual.value, [])
            actual = Parser.tokens.selectNext()
            return res
        
            

        if actual.type == 'OPEN_PAR':
            actual = Parser.tokens.selectNext()
            result = Parser.parseRelExpression()
            if Parser.tokens.actual.type == 'CLOSE_PAR':
                actual = Parser.tokens.selectNext()
                return result
            else:
                raise Exception("You did not fechate the parentesis! Line: {0}".format(str(Parser.line)))   

        
        raise Exception("Unexpected token '{0}'. Line: {1}".format(Parser.tokens.actual, str(Parser.line)))    


    def run(code):
        Parser.tokens = Tokenizer(PrePro.filter(code))
        Parser.line = 0
        Parser.tokens.selectNext()

        # while Parser.tokens.actual.type != "EOF":
        #     print(Parser.tokens.actual)
        #     Parser.tokens.selectNext()
        # return

        while Parser.tokens.actual.type == "BREAK":
            Parser.tokens.selectNext()

        res = Parser.parseProgram()

        while Parser.tokens.actual.type == "BREAK":
            Parser.tokens.selectNext()

        if Parser.tokens.actual.type == "EOF":
            return res
        else:
            raise Exception("Unexpected token '{0}'. Line: {1}".format(Parser.tokens.actual.type, str(Parser.line)))   