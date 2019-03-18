from Parser import Parser

code = input()
tree = Parser.run(code)
print(tree.Evaluate())

