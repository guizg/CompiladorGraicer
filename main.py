from Parser import Parser
from SymbolTable import SymbolTable
from PrePro import PrePro
import sys
from CodeWriter import CodeWriter


with open(sys.argv[1], "r") as f:       
    code = f.read()
    tree = Parser.run(code)
    ST = SymbolTable()
    tree.Evaluate(ST)
    CodeWriter.code += """\nPOP EBP\nMOV EAX, 1\nINT 0x80"""
    print(CodeWriter.code)
    with open("out.asm", "w+") as o:
        o.write(CodeWriter.code)
    