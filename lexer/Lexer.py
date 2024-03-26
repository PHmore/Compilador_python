from TOKEN import TOKEN


class Lexer:
    def __init__(self):
        self.transitions = {
            0: {'letter': 1, 'digit': 2, '+': 6, '-': 7, '*': 8, '/': 9, '=': 11, '<': 12, '>': 13, '(': 14, ')': 15,
                '{': 16, '}': 17, '[': 18, ']': 19, ';': 20, ',': 21, '.': 22},
            1: {'letter': 1, 'digit': 1},
            2: {'digit': 2, '.': 3, 'letter': 4},
            3: {'digit': 5},
            5: {'digit': 5}
        }
        self.accepting = {1: 'IDENTIFIER', 2: 'INTEGER', 5: 'FLOAT', 6: 'PLUS', 7: 'MINUS', 8: 'TIMES', 9: 'DIVIDE',
                          11: 'ASSIGN', 12: 'LESS_THAN', 13: 'GREATER_THAN', 14: 'LPAREN', 15: 'RPAREN', 16: 'LBRACE',
                          17: 'RBRACE', 18: 'LBRACKET', 19: 'RBRACKET', 20: 'SEMICOLON', 21: 'COMMA', 22: 'DOT'}
        self.reserved_words = ['if', 'else', 'for', 'while', 'int', 'float', 'double', 'char', 'return', 'main', 'void',
                               'switch', 'case', 'break', 'continue', 'typedef', 'struct', 'union', 'enum', 'sizeof',
                               'static', 'const', 'volatile', 'extern', 'register', 'auto', 'signed', 'unsigned',
                               'short', 'long', 'do']

    def lex(self, code):
        tokens = []
        state = 0
        value = ''

        for char in code:
            if char.isalpha():
                input_type = 'letter'
            elif char.isdigit():
                input_type = 'digit'
            else:
                input_type = char

            if state in self.transitions and input_type in self.transitions[state]:
                state = self.transitions[state][input_type]
                value += char
            else:
                if state in self.accepting:
                    if state == 1 and value in self.reserved_words:
                        tokens.append(TOKEN('RESERVED', value))
                    else:
                        tokens.append(TOKEN(self.accepting[state], value))
                    value = ''
                    state = 0

                if input_type in self.transitions[0]:
                    state = self.transitions[0][input_type]
                    value = char

        if state in self.accepting:
            if state == 1 and value in self.reserved_words:
                tokens.append(TOKEN('RESERVED', value))
            else:
                tokens.append(TOKEN(self.accepting[state], value))

        return tokens
