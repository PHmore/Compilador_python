from Lexer import Lexer


# Teste do lexer
def test():
    lexer = Lexer()
    # font_code = open('teste.txt')
    # code = font_code.read()
    code = 'int x = 4;'
    code += ' '
    tokens = lexer.lex(code)
    for token in tokens:
        print(f'<{token.type}, {token.value}>')


test()
