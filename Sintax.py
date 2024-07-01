class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.sentences = []  # Lista para armazenar listas de tokens por sentença

    def parse(self):
        while self.position < len(self.tokens):
            start_position = self.position  # Marca o início da sentença
            if self.lookahead() in ('<int, >', '<float, >', '<char, >', '<void, >'):
                self.parse_declaration(start_position)
            elif self.lookahead().startswith('<IDENTIFIER,'):
                self.parse_expression(start_position)
            elif self.lookahead() == '<printf, >':
                self.parse_printf_statement(start_position)
            elif self.lookahead() == '<if, >':
                self.parse_if_statement(start_position)
            elif self.lookahead() == '<for, >':
                self.parse_for_loop(start_position)
            elif self.lookahead() == '<while, >':
                self.parse_while_loop(start_position)
            elif self.lookahead() == '<return, >':
                self.parse_return_statement(start_position)
            else:
                self.error('declaration, if statement, for loop, while loop, return statement, or printf statement')

    def parse_declaration(self, start_position):
        self.expect_type()
        if 'IDENTIFIER' in self.lookahead():
            self.expect_identifier()
            if self.lookahead() == '<(, >':
                self.parse_function_declaration(start_position)
            else:
                self.parse_variable_declaration(start_position)
        else:
            self.error('<IDENTIFIER>')

    def parse_variable_declaration(self, start_position):
        if self.lookahead() == '<=, >':
            self.expect('<=, >')
            self.parse_expression(start_position)
        self.expect('<;, >')
        self.record_sentence(start_position, "Variable declaration")
    
    def parse_function_declaration(self, start_position):
        self.expect('<(, >')
        if self.lookahead() != '<), >':  # Se não for uma lista vazia de parâmetros
            self.parse_parameters()
        self.expect('<), >')
        self.expect('<{, >')
        self.parse_block()
        self.expect('<}, >')
        self.record_sentence(start_position, "Function declaration")

    def parse_parameters(self):
        self.expect_type()
        self.expect_identifier()
        while self.lookahead() == '<,, >': 
            self.expect('<,, >')
            self.expect_type()
            self.expect_identifier()
    
    def parse_if_statement(self, start_position):
        self.expect('<if, >')
        self.expect('<(, >')
        self.parse_expression(start_position)
        self.expect('<), >')
        self.expect('<{, >')
        self.parse_block()
        self.expect('<}, >')
        self.record_sentence(start_position, "If statement")
        if self.lookahead() == '<else, >':
            self.expect('<else, >')
            self.expect('<{, >')
            self.parse_block()
            self.expect('<}, >')
            self.record_sentence(start_position, "Else statement")
    
    def parse_for_loop(self, start_position):
        self.expect('<for, >')
        self.expect('<(, >')
        self.parse_declaration(start_position)
        self.parse_expression(start_position)
        self.expect('<;, >')
        self.parse_expression(start_position)
        self.expect('<), >')
        self.expect('<{, >')
        self.parse_block()
        self.expect('<}, >')
        self.record_sentence(start_position, "For loop")
    
    def parse_while_loop(self, start_position):
        self.expect('<while, >')
        self.expect('<(, >')
        self.parse_expression(start_position)
        self.expect('<), >')
        self.expect('<{, >')
        self.parse_block()
        self.expect('<}, >')
        self.record_sentence(start_position, "While loop")
    
    def parse_return_statement(self, start_position):
        self.expect('<return, >')
        self.parse_expression(start_position)
        self.expect('<;, >')
        self.record_sentence(start_position, "Return statement")
    
    def parse_printf_statement(self, start_position):
        self.expect('<printf, >')
        self.expect('<(, >')
        while self.position < len(self.tokens) and self.tokens[self.position] != '<), >':
            self.position += 1
        self.expect('<), >')
        self.expect('<;, >')
        self.record_sentence(start_position, "Printf statement")
    
    def parse_block(self):
        index_atual = self.position
        if self.position == index_atual and self.tokens[index_atual] == '<}, >':
            self.error('<code_block>')
        while self.position < len(self.tokens) and self.tokens[self.position] != '<}, >':
            if self.lookahead() in ('<int, >', '<float, >', '<char, >'):
                self.parse_declaration(self.position)
            elif self.lookahead() == '<printf, >':
                self.parse_printf_statement(self.position)
            elif self.lookahead().startswith('<IDENTIFIER,'):
                if self.lookahead() == '<IDENTIFIER, printf>':
                    self.parse_printf_statement(self.position)
                else:
                    self.parse_expression(self.position)
            elif self.lookahead() == '<if, >':
                self.parse_if_statement(self.position)
            elif self.lookahead() == '<for, >':
                self.parse_for_loop(self.position)
            elif self.lookahead() == '<while, >':
                self.parse_while_loop(self.position)
            elif self.lookahead() == '<return, >':
                self.parse_return_statement(self.position)
            else:
                self.position += 1 # Consome outros tokens por enquanto
    
    def parse_expression(self, start_position):
        while self.position < len(self.tokens) and self.tokens[self.position] not in ('<;, >', '<), >'):
            if self.tokens[self.position].startswith(('<IDENTIFIER,', '<INTEGER_LITERAL,', '<FLOAT_LITERAL,', '<CHAR_LITERAL,')):
                self.position += 1
            elif self.tokens[self.position] in ('<+, >', '<++, >', '<-, >', '<=, >', '<*, >', '</, >', '<==, >', '<!=, >', '<>, >', '<<, >', '<<=, >', '<>=, >'):
                self.position += 1
            elif self.tokens[self.tokens] == '<printf, >':
                self.parse_printf_statement(start_position)
            else:
                self.error('<expression>')

    def record_sentence(self, start_position, description):
        end_position = self.position
        sentence_tokens = self.tokens[start_position:end_position]
        self.sentences.append((description, sentence_tokens))
    
    def expect_type(self):
        if self.position < len(self.tokens) and self.tokens[self.position] in ('<int, >', '<float, >', '<char, >', '<void, >'):
            self.position += 1
        else:
            self.error('<type>')

    def expect(self, expected_token):
        if self.position < len(self.tokens) and self.tokens[self.position] == expected_token:
            self.position += 1
        else:
            self.error(expected_token)
    
    def expect_identifier(self):
        if self.position < len(self.tokens) and self.tokens[self.position].startswith('<IDENTIFIER,'):
            self.position += 1
        else:
            self.error('<IDENTIFIER>')
    
    def lookahead(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None
    
    def error(self, expected_token):
        raise SyntaxError(f"Expected {expected_token} but found {self.tokens[self.position] if self.position < len(self.tokens) else 'EOF'}")
