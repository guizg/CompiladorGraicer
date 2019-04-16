class Node:
    def Evaluate(self,  table):
        pass
    
class BinOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self,  table):

        x=self.children[0].Evaluate(table)
        y=self.children[1].Evaluate(table)

        if x[1] != y[1]:
            raise Exception("Trying to BinOp diferent types.")


        if x[1] == "INTEGER":
            if self.value == '+':
                return [x[0] + y[0], "INTEGER"]
            if self.value == '-':
                return [x[0] - y[0], "INTEGER"]
            if self.value == '*':
                return [x[0] * y[0], "INTEGER"]
            if self.value == '/':
                return [x[0] // y[0], "INTEGER"]
            if self.value == '=':
                return [x[0] == y[0], "BOOLEAN"]
            if self.value == '>':
                return [x[0] > y[0], "BOOLEAN"]
            if self.value == '<':
                return [x[0] < y[0], "BOOLEAN"]
        
        if x[1] == "BOOLEAN":
            if self.value == 'and':
                return [x[0] and y[0], "BOOLEAN"]
            if self.value == 'or':
                return [x[0] or y[0], "BOOLEAN"]

        raise Exception(f"What the fuck are you trying to do mate? {x.value} {self.value} {y.value}??")



        
class UnOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self,  table):
        x=self.children[0].Evaluate(table)

        if x[1] == "INTEGER":
            if self.value == '+':
                return [+x[0], "INTEGER"]
            if self.value == '-':
                return [-x[0], "INTEGER"]
        if x[1] == "BOOLEAN":
            if self.value == 'not':
                return [not x[0], "BOOLEAN"]

        raise Exception(f"What the fuck are you trying to do mate?{self.value} {x.value}??")

class IntVal(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self,  table):
        return [self.value, "INTEGER"]

class Boolean(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self,  table):
        return [self.value, "BOOLEAN"]

class Type(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self,  table):
        return self.value

class VarDec(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self,  table):
        try:
            var = table.table[self.children[0].value]
        except:
            var = None 

        if var != None:
            raise Exception(f"Variable {self.children[0].value} already declared.")
        
        table.createSymbol(self.children[0].value, self.children[1].Evaluate(table))
        

class Program(Node):
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
        try:
            var = table.table[self.children[0].value]
        except:
            var = None 
            
        if var == None:
            raise Exception(f"Variable {self.children[0].value} not declared. Can't assign value. Porra.")

        new_val = self.children[1].Evaluate(table)

        if new_val[1] != var[1]:
            raise Exception(f"Types {new_val[1]} and {var[1]} do not match.")

        table.setSymbol(self.children[0].value, new_val[0])

class Print(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, table):
        print(self.children[0].Evaluate(table)[0])

class NoOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

class WhileNode(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, table):
        r = self.children[0].Evaluate(table)
        if r[1] != "BOOLEAN":
            raise Exception("Please use a fucking boolean at the WHILE condition. Thanks for your attention.")

        while self.children[0].Evaluate(table)[0]:
            self.children[1].Evaluate(table)
        
class IfNode(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, table):
        r = self.children[0].Evaluate(table)
        if r[1] != "BOOLEAN":
            raise Exception("Please use a fucking boolean at the IF condition. Thanks for your attention.")
            
        if self.children[0].Evaluate(table)[0]:
            self.children[1].Evaluate(table)
        else:
            if len(self.children) == 3:
                self.children[2].Evaluate(table)

class Input(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, table):
        return (int(input()), "INTEGER")