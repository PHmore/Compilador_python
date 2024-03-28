from TOKEN import TOKEN


class Lexer:
    def __init__(self):
        self.tokens = []
        self.transitions = {
            0: {'letter': 1, 'digit': 2, '+': 6, '-': 7, '*': 8, '/': 9, '=': 11, '<': 12, '>': 13, '(': 14, ')': 15,
                '{': 16, '}': 17, '[': 18, ']': 19, ';': 20, ',': 21, '.': 22, '"': 23},
            1: {'letter': 1, 'digit': 1},
            2: {'digit': 2, '.': 3, 'letter': 4},
            3: {'digit': 5},
            5: {'digit': 5},
            11: {'=': 10},
            23: {'"': 24, ' ': 23, 'letter': 23, 'digit': 23, '+': 23, '-': 23, '*': 23, '/': 23, '=': 23, '<': 23,
                 '>': 23, '(': 23, ')': 23, '{': 23, '}': 23, '[': 23, ']': 23, ';': 23, ',': 23, '.': 23, '%': 23}
        }
        self.accepting = {1: 'IDENTIFIER', 2: 'INTEGER', 5: 'FLOAT', 6: '+', 7: '-', 8: '*', 9: '/', 10: '==',
                          11: '=', 12: '<', 13: '>', 14: '(', 15: ')', 16: '{',
                          17: '}', 18: '[', 19: ']', 20: ';', 21: ',', 22: '.', 24: 'LITERAL'}
        self.reserved_words = ['if', 'else', 'for', 'while', 'int', 'float', 'double', 'char', 'return', 'main', 'void',
                               'switch', 'case', 'break', 'continue', 'typedef', 'struct', 'union', 'enum', 'sizeof',
                               'static', 'const', 'volatile', 'extern', 'register', 'auto', 'signed', 'unsigned', 'do',
                               'short', 'long', 'printf']

    def cria_token(self, state, value):
        if value in self.reserved_words or value in self.accepting.values():
            self.tokens.append(TOKEN(type_token=value))
        else:
            self.tokens.append(TOKEN(self.accepting[state], value))

    def lex(self, code):
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

                if char == code[-1]:
                    self.cria_token(state, value)
            else:
                if state in self.accepting:
                    self.cria_token(state, value)
                    value = ''
                    state = 0

                if input_type in self.transitions[0]:
                    state = self.transitions[0][input_type]
                    value = char

        return self.tokens
