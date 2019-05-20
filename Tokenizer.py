from Token import Token

class Tokenizer:
    def __init__(self, origin):
        self.origin = origin
        self.position = 0
        self.actual = None
        self.reserved = ["PRINT", "BEGIN", "END", "IF", "WHILE", "ELSE", "INPUT", \
                        "WEND", "THEN", "DIM", "AS", "INTEGER", "BOOLEAN", "SUB", "FUNCTION",\
                        "AND", "OR", "NOT", "TRUE", "FALSE", "CALL"]

    def selectNext(self):

        if self.position == len(self.origin):
            self.actual = Token('EOF', '')
            # print(self.actual)
            return self.actual

        while self.origin[self.position] == ' ':
            self.position += 1
            if self.position == len(self.origin):
                self.actual = Token('EOF', '')
                # print(self.actual)
                return self.actual


        pseudotoken = self.origin[self.position]

        if pseudotoken == ',':
            self.actual = Token('COMMA', ',')
            self.position += 1
            # print(self.actual)
            return self.actual
        
        if pseudotoken == '+':
            self.actual = Token('PLUS', '+')
            self.position += 1
            # print(self.actual)
            return self.actual

        if pseudotoken == '-':
            self.actual = Token('MINUS', '-')
            self.position += 1
            # print(self.actual)
            return self.actual

        if pseudotoken == '*':
            self.actual = Token('MULT', '*')
            self.position += 1
            # print(self.actual)
            return self.actual
        
        if pseudotoken == '/':
            self.actual = Token('DIV', '/')
            self.position += 1
            # print(self.actual)
            return self.actual

        if pseudotoken == '(':
            self.actual = Token('OPEN_PAR', '(')
            self.position += 1
            # print(self.actual)
            return self.actual

        if pseudotoken == ')':
            self.actual = Token('CLOSE_PAR', ')')
            self.position += 1
            # print(self.actual)
            return self.actual

        if pseudotoken == '=':
            self.actual = Token('EQUAL', '=')
            self.position += 1
            # print(self.actual)
            return self.actual

        if pseudotoken == '>':
            self.actual = Token('BIGGER', '>')
            self.position += 1
            # print(self.actual)
            return self.actual

        if pseudotoken == '<':
            self.actual = Token('SMALLER', '<')
            self.position += 1
            # print(self.actual)
            return self.actual

        if pseudotoken == '\n':
            self.actual = Token('BREAK', 'BREAK')
            self.position +=1
            # print(self.actual)
            return self.actual

        if pseudotoken.isdigit():
            self.position += 1
            while(self.position<len(self.origin) and self.origin[self.position].isdigit()):
                pseudotoken += self.origin[self.position]
                self.position += 1
            
            self.actual = Token('INT', int(pseudotoken))
            # print(self.actual)
            return self.actual

        if pseudotoken.isalpha():
            self.position += 1

            while(self.position<len(self.origin) and (self.origin[self.position].isalpha() or self.origin[self.position] == "_" or self.origin[self.position].isdigit())):
                pseudotoken += self.origin[self.position]
                self.position += 1
            
            pseudotoken = pseudotoken.upper()

            if pseudotoken in self.reserved:
                self.actual = Token(pseudotoken, pseudotoken)
            else:
                self.actual = Token('ID', pseudotoken)
            #print(self.actual)
            return self.actual


        raise Exception("Token '{0}' not known.".format(pseudotoken))
