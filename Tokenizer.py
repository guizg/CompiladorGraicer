from Token import Token

class Tokenizer:
    def __init__(self, origin):
        self.origin = origin
        self.position = 0
        self.actual = None

    def selectNext(self):
        if self.position == len(self.origin):
            self.actual = Token('EOF', '')
            # print(self.actual)
            return self.actual

        while self.origin[self.position] == ' ':
            self.position += 1


        pseudotoken = self.origin[self.position]
        
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
            self.actual = Token('MULTIPLIED BY', '*')
            self.position += 1
            # print(self.actual)
            return self.actual
        
        if pseudotoken == '/':
            self.actual = Token('DIVIDED BY', '/')
            self.position += 1
            # print(self.actual)
            return self.actual
        
        self.position += 1
        while(self.position<len(self.origin) and self.origin[self.position].isdigit()):
            pseudotoken += self.origin[self.position]
            self.position += 1
        
        self.actual = Token('INT', int(pseudotoken))
        # print(self.actual)
        return self.actual
        

# toks = Tokenizer("11+12   -   4+    100")

# for i in range(9):
#     toks.selectNext()