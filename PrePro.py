
class PrePro:
    def filter(code):
        new = ""
        comment = False
        for c in code:
            if c == "\n":
                comment = False
            
            if comment == True:
                continue
                
            if c == "'":
                comment = True
                continue
            new += c

        return new
