from Tokenizer import Tokenizer
from Token import Token
from PrePro import PrePro

class Parser:
    def parseExpression():
        result = Parser.parseTerm()

        while(Parser.tokens.actual.type == 'PLUS' or Parser.tokens.actual.type == 'MINUS'):
            if(Parser.tokens.actual.type == 'PLUS'):
                actual = Parser.tokens.selectNext()
                result += Parser.parseTerm()
            elif(Parser.tokens.actual.type == 'MINUS'):
                actual = Parser.tokens.selectNext()
                result -= Parser.parseTerm()
        
        return result

    def parseTerm():
        result = Parser.parseFactor()

        while(Parser.tokens.actual.type == 'DIV' or Parser.tokens.actual.type == 'MULT'):
            if(Parser.tokens.actual.type == 'MULT'):
                actual = Parser.tokens.selectNext()
                result *= Parser.parseTerm()
            elif(Parser.tokens.actual.type == 'DIV'):
                actual = Parser.tokens.selectNext()
                result //= Parser.parseTerm()
        
        return result

    def parseFactor():
        actual = Parser.tokens.actual
        result = 0

        if actual.type == 'INT':
            result = actual.value
            actual = Parser.tokens.selectNext()
            return result

        elif actual.type == 'PLUS':
            actual = Parser.tokens.selectNext()
            return +Parser.parseFactor()

        elif actual.type == 'MINUS':
            actual = Parser.tokens.selectNext()
            return -Parser.parseFactor()

        elif actual.type == 'OPEN_PAR':
            actual = Parser.tokens.selectNext()
            result = Parser.parseExpression()
            if Parser.tokens.actual.type == 'CLOSE_PAR':
                actual = Parser.tokens.selectNext()
                return result
            else:
                raise Exception("You did not fechate the parentesis! Column: "+str(Parser.tokens.position))

        else:
            raise Exception("Unexpected token. Column: "+str(Parser.tokens.position))    


    def run(code):
        Parser.tokens = Tokenizer(PrePro.filter(code))
        Parser.tokens.selectNext()
        res = Parser.parseExpression()
        if Parser.tokens.actual.type == "EOF":
            return res
        else:
            raise Exception("Can't put number after number. Column: "+str(Parser.tokens.position))

