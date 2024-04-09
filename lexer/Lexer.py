import re

# Classe TOKEN importada para instanciar os tokens
from TOKEN import TOKEN

# Declaração da classe Lexer
class Lexer:
    def __init__(self):
        # Lembra a tabela de automatos onde cada transição representa uma mudança para um outro estado
        """
            Construtor da classe Lexer;
            Inicializa a lista onde os tokens serão armazenados;
            Define dicionários que representam a tabela do autômato utilizado para gerar os tokens;
        """
        self.tokens = []  # Lista com os tokens gerados pela análise léxica
        self.transitions = {
            0: {'letter': 1, 'digit': 2, '+': 6, '-': 7, '*': 8, '/': 9, '=': 11, '<': 12, '>': 13, '(': 14, ')': 15,
                '{': 16, '}': 17, '[': 18, ']': 19, ';': 20, ',': 21, '.': 22, '"': 23, '!': 27, '#': 29},
            1: {'letter': 1, 'digit': 1},
            2: {'digit': 2, '.': 3, 'letter': 4},
            3: {'digit': 5},
            5: {'digit': 5},
            9: {'/': 30, '*': 32},#Adicionar um caso de letra por exemplo \n \t
            11: {'=': 10},
            12: {'=': 25, 'letter': 35},
            13: {'=': 26},
            23: {'"': 24, ' ': 23, 'letter': 23, 'digit': 23, '+': 23, '-': 23, '*': 23, '/': 23, '=': 23, '<': 23,
                 '>': 23, '(': 23, ')': 23, '{': 23, '}': 23, '[': 23, ']': 23, ';': 23, ',': 23, '.': 23, '%': 23,
                 '!': 23},
            27: {'=': 28},
            30: {' ': 30, 'letter': 30, 'digit': 30, '+': 30, '-': 30, '*': 30, '/': 30, '=': 30, '<': 30,
                 '>': 30, '(': 30, ')': 30, '{': 30, '}': 30, '[': 30, ']': 30, ';': 30, ',': 30, '.': 30, '%': 30,
                 '!': 30, '\n': 31},
            32: {' ': 32, 'letter': 32, 'digit': 32, '+': 32, '-': 32, '*': 33, '/': 32, '=': 32, '<': 32,
                 '>': 32, '(': 32, ')': 32, '{': 32, '}': 32, '[': 32, ']': 32, ';': 32, ',': 32, '.': 32, '%': 32,
                 '!': 32},
            33: {'/': 31, ' ': 4, 'letter': 4, 'digit': 4, '+': 4, '-': 4, '*': 4, '=': 4, '<': 4, '>': 4, '(': 4,
                 ')': 4, '{': 4, '}': 4, '[': 4, ']': 4, ';': 4, ',': 4, '.': 4, '%': 4, '!': 4, '\n': 4},
            35: {'letter': 35, '.': 35, '>': 34}
        }
        self.accepting = {1: 'IDENTIFIER', 2: 'INTEGER', 4: 'ERROR', 5: 'FLOAT', 6: '+', 7: '-', 8: '*', 9: '/',
                          10: '==', 11: '=', 12: '<', 13: '>', 14: '(', 15: ')', 16: '{', 17: '}', 18: '[', 19: ']',
                          20: ';', 21: ',', 22: '.', 24: 'LITERAL', 25: '<=', 26: '>=', 28: '!=', 29: '#',
                          31: 'COMMENT', 34: 'LIBRARY'
                          }
        self.reserved_words = ['if', 'else', 'for', 'while', 'int', 'float', 'double', 'char', 'return', 'main', 'void',
                               'switch', 'case', 'break', 'continue', 'typedef', 'struct', 'union', 'enum', 'sizeof',
                               'static', 'const', 'volatile', 'extern', 'register', 'auto', 'signed', 'unsigned', 'do',
                               'short', 'long', 'printf', 'define', 'include']

    def define_tipo(self, char):
        """
            Verifica de qual tipo é o caracter;
            :param char: caracter que será avaliado
            :return input_type: retorna o tipo do caracter
        """
        # print(char)
        if char.isalpha():
            tipo = 'letter'
        elif char.isdigit():
            tipo = 'digit'
        else:
            tipo = char

        return tipo

    def cria_token(self, state, value):
        """
            Instancia um objeto TOKEN com o tipo e valor do token extraído do código lido no arquivo .txt;
        :param state: estado q em que o autômato se encontra no momento de processamento do valor;
        :param value: valor em processamento, que será adicionado a um token;
        """
        # print(value)
        if value in self.reserved_words or value in self.accepting.values():
            self.tokens.append(TOKEN(type_token=value))
        else:
            self.tokens.append(TOKEN(self.accepting[state], value))

    def lex(self, code):
        """
            Método utilizado para fazer a análise léxica de um código;
        :param code: recebe o código lido no arquivo .txt para o processamento e a geração de tokens;
        :return tokens: retorna a lista dos tokens obtidos e instanciados a partir da análise léxica;
        """
        state = 0
        value = ''
        code += '\n'
        for char in code + ' ':  # laço que lê caracter por caracter do arquivo
            input_type = self.define_tipo(char)
            print(state," :Estado e valor: ",value);
            # Verifica se ainda há estados a serem atingidos a partir do estado atual
            if state in self.transitions and input_type in self.transitions[state]:
                state = self.transitions[state][input_type]
                value += char
                # print("Ainda há estados")
            # Se não houver mais estados a serem atingidos, entra no "else"
            else:
                # Se o valor (value) armazenado for estado final
                if state in self.accepting:
                    self.cria_token(state, value)
                    value = ''
                    state = 0

                if input_type in self.transitions[0]:
                    state = self.transitions[0][input_type]
                    value = char

        return self.tokens
