# Aparentemente vai ser necessário fazer várias funções para a indentificação da gramática






# A analise será feita de forma as descendentes pois são na teoria mais simples de se implementar doq os ascendentes

# Para fazermos um analisador sintático é necessário utilizar regras de produção

# Devemos separar em grupos como Cabeça, Final, First e Follow
# Cabeça é o primeiro caracter a direita da linha de produção sendo terminal ou não terminal
# Final é o último caracter a direta da linha de produção sendo terminal ou não terminal
# First é o primeiro caracter a direta da linha de produção sendo terminal caso seja vazio é feito uma união com o first do próximo não teminal

# sendo A um não terminal o Follow é o conjunto de terminais que aparecem a frente imediatamente a frente do mesmo, 
# caso haja (vazio) é folloW de A é toda a linha de produção que A está inserido

"""
Exemplo 


A -> BC
B -> a|b|(vazio)
C -> c

obs: cada | apresenta um para o first

firstA = firstB (união) firstC = a,b,c,(vazio)
followA = firstC = c


Exemplo de derivação:

Gramatica:
S -> AG (1)
A -> aDF (2)
F -> f (3) |fR (5) |(vazio) (6)
G -> g (7)

Derivação:
S -> (iniciou derivação)
AG -> (Aplicou regra 1)
aDFG -> (aplicou regra 2)
aD G -> (aplicou a regra 6)

onde follow de D é igua follow de A

Construtor função:

sendo isto F = função, T = Tipo, I = indentificador, .. = Qlq código dentro
F -> T I ( T ) { .. }

"""


"""
Claro! Vou mostrar um exemplo bem simples de um analisador sintático descendente recursivo para uma pequena parte da linguagem C, que lida apenas com declarações de variáveis simples.

Vamos considerar a seguinte gramática simplificada:

```
DeclaraçãoVariável -> Tipo Identificador ;
Tipo -> int | float | char
Identificador -> [a-zA-Z][a-zA-Z0-9_]*
```

E aqui está como você pode implementar isso em pseudocódigo:

```python

"""
# Função principal do analisador sintático
def analisador_sintatico(codigo_fonte):

    # Feito com analisador léxico
    tokens = analisador_lexico(codigo_fonte)
    indice_token_atual = 0
    while indice_token_atual < len(tokens):
        # Ver qual o valor do token
        if tokens[indice_token_atual] == 'int' or tokens[indice_token_atual] == 'float' or tokens[indice_token_atual] == 'char':
            indice_token_atual = analisa_declaracao_variavel(tokens, indice_token_atual)
        else:
            # Se não for uma declaração de variável, emite um erro
            emite_erro("Esperava uma declaração de variável", tokens[indice_token_atual])
            break

# Função para analisar uma declaração de variável
def analisa_declaracao_variavel(tokens, indice_atual):
    tipo = tokens[indice_atual]  # O primeiro token deve ser o tipo da variável
    if tipo not in ['int', 'float', 'char']:
        emite_erro("Tipo de variável inválido", tipo)
        return indice_atual

    indice_atual += 1  # Avança para o próximo token
    if indice_atual < len(tokens) and tokens[indice_atual].isalpha():
        # Se o próximo token for um identificador válido
        identificador = tokens[indice_atual]
        if indice_atual + 1 < len(tokens) and tokens[indice_atual + 1] == ';':
            # Se o token seguinte for um ponto e vírgula, a declaração está completa
            print("Declaração de variável válida:", tipo, identificador)
            return indice_atual + 2  # Avança para o token após o ponto e vírgula
        else:
            emite_erro("Esperava um ponto e vírgula", tokens[indice_atual + 1])
            return indice_atual + 1
    else:
        emite_erro("Identificador inválido", tokens[indice_atual])
        return indice_atual

# Função para analisar erros
def emite_erro(mensagem, token):
    print("Erro:", mensagem, "- Token encontrado:", token)

# Função de exemplo para análise léxica (simplificada)
def analisador_lexico(codigo_fonte):
    return codigo_fonte.split()

# Exemplo de código-fonte
codigo_fonte = "int x;"
analisador_sintatico(codigo_fonte)

"""
```

Neste exemplo:

- `analisador_sintatico()` é a função principal que chama outras funções para analisar diferentes partes do código-fonte.
- `analisa_declaracao_variavel()` analisa declarações de variáveis, verificando se o tipo e o identificador estão corretos.
- `emite_erro()` é uma função auxiliar para imprimir mensagens de erro.
- `analisador_lexico()` é uma função de exemplo para análise léxica, que simplesmente divide o código-fonte em palavras.

Este é um exemplo bastante simplificado, mas ilustra os princípios básicos de um analisador sintático descendente recursivo."""