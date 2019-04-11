class SymbolTable:
    def __init__(self):
        self.table = {}
    def getSymbol(self, symbol):
        symbol = symbol.upper()
        value = self.table[symbol]
        if value != None:
            return value
        raise Exception("Symbol '{0}' not declared.".format(symbol))

    def setSymbol(self, symbol, value):
        symbol = symbol.upper()
        self.table[symbol] = value