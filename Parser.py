from Tokenizer import Tokenizer
from Token import Token
from PrePro import PrePro
from Node import *

class Parser:
    def parseStatements():
        Parser.line = 0

        if Parser.tokens.actual.type != 'BEGIN':
            raise Exception("Expecting a BEGIN.")
        Parser.tokens.selectNext()

        if Parser.tokens.actual.type != 'BREAK':
            raise Exception("You didnt quebrate the line. Line: {0}".format(str(Parser.line)))
        Parser.tokens.selectNext()

        Parser.line +=1
        
        children = []
        while Parser.tokens.actual.type != 'END':
            children.append(Parser.parseStatement())
            if Parser.tokens.actual.type != 'BREAK':
                print(Parser.tokens.actual.type)
                raise Exception("You didnt quebrate the line. Line: {0}".format(str(Parser.line)))
            Parser.line +=1
            Parser.tokens.selectNext()
        Parser.tokens.selectNext()

        # if Parser.tokens.actual.type != 'BREAK':
        #     raise Exception("You didnt quebrate the line. Line: {0}".format(str(Parser.line)))
        # Parser.tokens.selectNext()
        
        return Statements("statements", children)

    def parseStatement():
        res = NoOp('', [])

        if Parser.tokens.actual.type == 'ID':
           child0 = Id(Parser.tokens.actual.value, [])
           Parser.tokens.selectNext()
           if Parser.tokens.actual.value != '=':
               raise Exception("Excpected a '=' here. Line: {0}".format(str(Parser.line)))
           Parser.tokens.selectNext()
           res = Assignment("=", [child0, Parser.parseExpression()])
        
        elif Parser.tokens.actual.type == 'PRINT':
            Parser.tokens.selectNext()
            res = Print("print", [Parser.parseExpression()])

        elif Parser.tokens.actual.type == 'BEGIN':
            res = Parser.parseStatements()
        
        return res
        
            



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

        elif actual.type == 'PLUS':
            actual = Parser.tokens.selectNext()
            child = Parser.parseFactor()
            return UnOp("+", [child])

        elif actual.type == 'MINUS':
            actual = Parser.tokens.selectNext()
            child = Parser.parseFactor()
            return UnOp("-", [child])

        elif actual.type == 'OPEN_PAR':
            actual = Parser.tokens.selectNext()
            result = Parser.parseExpression()
            if Parser.tokens.actual.type == 'CLOSE_PAR':
                actual = Parser.tokens.selectNext()
                return result
            else:
                raise Exception("You did not fechate the parentesis! Line: {0}".format(str(Parser.line)))   

        else:
            raise Exception("Unexpected token. Line: {0}".format(str(Parser.line)))    


    def run(code):
        Parser.tokens = Tokenizer(PrePro.filter(code))
        Parser.line = 0
        Parser.tokens.selectNext()
        res = Parser.parseStatements()
        if Parser.tokens.actual.type == "EOF":
            return res
        else:
            raise Exception("Unexpected token '{0}'. Line: {1}".format(Parser.tokens.actual.type, str(Parser.line)))   