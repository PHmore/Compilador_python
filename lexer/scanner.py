from Lexer import Lexer


# Teste do lexer
def test():
    lexer = Lexer()
    font_code = open('teste.txt')
    code = font_code.read()
    tokens = lexer.lex(code)
    for token in tokens:
        print(f'<{token.type}, {token.value}>')


test()
