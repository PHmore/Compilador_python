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

# Talvez salvar em uma tabela dps 
# E tentar aplicar um automato finito, pois acho q o mesmo não está send
