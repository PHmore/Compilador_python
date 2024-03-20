import re
from rules import *
from TOKEN import *


def REGEX(code):
    while code:
        match = None

        for tk_type, pattern in RULES:
            regex = re.compile(pattern)
            match = regex.match(code)

            if match:
                value = match.group(0)
                if tk_type != 'WHITESPACE':
                    token_gerado = TOKEN(tk_type, value)
                    if token_gerado.value != '':
                        print(f'<{token_gerado.type}, "{token_gerado.value}">')
                    elif token_gerado.value == '':
                        print(f'<{token_gerado.type}, {token_gerado.value}>')
                code = code[match.end():]
                break
        if not match:
            raise ValueError('Caractere inválido: ', code[0])

    return


fontCode = open('../../exemplo/example.py')
remaingCode = fontCode.read()
print(remaingCode)

REGEX(remaingCode)
