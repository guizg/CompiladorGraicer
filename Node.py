from CodeWriter import CodeWriter

class Node:
    i = 0
    def Evaluate(self,  table):
        pass

    @staticmethod
    def newId():
        Node.i += 1
        return Node.i
    
class BinOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newId()

    def Evaluate(self,  table):

        x=self.children[0].Evaluate(table)

        CodeWriter.write("PUSH EBX")

        y=self.children[1].Evaluate(table)

        CodeWriter.write("POP EAX")

        if x[1] != y[1]:
            raise Exception("Trying to BinOp diferent types.")


        if x[1] == "INTEGER":
            if self.value == '+':
                CodeWriter.write("ADD EAX, EBX")
                CodeWriter.write("MOV EBX, EAX")
                return [x[0] + y[0], "INTEGER"]
            if self.value == '-':
                CodeWriter.write("SUB EAX, EBX")
                CodeWriter.write("MOV EBX, EAX")
                return [x[0] - y[0], "INTEGER"]
            if self.value == '*':
                CodeWriter.write("IMUL EBX")
                CodeWriter.write("MOV EBX, EAX")
                return [x[0] * y[0], "INTEGER"]
            if self.value == '/':
                CodeWriter.write("IDIV EBX")
                CodeWriter.write("MOV EBX, EAX")
                return [x[0] // y[0], "INTEGER"]
            if self.value == '=':
                CodeWriter.write("CMP EAX, EBX")
                CodeWriter.write("CALL binop_je")
                return [x[0] == y[0], "BOOLEAN"]
            if self.value == '>':
                CodeWriter.write("CMP EAX, EBX")
                CodeWriter.write("CALL binop_jg")
                return [x[0] > y[0], "BOOLEAN"]
            if self.value == '<':
                CodeWriter.write("CMP EAX, EBX")
                CodeWriter.write("CALL binop_jl")
                return [x[0] < y[0], "BOOLEAN"]
        
        if x[1] == "BOOLEAN":
            if self.value == 'and':
                CodeWriter.write("AND EAX, EBX")
                CodeWriter.write("MOV EBX, EAX")
                return [x[0] and y[0], "BOOLEAN"]
            if self.value == 'or':
                CodeWriter.write("OR EAX, EBX")
                CodeWriter.write("MOV EBX, EAX")
                return [x[0] or y[0], "BOOLEAN"]
            if self.value == '=':
                CodeWriter.write("CMP EAX, EBX")
                CodeWriter.write("CALL binop_je")
                return [x[0] == y[0], "BOOLEAN"]

        raise Exception(f"What the fuck are you trying to do mate? {x.value} {self.value} {y.value}??")



        
class UnOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newId()

    def Evaluate(self,  table):
        x=self.children[0].Evaluate(table)

        if x[1] == "INTEGER":
            if self.value == '+':
                CodeWriter.write("; aqui jaz um operdor unario inutil")
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
        self.id = Node.newId()

    def Evaluate(self,  table):
        CodeWriter.write(f"MOV EBX, {str(self.value)}")
        return [self.value, "INTEGER"]

class Boolean(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newId()

    def Evaluate(self,  table):
        boolval = 1 if self.value==True else  0
        CodeWriter.write(f"MOV EBX, {str(boolval)}")
        return [self.value, "BOOLEAN"]

class Type(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newId()

    def Evaluate(self,  table):
        return self.value

class VarDec(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newId()

    def Evaluate(self,  table):
        try:
            var = table.table[self.children[0].value]
        except:
            var = None 

        if var != None:
            raise Exception(f"Variable {self.children[0].value} already declared.")
        
        table.createSymbol(self.children[0].value, self.children[1].Evaluate(table))
        CodeWriter.write("PUSH DWORD 0")

        

class Program(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newId()

    def Evaluate(self, table):
        for c in self.children:
            c.Evaluate(table)

class Id(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newId()

    def Evaluate(self, table):
        CodeWriter.write(f"MOV EBX, [EBP{str(table.table[self.value][2])}]")
        return table.getSymbol(self.value)
    
class Assignment(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newId()

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

        CodeWriter.write(f"MOV [EBP{str(table.table[self.children[0].value][2])}], EBX")

class Print(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newId()

    def Evaluate(self, table):
        # print(self.children[0].Evaluate(table)[0])
        self.children[0].Evaluate(table)
        CodeWriter.write("PUSH EBX")
        CodeWriter.write("CALL print")
        CodeWriter.write("POP EBX")

class NoOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newId()

class WhileNode(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newId()

    def Evaluate(self, table):
        CodeWriter.write("LOOP_"+str(self.id)+":")
        r = self.children[0].Evaluate(table)
        CodeWriter.write("CMP EBX, False")
        CodeWriter.write("JE EXIT_"+str(self.id))
        if r[1] != "BOOLEAN":
            raise Exception("Please use a fucking boolean at the WHILE condition. Thanks for your attention.")

        # while self.children[0].Evaluate(table)[0]:
        self.children[1].Evaluate(table)

        CodeWriter.write("JMP "+"LOOP_"+str(self.id))
        CodeWriter.write("EXIT_"+str(self.id)+":")
        
class IfNode(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newId()

    def Evaluate(self, table):
        r = self.children[0].Evaluate(table)
        if r[1] != "BOOLEAN":
            raise Exception("Please use a fucking boolean at the IF condition. Thanks for your attention.")
        CodeWriter.write("CMP EBX, False")
        CodeWriter.write("JE ELSE_"+str(self.id))
        # if self.children[0].Evaluate(table)[0]:
        self.children[1].Evaluate(table)
        # else:
        CodeWriter.write("ELSE_"+str(self.id)+":")
        if len(self.children) == 3:
            self.children[2].Evaluate(table)

class Input(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newId()

    def Evaluate(self, table):
        return (int(input()), "INTEGER")