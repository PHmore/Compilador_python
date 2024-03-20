class TOKEN:
    def __init__(self, type, value):
        palavras_reservadas = [
            'and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else',
            'except', 'False', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is',
            'lambda', 'None', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'True',
            'try', 'while', 'with', 'yield', 'print',
            '+', '-', '*', '/', '=', '==', '+=', '-=', '*=', '/=', '!=', '>', '<', '>=', '<=',
            '(', ')', '[', ']', '{', '}', ':'
        ]

        if value in palavras_reservadas:
            self.type = value
            self.value = ''
        else:
            self.type = type
            self.value = value

    def TABELAR(self):
        print(self.type, self.value)
