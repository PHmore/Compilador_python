import re

class TOKEN:
    __init__(self,)

# Definição dos tokens
TOKENS = [
    ('ID',r'[A-Za-z][A-Za-z]*'),
    ('NUMBER', r'\d+(\.\d+)?'),  # Números inteiros e decimais
    ('PLUS', r'\+'),              # Operador de adição
    ('MINUS', r'\-'),             # Operador de subtração
    ('TIMES', r'\*'),             # Operador de multiplicação
    ('DIVIDE', r'\/'),            # Operador de divisão
    ('LPAREN', r'\('),            # Parêntese esquerdo
    ('RPAREN', r'\)'),            # Parêntese direito
    ('WHITESPACE', r'\s+'),       # Espaços em branco
]

# Usaremos uma tupla cara geração de tokens do tipo <tipo,lexema(valor)>
# OBS: Palavras reservadas não precisam conter lexema visto que são escritos apenas de uma forma

# Cada token têm um número /nome

# Separamos aqui os tokens para cada espaço \n \t ou qualquer outro fator
def TOKEN(expression):
    re.compile()

# Usaremos uma tabela de simbólos para dizer qual o tipo do token

# KWs (Key words) palavras reservadas
def KW_int():
    re.compile()

# ID identificadores
def ID(expression):
    patternID=re.compile('\d(\d*)')
    result = re.findall(patternID,expression)
    print(result)

# Números reais

# Números inteiros sem sinal
    
# Números reais
    
# Caracteres especiais
    
# Comentários
    