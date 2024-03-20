# Aqui estarão as regex
RULES = [
    ('NUMBER', r'\d+(\.\d+)?'),
    ('STRING', r'\".*?\"'),
    ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('PLUS', r'\+'),
    ('MINUS', r'\-'),
    ('TIMES', r'\*'),
    ('DIVIDE', r'\/'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('ASSIGN', r'='),
    ('EQUIASSIGN', r'=='),
    ('WHITESPACE', r'\s+'),
    ('DOUBLEPOINTS', r':?')
]
