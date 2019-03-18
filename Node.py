class Node:
    def Evaluate(self):
        pass
    
class BinOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self):
        if self.value == '+':
            return self.children[0].Evaluate() + self.children[1].Evaluate()
        if self.value == '-':
            return self.children[0].Evaluate() - self.children[1].Evaluate()
        if self.value == '*':
            return self.children[0].Evaluate() * self.children[1].Evaluate()
        if self.value == '/':
            return self.children[0].Evaluate() // self.children[1].Evaluate()


        
class UnOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self):
        if self.value == '+':
            return +self.children[0].Evaluate()
        if self.value == '-':
            return -self.children[0].Evaluate()

class IntVal(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self):
        return self.value

class NoOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
