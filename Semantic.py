class Tradutor:
    # Construtor da Classe; instancia a lista de tokens e salva a posição da lista
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def traduzir(self):
        traducao = ["import sys", "import math", ""]

        # Percorre todos os tokens da lista
        while self.position < len(self.tokens):
            token, value = self._next_token()
            if value in ['int', 'char', 'float']:  # Verifica se é uma declaração de variável ou função
                next_token, next_value = self._peek_token()
                if next_value == 'main':  # Verifica se é a declaração da função main()
                    self._translate_main(traducao)
                else:
                    self._translate_variable(traducao, value)  # Caso não seja, é apenas uma declaração de variável comum
            elif value == 'for':  # Verifica se o token lido no momento indica o início de loop for
                self._translate_for(traducao)
            elif value == 'while':  # Verifica se o token lido no momento indica o início de loop while
                self._translate_while(traducao)
            elif 'RESERVED_WORD' in token:
                    if value == 'printf':
                        self._translate_printf(traducao)
            elif 'IDENTIFIER' in token:  # Verifica se a sentença começa apenas com um identificador, indicando atribuição de valor    
                self.position -= 1
                self._translate_assignment(traducao)

        return "\n".join(traducao)
    
    def _next_token(self):  # Pega o próximo token da lista e aumenta uma posição
        token = self.tokens[self.position]
        self.position += 1
        return token[1:-1].split(', ')

    def _peek_token(self):
        token = self.tokens[self.position]
        return token[1:-1].split(", ")

    def _translate_main(self, traducao):  # Faz a tradução da função main()
        traducao.append("def main():")
        self._next_token()  # Ignorar 'main'
        self._next_token()  # Ignorar '('
        self._next_token()  # Ignorar ')'
        self._next_token()  # Ignorar '{'
        
        while self.position < len(self.tokens):
            token, value = self._next_token()
            if value == 'return':
                traducao.append("    return ", end='')
                token, value = self._next_token()
                traducao[-1] += f"{token}"
                token, value = self._next_token()
                if value == 'OPERADOR_ARITMETICO':
                    traducao[-1] += f" {token} "
                    token, value = self._next_token()
                    traducao[-1] += f"{token}"
                self._next_token()  # Ignorar ';'
            elif value == '}':
                break
            else:
                self.position -= 1
                self._translate_statement(traducao)
        
        traducao.append("")
        traducao.append("if __name__ == '__main__':")
        traducao.append("    main()")

    def _translate_variable(self, traducao, tipo):  # Traduz a declaração de uma variável, ou atribuição de outro valor a uma variável já existente
        _, var_name = self._next_token()
        var_name = var_name.strip()
        if '=' in self._next_token():
            _, var_valor = self._next_token()
            var_valor = var_valor.replace('"', "'")
            traducao.append(f"{var_name} = {var_valor}")
        else:
            traducao.append(f"{var_name} = 0" if tipo in ['int', 'float'] else f"{var_name} = ''")
            self._next_token()  # Ignorar ';'

    def _translate_assignment(self, traducao):
        ident_token, ident_value = self._next_token()
        ident_value = ident_value.strip()
        operator_token, operator_value = self._next_token()
        _, valor_atribuido = self._next_token()
        traducao.append(f"{ident_value} {operator_value} {valor_atribuido}")

    def _translate_statement(self, traducao):
        token, value = self._next_token()
        if value in ['int', 'float', 'char']:
            self._translate_variable(traducao, value)
        elif value == 'for':
            self._translate_for(traducao)
        elif value == 'while':
            self._translate_while(traducao)
        elif 'RESERVED_WORD' in token:
                if value == 'printf':
                    self._translate_printf(traducao)
        elif 'IDENTIFIER' in token:
            self.position -= 1
            self._translate_assignment(traducao)

    def _translate_for(self, traducao):
        self._next_token()  # Ignorar 'for'
        init_var, init_value = self._next_token()
        init_value = init_value.replace('IDENTIFIER, ', '')
        self._next_token()  # Ignorar '='
        _, start_val = self._next_token()
        self._next_token()  # Ignorar ';'
        self._next_token()  # Ignorar o identificador
        cond_var, cond_op = self._next_token()
        cond_var = cond_var.replace('IDENTIFIER, ', '')
        cond_op = cond_op[:-1].strip()
        _, limit_val = self._next_token()
        self._next_token()  # Ignorar ';'
        inc_var, inc_op = self._next_token()
        inc_var = inc_var.replace('IDENTIFIER, ', '')
        inc_op = inc_op[:-1].strip()
        self._next_token()  # Ignorar ')'
        self._next_token()  # Ignorar '{'
        
        traducao.append(f"for {init_value} in range({start_val}, {limit_val}):")
        
        while self.position < len(self.tokens):
            token, value = self._next_token()
            if value == '}':
                break
            else:
                self.position -= 1
                self._translate_statement(traducao)
        
        self._next_token()  # Ignorar '}'

    def _translate_while(self, traducao):
        self._next_token()
        init_var, init_value = self._next_token()
        _, operador = self._next_token()
        cond_var, valor_limite = self._next_token()
        self._next_token()
        self._next_token()
        
        traducao.append(f"while {init_value} {operador} {valor_limite}:")
        
        while self.position < len(self.tokens):
            token, value = self._next_token()
            if value == '}':
                break
            else:
                self.position -= 1
                self._translate_statement(traducao)
        
        self._next_token()  # Ignorar '}'

    def _translate_printf(self, traducao):
        self._next_token()
        string_token, string_value = self._next_token()
        self._next_token()
        self._next_token()

        traducao.append(f"print({string_value})")

tokens = [
    '<RESERVED_WORD, int>', '<RESERVED_WORD, main>', '<DELIMITER, (>', '<DELIMITER, )>', '<DELIMITER, {>', 
        '<RESERVED_WORD, int>', '<IDENTIFIER, numero>', '<OPERADOR_ATRIBUICAO, =>', '<INTEGER_LITERAL, 10>', '<;, >', 
        '<RESERVED_WORD, char>', '<IDENTIFIER, nome>', '<OPERADOR_ATRIBUICAO, =>', '<LITERAL, "Lucas">', '<;, >',
        '<RESERVED_WORD, while>', '<DELIMITER, (>', '<IDENTIFIER, numero>', '<OPERADOR_RELACIONAL, <>', '<INTEGER_LITERAL, 5>', '<DELIMITER, )>', '<DELIMITER, {>', 
            '<IDENTIFIER, numero>', '<OPERADOR_ATRIBUICAO, =>', '<INTEGER_LITERAL, 1>', '<;, >',
            '<RESERVED_WORD, printf>', '<DELIMITER, (>', '<LITERAL, "Hello world">', '<DELIMITER, )>', '<;, >',
        '<DELIMITER, }>', 
    '<DELIMITER, }>'
]

tradutor = Tradutor(tokens)
codigo_python = tradutor.traduzir()
print(codigo_python)
