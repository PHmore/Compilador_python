from Lexer import Lexer


# Teste do lexer
def test():
    """
        Função para teste do analisador léxico;
        O código é extraído de um arquivo .txt e analisado;
    """
    lexer = Lexer()
    font_code = open('./lexer/teste.c','r')
    code = font_code.read()
    # code = 'int x = 4;\n//fdsfa'
    # code += ' '
    tokens = lexer.lex(code)
    for token in tokens:
        print(f'<{token.type}, {token.value}>')

# Salvando tokens em um txt
    caminho_do_arquivo = "output.txt"
    
    with open(caminho_do_arquivo, 'w') as arquivo:
        for token in tokens:
            arquivo.write(f'<{token.type}, {token.value}> ')

# Programa Principal
test()
