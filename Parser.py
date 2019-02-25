from Tokenizer import Tokenizer
from Token import Token

class Parser:
    def parseExpression():
        result = 0
        actual = Parser.tokens.selectNext()

        if actual.type == 'INT':
            result += actual.value
            actual = Parser.tokens.selectNext()
            while(actual.type == 'PLUS' or actual.type == 'MINUS' or actual.type == 'MULTIPLIED BY' or actual.type == 'DIVIDED BY'):
                if(actual.type == 'PLUS'):
                    actual = Parser.tokens.selectNext()
                    if actual.type == 'INT':
                        result += actual.value
                    else:
                        raise Exception("Can't use a symbol after a symbol (or end with symbol). Column: "+str(Parser.tokens.position)) 
                elif(actual.type == 'MINUS'):
                    actual = Parser.tokens.selectNext()
                    if actual.type == 'INT':
                        result -= actual.value
                    else:
                        raise Exception("Can't use a symbol after a symbol (or end with symbol). Column: "+str(Parser.tokens.position))
                elif(actual.type == 'MULTIPLIED BY'):
                    actual = Parser.tokens.selectNext()
                    if actual.type == 'INT':
                        result *= actual.value
                    else:
                        raise Exception("Can't use a symbol after a symbol (or end with symbol). Column: "+str(Parser.tokens.position))
                elif(actual.type == 'DIVIDED BY'):
                    actual = Parser.tokens.selectNext()
                    if actual.type == 'INT':
                        result /= actual.value
                    else:
                        raise Exception("Can't use a symbol after a symbol (or end with symbol). Column: "+str(Parser.tokens.position))
                actual = Parser.tokens.selectNext()
        else:
            raise Exception("Can't start with a symbol. Column: "+str(Parser.tokens.position))
        
        return result

    def run(code):
        Parser.tokens = Tokenizer(code)
        print(Parser.parseExpression())

