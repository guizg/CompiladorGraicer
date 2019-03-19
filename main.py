from Parser import Parser

# code = input()

f = open("input.vbs", "r")
code = f.read()
# print(code)
tree = Parser.run(code)
print(tree.Evaluate())

