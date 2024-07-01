from Lexer import Lexer
from Sintax import Parser

tokens = []

code = '''int main() {
    int somar(int a, int b){
        return a + b;
    }
    printf("Olá, mundo");
    for(int c = 0; c < 4; c++){
        printf("Olá, mundo");
    }
}'''

lexer = Lexer()

resultado_lexer = lexer.lex(code)
for token in resultado_lexer:
    if token.type != '\\n':
        tokens.append(f'<{token.type}, {token.value}>')

parser = Parser(tokens)
parser.parse()

# Exibindo as sentenças reconhecidas
print("Sentenças reconhecidas:")
for description, tokens in parser.sentences:
    print(description, " -> Tokens:", tokens, '\n\n\n')