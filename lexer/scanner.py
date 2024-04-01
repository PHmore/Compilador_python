from Lexer import Lexer


# Teste do lexer
def test():
    """
        Função para teste do analisador léxico;
        O código é extraído de um arquivo .txt e analisado;
    """
    lexer = Lexer()
    font_code = open('teste.txt')
    code = font_code.read()
    tokens = lexer.lex(code)
    for token in tokens:
        print(f'<{token.type}, {token.value}>')


# Programa Principal
test()
