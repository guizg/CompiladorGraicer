


class PrePro:
    def filter(code):
        new = ""
        for c in code:
            if c == "'":
                break
            new += c

        return new
