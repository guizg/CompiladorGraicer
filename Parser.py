from Tokenizer import Tokenizer
from Token import Token
from PrePro import PrePro
from Node import *

class Parser:
    def parseStatements():
        
        
        children = []

        while Parser.tokens.actual.type != 'EOF' and Parser.tokens.actual.type != 'WEND' and Parser.tokens.actual.type != 'END' and Parser.tokens.actual.type != 'ELSE':
            children.append(Parser.parseStatement())
            Parser.line +=1
            Parser.tokens.selectNext()

        return Statements("statements", children)

    def parseStatement():

        if Parser.tokens.actual.type == 'ID':
           child0 = Id(Parser.tokens.actual.value, [])
           Parser.tokens.selectNext()
           if Parser.tokens.actual.value != '=':
               raise Exception("Excpected a '=' here. Line: {0}".format(str(Parser.line)))
           Parser.tokens.selectNext()
           return Assignment("=", [child0, Parser.parseExpression()])
        
        if Parser.tokens.actual.type == 'PRINT':
            Parser.tokens.selectNext()
            return Print("print", [Parser.parseExpression()])

        if Parser.tokens.actual.type == 'WHILE':
            Parser.tokens.selectNext()
            child0 = Parser.parseRelExpression()

            if Parser.tokens.actual.type != 'THEN':
                raise Exception("Cade o THEN amigao? Line: "+str(Parser.line))
            Parser.tokens.selectNext()

            if Parser.tokens.actual.type != 'BREAK':
                raise Exception("Faltou quebrar a linha. Line: "+str(Parser.line))
            Parser.line += 1
            Parser.tokens.selectNext()

            res = WhileNode("while", [child0, Parser.parseStatements()])
            if Parser.tokens.actual.type != 'WEND':
                raise Exception("Cade o WEND amigao? Line: "+str(Parser.line))
            Parser.tokens.selectNext()

            # if Parser.tokens.actual.type != 'BREAK':
            #     raise Exception("Faltou quebrar a linha. Line: "+str(Parser.line))
            # Parser.line += 1
            # Parser.tokens.selectNext()

            return res

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

            children.append(Parser.parseStatements())

            if Parser.tokens.actual.type == "ELSE":
                Parser.tokens.selectNext()

                if Parser.tokens.actual.type != 'BREAK':
                    raise Exception("Faltou quebrar a linha. Line: "+str(Parser.line))
                Parser.line += 1
                Parser.tokens.selectNext()

                children.append(Parser.parseStatements())
            
            if Parser.tokens.actual.type != 'END':
                raise Exception("Cade o END amigao? Line: "+str(Parser.line))
            Parser.tokens.selectNext()

            if Parser.tokens.actual.type != 'IF':
                raise Exception("Cade o IF amigao? Line: "+str(Parser.line))
            Parser.tokens.selectNext()

            # if Parser.tokens.actual.type != 'BREAK':
            #     raise Exception("Faltou quebrar a linha. Line: "+str(Parser.line))
            # Parser.line += 1
            # Parser.tokens.selectNext()

            return IfNode("if", children)

        
        
        return NoOp('', [])
        
            
    def parseRelExpression():
        child0 = Parser.parseExpression()

        if Parser.tokens.actual.type == 'EQUAL':
            Parser.tokens.selectNext()
            return BinOp("=", [child0, Parser.parseExpression()])
        
        if Parser.tokens.actual.type == 'BIGGER':
            Parser.tokens.selectNext()
            return BinOp(">", [child0, Parser.parseExpression()])
        
        if Parser.tokens.actual.type == 'SMALLER':
            Parser.tokens.selectNext()
            return BinOp("<", [child0, Parser.parseExpression()])
        
        raise Exception("Unexpected token (not =, > or <)")

        

    def parseExpression():
        result = Parser.parseTerm()

        while(Parser.tokens.actual.type == 'PLUS' or Parser.tokens.actual.type == 'MINUS'):
            if(Parser.tokens.actual.type == 'PLUS'):
                actual = Parser.tokens.selectNext()
                child1 = Parser.parseTerm()
                result = BinOp("+", [result, child1])
            elif(Parser.tokens.actual.type == 'MINUS'):
                actual = Parser.tokens.selectNext()
                child1 = Parser.parseTerm()
                result = BinOp("-", [result, child1])
        
        return result

    def parseTerm():
        result = Parser.parseFactor()

        while(Parser.tokens.actual.type == 'DIV' or Parser.tokens.actual.type == 'MULT'):
            if(Parser.tokens.actual.type == 'MULT'):
                actual = Parser.tokens.selectNext()
                child1 = Parser.parseFactor()
                result = BinOp("*", [result, child1])
                
            elif(Parser.tokens.actual.type == 'DIV'):
                actual = Parser.tokens.selectNext()
                child1 = Parser.parseFactor()
                result = BinOp("/", [result, child1])

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
        
        if actual.type == 'INPUT':
            res = Input(actual.value, [])
            actual = Parser.tokens.selectNext()
            return res
            

        if actual.type == 'OPEN_PAR':
            actual = Parser.tokens.selectNext()
            result = Parser.parseExpression()
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
        res = Parser.parseStatements()

            
        if Parser.tokens.actual.type == "EOF":
            return res
        else:
            raise Exception("Unexpected token '{0}'. Line: {1}".format(Parser.tokens.actual.type, str(Parser.line)))   