class Tradutor:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.indent_level = 0  # Nível atual de indentação

    def traduzir(self):
        traducao = ["import sys", "import math", ""]
        while self.position < len(self.tokens):
            token, value = self._next_token()
            if value in ['int', 'char', 'float', 'void']:
                next_token, next_value = self._peek_token()
                if next_value == 'main':
                    self._translate_main(traducao)
                else:
                    self._translate_function_or_variable(traducao, value)
            elif value == 'for':
                self._translate_for(traducao)
            elif value == 'while':
                self._translate_while(traducao)
            elif value == 'if':
                self._translate_if(traducao)
            elif value == 'else':
                self._translate_else(traducao)
            elif 'OPERADOR_ARITMETICO' in token and value == '++':
                self.translate_plus_one(traducao)
            elif 'RESERVED_WORD' in token and value == 'printf':
                self._translate_printf(traducao)
            elif 'IDENTIFIER' in token:
                self.position -= 1
                self._translate_assignment(traducao)
        return "\n".join(traducao)

    def _next_token(self):
        token = self.tokens[self.position]
        self.position += 1
        return token[1:-1].split(', ')

    def _peek_token(self):
        token = self.tokens[self.position]
        return token[1:-1].split(", ")

    def _translate_main(self, traducao):
        traducao.append(self._indent("def main():"))
        self.indent_level += 1
        self._next_token()
        self._next_token()
        self._next_token()
        self._next_token()

        while self.position < len(self.tokens):
            token, value = self._next_token()
            if value == 'return':
                traducao.append(self._indent("return ", end=''))
                token, value = self._next_token()
                traducao[-1] += f"{token}"
                token, value = self._next_token()
                if value == 'OPERADOR_ARITMETICO':
                    traducao[-1] += f" {token} "
                    token, value = self._next_token()
                    traducao[-1] += f"{token}"
                self._next_token()
            elif value == '}':
                self.indent_level -= 1
                break
            else:
                self.position -= 1
                self._translate_statement(traducao)

        traducao.append("")
        traducao.append("if __name__ == '__main__':")
        traducao.append(self._indent("main()"))
        self.indent_level -= 1

    def _translate_function_or_variable(self, traducao, tipo):
        _, name = self._next_token()
        next_token, next_value = self._peek_token()

        if next_value == '(':
            self._translate_function(traducao, name)
        else:
            self._translate_variable(traducao, tipo)

    def _translate_function(self, traducao, name):
        self._next_token()
        self._next_token()
        self._next_token()
        self._next_token()

        traducao.append(self._indent(f"def {name}():"))
        self.indent_level += 1

        while self.position < len(self.tokens):
            token, value = self._next_token()
            if value == '}':
                self.indent_level -= 1
                break
            else:
                self.position -= 1
                self._translate_statement(traducao)

        traducao.append("")

    def _translate_variable(self, traducao, tipo):
        _, var_name = self._next_token()
        var_name = var_name.strip()
        if '=' in self._next_token():
            _, var_valor = self._next_token()
            var_valor = var_valor.replace('"', "'")
            traducao.append(self._indent(f"{var_name} = {var_valor}"))
        else:
            traducao.append(self._indent(f"{var_name} = 0" if tipo in ['int', 'float'] else f"{var_name} = ''"))
            self._next_token()

    def _translate_assignment(self, traducao):
        ident_token, ident_value = self._next_token()
        ident_value = ident_value.strip()
        operator_token, operator_value = self._next_token()
        _, valor_atribuido = self._next_token()
        traducao.append(self._indent(f"{ident_value} {operator_value} {valor_atribuido}"))

    def _translate_statement(self, traducao):
        token, value = self._next_token()
        if value in ['int', 'float', 'char', 'void']:
            self._translate_variable(traducao, value)
        elif value == 'for':
            self._translate_for(traducao)
        elif value == 'while':
            self._translate_while(traducao)
        elif value == 'if':
            self._translate_if(traducao)
        elif value == 'else':
            self._translate_else(traducao)
        elif 'OPERADOR_ARITMETICO' in self._peek_token() and '++' in self._peek_token():
            self.translate_plus_one(traducao, self.tokens[self.position - 1])
        elif 'RESERVED_WORD' in token and value == 'printf':
            self._translate_printf(traducao)
        elif 'IDENTIFIER' in token:
            self.position -= 1
            self._translate_assignment(traducao)

    def translate_plus_one(self, traducao, identificador):
        self._next_token()
        _, variavel = identificador[1:-1].split(', ')
        traducao.append(self._indent(f"{variavel} += 1"))

    def _translate_for(self, traducao):
        self._next_token()
        self._next_token()
        init_var, init_value = self._next_token()
        self._next_token()
        _, start_val = self._next_token()
        self._next_token()
        self._next_token()
        cond_var, cond_op = self._next_token()
        cond_var = cond_var.replace('IDENTIFIER, ', '')
        cond_op = cond_op[:-1].strip()
        _, limit_val = self._next_token()
        traducao.append(self._indent(f"for {init_value} in range({start_val}, {limit_val}):"))
        self.indent_level += 1

        self._next_token()
        self._next_token()
        self._next_token()
        self._next_token()

        while self.position < len(self.tokens):
            token, value = self._next_token()
            if value == '}':
                self.indent_level -= 1
                break
            else:
                self.position -= 1
                self._translate_statement(traducao)

    def _translate_while(self, traducao):
        self._next_token()
        init_var, init_value = self._next_token()
        _, operador = self._next_token()
        cond_var, valor_limite = self._next_token()
        self._next_token()
        self._next_token()

        traducao.append(self._indent(f"while {init_value} {operador} {valor_limite}:"))
        self.indent_level += 1

        while self.position < len(self.tokens):
            token, value = self._next_token()
            if value == '}':
                self.indent_level -= 1
                break
            else:
                self.position -= 1
                self._translate_statement(traducao)

        self._next_token()

    def _translate_if(self, traducao):
        self._next_token()
        _, identificador = self._next_token()
        _, operador = self._next_token()
        _, valor_comparar = self._next_token()
        self._next_token()
        self._next_token()

        traducao.append(self._indent(f"if {identificador} {operador} {valor_comparar}:"))
        self.indent_level += 1

        while self.position < len(self.tokens):
            token, value = self._next_token()
            if value == '}':
                self.indent_level -= 1
                break
            else:
                self.position -= 1
                self._translate_statement(traducao)

    def _translate_else(self, traducao):
        self._next_token()

        traducao.append(self._indent("else:"))
        self.indent_level += 1

        while self.position < len(self.tokens):
            token, value = self._next_token()
            if value == '}':
                self.indent_level -= 1
                break
            else:
                self.position -= 1
                self._translate_statement(traducao)

    def _translate_printf(self, traducao):
        self._next_token()
        string_token, string_value = self._next_token()
        self._next_token()
        self._next_token()

        traducao.append(self._indent(f"print({string_value})"))

    def _indent(self, line, end=''):
        return '    ' * self.indent_level + line + end


tokens = [
    '<RESERVED_WORD, void>', '<IDENTIFIER, minhaFuncao>', '<DELIMITER, (>', '<DELIMITER, )>', '<DELIMITER, {>',
        '<RESERVED_WORD, int>', '<IDENTIFIER, x>', '<OPERADOR_ATRIBUICAO, =>', '<INTEGER_LITERAL, 10>', '<;, >',
        '<RESERVED_WORD, printf>', '<DELIMITER, (>', '<LITERAL, "Valor de x: " + x>', '<DELIMITER, ,>', '<IDENTIFIER, x>', '<DELIMITER, )>', '<;, >',
    '<DELIMITER, }>',

    '<RESERVED_WORD, void>', '<RESERVED_WORD, main>', '<DELIMITER, (>', '<DELIMITER, )>', '<DELIMITER, {>',
        '<RESERVED_WORD, int>', '<IDENTIFIER, numero>', '<OPERADOR_ATRIBUICAO, =>', '<INTEGER_LITERAL, 0>', '<;, >',
        '<RESERVED_WORD, char>', '<IDENTIFIER, letra>', '<OPERADOR_ATRIBUICAO, =>', '<LITERAL, "K">', '<;, >',

        '<RESERVED_WORD, printf>', '<DELIMITER, (>', '<LITERAL, "A letra é " + letra>', '<DELIMITER, )>', '<;, >',

        '<RESERVED_WORD, if>', '<DELIMITER, (>', '<IDENTIFIER, numero>', '<OPERADOR_RELACIONAL, ==>', '<INTEGER_LITERAL, 0>', '<DELIMITER, )>', '<DELIMITER, {>',
            '<RESERVED_WORD, printf>', '<DELIMITER, (>', '<LITERAL, "O número é zero!">', '<DELIMITER, )>', '<;, >',
        '<DELIMITER, }>', '<RESERVED_WORD, else>', '<DELIMITER, {>',
            '<RESERVED_WORD, printf>', '<DELIMITER, (>', '<LITERAL, "O número não é zero...">', '<DELIMITER, )>', '<;, >',
        '<DELIMITER, }>',
        '<RESERVED_WORD, for>', '<DELIMITER, (>', '<RESERVED_WORD, int>', '<IDENTIFIER, i>', '<OPERADOR_ATRIBUICAO, =>', '<INTEGER_LITERAL, 0>', '<DELIMITER, ;>',
        '<IDENTIFIER, i>', '<OPERADOR_RELACIONAL, <>', '<INTEGER_LITERAL, 5>', '<DELIMITER, ;>',
        '<IDENTIFIER, i>', '<OPERADOR_ARITMETICO, ++>', '<DELIMITER, )>', '<DELIMITER, {>',
            '<RESERVED_WORD, printf>', '<DELIMITER, (>', '<LITERAL, "Hello World (for)">', '<DELIMITER, )>','<;, >',
        '<DELIMITER, }>',
        '<RESERVED_WORD, while>', '<DELIMITER, (>', '<IDENTIFIER, numero>', '<OPERADOR_RELACIONAL, <>', '<INTEGER_LITERAL, 5>', '<DELIMITER, )>', '<DELIMITER, {>',
            '<RESERVED_WORD, printf>', '<DELIMITER, (>', '<LITERAL, "Hello world (while)">', '<DELIMITER, )>', '<;, >',
            '<IDENTIFIER, numero>', '<OPERADOR_ARITMETICO, ++>', '<;, >',
        '<DELIMITER, }>',
    '<DELIMITER, }>',
]

tradutor = Tradutor(tokens)
codigo_python = tradutor.traduzir()
print(codigo_python)
