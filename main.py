from Parser import Parser
from SymbolTable import SymbolTable
from PrePro import PrePro
import sys



with open(sys.argv[1], "r") as f:       
    code = f.read()
    # print(PrePro.filter(code))
    tree = Parser.run(code)
    ST = SymbolTable()
    tree.Evaluate(ST)