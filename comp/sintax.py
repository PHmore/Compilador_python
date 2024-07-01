import ply.lex as lex
import ply.yacc as yacc

# Lista de tokens
tokens = [
    'ID', 'INTEGER', 'FLOAT',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'SEMICOLON', 'INT', 'FLOAT_TYPE', 'RETURN',
    'EQUALS', 'IF', 'ELSE', 'LT', 'LE', 'GT', 'GE', 'EQ', 'NE'  # Adicionamos ELSE como um novo token
]

# Palavras-chave reservadas
reserved = {
    'int': 'INT',
    'float': 'FLOAT_TYPE',
    'return': 'RETURN',
    'if': 'IF',
    'else': 'ELSE'
}

# Expressões regulares para tokens simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_EQUALS = r'='

# Expressões regulares para operadores lógicos
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='

# Expressão regular para números de ponto flutuante
def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# Expressão regular para números inteiros
def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Expressão regular para identificadores (IDs)
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# Ignorar caracteres em branco (espaços e tabs)
t_ignore = ' \t'

# Tratamento de novas linhas (para contagem)
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Tratamento de erros
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Definindo as regras gramaticais
def p_program(p):
    '''program : type ID LPAREN RPAREN LBRACE statements RBRACE'''
    p[0] = ('program', p[1], p[2], p[6])

def p_type(p):
    '''type : INT
            | FLOAT'''
    p[0] = p[1]

def p_statements(p):
    '''statements : statement
                  | statement statements'''
    p[0] = [p[i] for i in range(1, len(p))]

def p_statement(p):
    '''statement : assignment
                 | return_statement
                 | if_statement'''
    p[0] = p[1]

def p_assignment(p):
    '''assignment : type ID EQUALS expression SEMICOLON'''
    p[0] = ('assignment', p[1], p[2], p[4])

def p_return_statement(p):
    '''return_statement : RETURN expression SEMICOLON'''
    p[0] = ('return', p[2])

def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN LBRACE statements RBRACE'''
    p[0] = ('if', p[3], p[6])

def p_if_else_statement(p):
    '''if_statement : IF LPAREN expression RPAREN LBRACE statements RBRACE ELSE LBRACE statements RBRACE'''
    p[0] = ('if-else', p[3], p[6], p[10])

def p_expression(p):
    '''expression : ID
                  | INTEGER
                  | FLOAT
                  | expression LT expression
                  | expression LE expression
                  | expression GT expression
                  | expression GE expression
                  | expression EQ expression
                  | expression NE expression'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])

# Lida com erros de sintaxe
def p_error(p):
    if p:
        print(f"Erro de sintaxe na entrada: {p.value}")
    else:
        print("Erro de sintaxe no final da entrada")

# Construindo o lexer e parser
lexer = lex.lex()
parser = yacc.yacc()

# Código de teste
if __name__ == '__main__':
    code = '''
    int main() {
        int a = 5;
        if (a > 3) {
            return a;
        } else {
            return 0;
        }
    }
    '''
    lexer.input(code)
    parsed = parser.parse(lexer=lexer)
    print("AST:", parsed)