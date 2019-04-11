class Node:
    def Evaluate(self,  table):
        pass
    
class BinOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self,  table):
        if self.value == '+':
            return self.children[0].Evaluate(table) + self.children[1].Evaluate(table)
        if self.value == '-':
            return self.children[0].Evaluate(table) - self.children[1].Evaluate(table)
        if self.value == '*':
            return self.children[0].Evaluate(table) * self.children[1].Evaluate(table)
        if self.value == '/':
            return self.children[0].Evaluate(table) // self.children[1].Evaluate(table)
        if self.value == '=':
            return self.children[0].Evaluate(table) == self.children[1].Evaluate(table)
        if self.value == '>':
            return self.children[0].Evaluate(table) > self.children[1].Evaluate(table)
        if self.value == '<':
            return self.children[0].Evaluate(table) < self.children[1].Evaluate(table)


        
class UnOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self,  table):
        if self.value == '+':
            return +self.children[0].Evaluate(table)
        if self.value == '-':
            return -self.children[0].Evaluate(table)

class IntVal(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self,  table):
        return self.value

class Statements(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, table):
        for c in self.children:
            c.Evaluate(table)

class Id(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, table):
        return table.getSymbol(self.value)
    
class Assignment(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, table):
        table.setSymbol(self.children[0].value, self.children[1].Evaluate(table))

class Print(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, table):
        print(self.children[0].Evaluate(table))

class NoOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

class WhileNode(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, table):
        while self.children[0].Evaluate(table):
            self.children[1].Evaluate(table)
        
class IfNode(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, table):
        if self.children[0].Evaluate(table):
            self.children[1].Evaluate(table)
        else:
            if len(self.children) == 3:
                self.children[2].Evaluate(table)

class Input(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, table):
        return int(input())