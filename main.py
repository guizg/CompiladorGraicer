from Parser import Parser
from SymbolTable import SymbolTable

# code = input()

with open("input.vbs", "r") as f: ## Guilherme, para debug use o input da pasta logicomp!!!!       
    code = f.read()
    # print(code)
    tree = Parser.run(code)
    ST = SymbolTable()
    tree.Evaluate(ST)


