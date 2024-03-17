# Aqui criaremos a classe scanner a qual chamará as funções do rules 

import re
from rules import *
from TOKEN import *

def REGEX(code):
    while code:
        match = None
        for tk_type, pattern in RULES:
            
            regex = re.compile(pattern)
            match = regex.match(code)
            print(match)
            if match:
                value = match.group(0)
                if tk_type != 'WHITESPACE':
                    TOKEN(tk_type,value)
                code = code[match.end():]
                break

        if not match:
            raise ValueError('Caractere inválido: '+ code[0])
    return


fontCode = open('./exemplo/example.py')
remaingCode = fontCode.read()
print (remaingCode)

REGEX(remaingCode)

"""
import re

# Definindo os tokens e padrões regulares correspondentes
TOKENS = [
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
    ('WHITESPACE', r'\s+'),
]

# Função para tokenizar o código fonte
def tokenize(code):
    tokens = []
    while code:
        match = None
        for token_type, pattern in TOKENS:
            regex = re.compile(pattern)
            match = regex.match(code)
            if match:
                value = match.group(0)
                if token_type != 'WHITESPACE':
                    tokens.append((token_type, value))
                code = code[match.end():]
                break
        if not match:
            raise ValueError('Caractere inválido: ' + code[0])
    return tokens

# Função principal para testar o analisador léxico
def main():
    while True:
        try:
            code = input("Digite o código Python: ")
            tokens = tokenize(code)
            print("Tokens:")
            for token in tokens:
                print(token)
        except KeyboardInterrupt:
            print("\nPrograma encerrado.")
            break

if __name__ == "__main__":
    main()
"""