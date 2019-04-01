from Parser import Parser
from SymbolTable import SymbolTable
from PrePro import PrePro
import sys



with open(sys.argv[1], "r") as f: ## Guilherme, para debug use o input da pasta logicomp!!!!       
    code = f.read()
    # print(PrePro.filter(code))
    tree = Parser.run(code)
    ST = SymbolTable()
    tree.Evaluate(ST)