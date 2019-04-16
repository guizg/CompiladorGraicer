class SymbolTable:
    def __init__(self):
        self.table = {}

    def getSymbol(self, symbol):
        symbol = symbol.upper()
        try:
            value = self.table[symbol]
        except:
            value = None
            
        if value == None:
            raise Exception("Symbol '{0}' not declared.".format(symbol))

        if value[0] == None:
            raise Exception("Symbol '{0}' not initialized.".format(symbol))

        return value
        

    def setSymbol(self, symbol, value):
        symbol = symbol.upper()
        self.table[symbol][0] = value

    def createSymbol(self, symbol, typi):
        symbol = symbol.upper()
        self.table[symbol] = [None, typi]