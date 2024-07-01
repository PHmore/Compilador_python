import ply.lex as lex

# Lista de tokens
tokens = [
    'ID', 'INTEGER', 'FLOAT',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'SEMICOLON', 'INT', 'FLOAT_TYPE', 'RETURN'
]

# Palavras-chave reservadas
reserved = {
    'int': 'INT',
    'float': 'FLOAT_TYPE',
    'return': 'RETURN'
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
    t.type = reserved.get(t.value, 'ID')  # Verifica se é uma palavra reservada
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

# Construindo o lexer
lexer = lex.lex()
