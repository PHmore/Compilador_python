import ply.yacc as yacc
from ..lexer.Lexer import Lexer
# Instanciando o lexer
lexer = Lexer()

# Obtendo a lista de tokens do código de entrada
code = '''
int main() {
    int a = 5;
    return a;
}
'''
tokens = lexer.lex(code)

# Definindo os tokens reconhecidos pelo lexer
tokens = [token.type for token in tokens]

# Definindo as regras gramaticais
def p_program(p):
    '''program : type ID LPAREN RPAREN LBRACE statements RBRACE'''
    p[0] = ('program', p[1], p[2], p[6])

def p_type(p):
    '''type : INT
            | FLOAT
            | CHAR'''
    p[0] = p[1]

def p_statements(p):
    '''statements : statement
                  | statement statements'''
    p[0] = [p[i] for i in range(1, len(p))]

def p_statement(p):
    '''statement : assignment
                 | return_statement'''
    p[0] = p[1]

def p_assignment(p):
    '''assignment : type ID EQUALS expression SEMICOLON'''
    p[0] = ('assignment', p[1], p[2], p[4])

def p_return_statement(p):
    '''return_statement : RETURN expression SEMICOLON'''
    p[0] = ('return', p[2])

def p_expression(p):
    '''expression : ID
                  | NUMBER'''
    p[0] = p[1]

# Lida com erros de sintaxe
def p_error(p):
    if p:
        print(f"Erro de sintaxe na entrada: {p.value}")
    else:
        print("Erro de sintaxe no final da entrada")

# Construindo o parser
parser = yacc.yacc()

# Parseando o código
parsed = parser.parse(tokens)

# Imprimindo a árvore sintática (AST)
print("AST:", parsed)
