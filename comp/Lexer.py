# Importando os módulos necessários
import ply.lex as lex
import ply.yacc as yacc

# Lista de tokens
tokens = [
    'ID', 'INTEGER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN',
    'EQUALS', 'SEMICOLON', 'INT'
]

# Expressões regulares para tokens simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_EQUALS = r'='
t_SEMICOLON = r';'

# Expressão regular para números inteiros
def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Expressão regular para identificadores (IDs)
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

# Ignorar caracteres em branco (espaços e tabs)
t_ignore = ' \t'

# Tratamento de novas linhas (para contagem)
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Tratamento de erros
def t_error(t):
    print(f"Caractere inválido: '{t.value[0]}'")
    t.lexer.skip(1)

# Construindo o lexer
lexer = lex.lex()

# Definindo as regras gramaticais
def p_program(p):
    '''program : INT declarations statements'''
    p[0] = p[3]

def p_declarations(p):
    '''declarations : declarations declaration
                    | declaration'''
    if len(p) == 3:
        p[0] = p[1] + p[2]
    else:
        p[0] = p[1]

def p_declaration(p):
    '''declaration : INT ID SEMICOLON'''
    p[0] = f'inteiro {p[2]};\n'

def p_statements(p):
    '''statements : statements statement
                  | statement'''
    if len(p) == 3:
        p[0] = p[1] + p[2]
    else:
        p[0] = p[1]

def p_statement_assign(p):
    '''statement : ID EQUALS expression SEMICOLON'''
    p[0] = f'{p[1]} = {p[3]};\n'

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    p[0] = f'({p[1]} {p[2]} {p[3]})'

def p_expression_integer(p):
    '''expression : INTEGER'''
    p[0] = str(p[1])

# Lida com erros de sintaxe
def p_error(p):
    if p:
        print(f"Erro de sintaxe na entrada: {p.value}")
    else:
        print("Erro de sintaxe no final da entrada")

# Construindo o parser
parser = yacc.yacc()

# Função principal para tradução
def translate_c_to_portugol(code):
    lexer.input(code)
    parsed = parser.parse(lexer=lexer)
    return parsed

# Exemplo de uso
if __name__ == '__main__':
    code = '''
    int main() {
        int a;
        int b;
        a = 5;
        b = 3;
        int c;
        c = a + b * 2;
    }
    '''
    translated_code = translate_c_to_portugol(code)
    print("Código traduzido para PORTUGOL:")
    print(translated_code)