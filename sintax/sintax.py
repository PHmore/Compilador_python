# Definição da gramática

gramatica = {
    'Programa': ['DeclaraçãoLista'],
    'DeclaraçãoLista': ['Declaração', 'Declaração DeclaraçãoLista'],
    'Declaração': ['DeclaraçãoVariável', 'DeclaraçãoFunção', 'DeclaraçãoEstrutura'],
    'DeclaraçãoVariável': ['Tipo Identificador ;', 'Tipo Identificador [ Número ] ;'],
    'DeclaraçãoFunção': ['Tipo Identificador ( ListaParâmetros ) DeclaraçãoComposta'],
    'DeclaraçãoComposta': ['{ DeclaraçãoLista }'],
    'Tipo': ['int', 'float', 'char', 'void'],
    'ListaParâmetros': ['ListaVazia', 'Tipo Identificador', 'Tipo Identificador , ListaParâmetros'],
    'DeclaraçãoEstrutura': ['struct Identificador { DeclaraçãoLista } ;'],
    'Expressão': ['ExpressãoAtribuição', 'Expressão , ExpressãoAtribuição'],
    'ExpressãoAtribuição': ['Identificador = Expressão', 'ExpressãoCondicional'],
    'ExpressãoCondicional': ['ExpressãoLogica ? Expressão : Expressão'],
    'ExpressãoLogica': ['ExpressãoLogica || ExpressãoLogica', 'ExpressãoLogica && ExpressãoLogica', 'ExpressãoRelacional'],
    'ExpressãoRelacional': [
        'ExpressãoAditiva > ExpressãoAditiva', 
        'ExpressãoAditiva < ExpressãoAditiva', 
        'ExpressãoAditiva >= ExpressãoAditiva', 
        'ExpressãoAditiva <= ExpressãoAditiva', 
        'ExpressãoAditiva == ExpressãoAditiva', 
        'ExpressãoAditiva != ExpressãoAditiva'
    ],
    'ExpressãoAditiva': ['ExpressãoAditiva + Termo', 'ExpressãoAditiva - Termo', 'Termo'],
    'Termo': ['Termo * Fator', 'Termo / Fator', 'Fator'],
    'Fator': ['( Expressão )', 'number', 'ID'],
    'Identificador': ['ID'],
    'Número': ['number'],
    'ListaVazia': ['ε']
}


# Dicionário de símbolos terminais
simbolos_terminais = {
    'Operadores': [
        '+', '-', '*', '/',  # Operadores aritméticos
        '>', '<', '>=', '<=', '==', '!=',  # Operadores relacionais
        '||', '&&', '? :',  # Operadores lógicos
        '='  # Operador de atribuição
    ],
    'Operandos': [
        'Identificador',  # Identificadores
        'Número',  # Números
        'int', 'float', 'char', 'void'  # Tipos primitivos
    ],
    'Outros Símbolos': [
        ';', ',', '{', '}', '(', ')', '[', ']',  # Símbolos de pontuação
        'struct'  # Palavra-chave
    ]
}

# Imprimir a tabela de símbolos terminais
for categoria, simbolos in simbolos_terminais.items():
    print(f"{categoria}:")
    for simbolo in simbolos:
        print(f"  - {simbolo}")



"""

OBS: vazio = £

Uma gramatica livre de contexto deve conter 
G = (N,T,P,S)
N = Conjunto de não terminais
T = Conjunto de terminais que são representados pelos tokens
P = Regras de derivação (produção)
S = Não terminal inicial que representa a raiz da gramática


Tomar cuidado com recursão a esquerda na linha de produção exemplo:

G(E) - Recursiva (direta) à esquerda
E ::= E + T | T
T ::= T * F | F
F ::= ID | (E)

G'(E) - Não recursiva à esquerda
E ::= T E'
T ::= F T'
F ::= ID | ( E )
E' ::= + T E' | £
T' ::= * F T' | £

S ::= D
D ::= D' | D' D
D' ::= V | F | H
V ::= 

Programa ::= DeclaraçãoLista

DeclaraçãoLista ::= Declaração | Declaração DeclaraçãoLista

Declaração -> DeclaraçãoVariável | DeclaraçãoFunção | DeclaraçãoEstrutura

DeclaraçãoVariável -> Tipo Identificador ';'
                    | Tipo Identificador '[' Número ']' ';'

DeclaraçãoFunção -> Tipo Identificador '(' ListaParâmetros ')' DeclaraçãoComposta

DeclaraçãoComposta -> '{' DeclaraçãoLista '}'

Tipo -> 'int' | 'float' | 'char' | 'void'

ListaParâmetros -> ListaVazia
                  | ListaParâmetros
                  | Tipo Identificador
                  | Tipo Identificador ',' ListaParâmetros

DeclaraçãoEstrutura -> 'struct' Identificador '{' DeclaraçãoLista '}' ';'

Expressão -> ExpressãoAtribuição
           | Expressão ',' ExpressãoAtribuição

ExpressãoAtribuição -> Identificador '=' Expressão
                      | ExpressãoCondicional

ExpressãoCondicional -> ExpressãoLogica '?' Expressão ':' Expressão

ExpressãoLogica -> ExpressãoLogica '||' ExpressãoLogica
                 | ExpressãoLogica '&&' ExpressãoLogica
                 | ExpressãoRelacional

ExpressãoRelacional -> ExpressãoAditiva '>' ExpressãoAditiva
                      | ExpressãoAditiva '<' ExpressãoAditiva
                      | ExpressãoAditiva '>=' ExpressãoAditiva
                      | ExpressãoAditiva '<=' ExpressãoAditiva
                      | ExpressãoAditiva '==' ExpressãoAditiva
                      | ExpressãoAditiva '!=' ExpressãoAditiva

ExpressãoAditiva -> ExpressãoAditiva '+' Termo
                   | ExpressãoAditiva '-' Termo
                   | Termo

Termo -> Termo '*' Fator
        | Termo '/' Fator
        | Fator

Fator -> '(' Expressão ')'
        | Número
        | Identificador

Identificador -> [a-zA-Z_][a-zA-Z0-9_]*
Número -> [0-9]+

ListaVazia -> ε

Iremos montar a tabela de ações e 

"""
