#obs: devemos usar um autômato deterministico para diminuir o gasto computacional segue o link do video que explica um pouco sobre: https://youtu.be/mCwQoM8KaZk
#palavras chave em python: https://www.delftstack.com/pt/tutorial/python-3-basic-tutorial/keywords-and-identifiers/

# Devemos primeiramente estudar as regras de sintaxé do python e classifica-las bem como criar o regex correspondente para cada uma

### Definição do autômato
# devemos começar definindo as 5 tuplas do autômato isto é
# S = conjunto de estados finito no reconhecedor junto com o estado de erro
# Z(esquisito) = alfabeto finido usado pelo reconhecedor
# ç(simbolo nulo) = função de transição do reconhecedor. Ela mapeia cada estado s pertencente a S e cada caracter c pertencente ao alfabeto a algum estado seguinte
#s_0 pertence a S e é o estado inicial designado
# S_a é o conjunto de estados de aceitação, ou seja está contido em S. Cada estado S_a aparece como um duplo círculo no diagrama de transição. Ou seja são estados finais


# Importação do regex
import re

# Aqui já temos um pensamento para podermos descartar expressões que não começam com caracteres alfabeticos
# Deve se pensar se salvaremos a string toda e comparamos as palavras reservadas ou usarmos um pensamento de automato e verificamos se a leitura de letra por letra resultam em uma palavra reservada
def ID(expression):
    # A frase deve estar do ínicio até o fim da linha caso contenha algum caracter não tratado não dará match
    pattern = re.compile('/^[A-Za-z_]+$/')
    result = re.findall(pattern,expression)
    if result:
        print('It is a ID')
    else:
        print('Erro')
    return result

# Aqui mostramos os diferentes tipos de pattern mudando apenas as ()
# Observação se usamos () é find é separado se usarmos [] é feito uma união ao que já foi encontrado
# Neste caso os números são lidos com . e ,
def NUMBER(expression):
    patternA = re.compile("^([0-9])*(.|,)?([0-9])*$")
    patternB = re.compile("(^[0-9]*)(.|,?)([0-9]*)$")
    patternC = re.compile("^[0-9]*.|,?[0-9]*$")
    patternD = re.compile("^/d*[.|,]?/d*$")
    patternE = re.compile("^[0-9]*[.|,]?[0-9]*$")
    result = re.findall(patternE,expression)
    if result:
        print('It is a number')
    else:
        print('Erro')
    return result



# Temos um problema pois o _ não é lido
expression = "h_eLl_o_Wo0rld"
print(ID(expression))
expression = "123.56"
print(NUMBER(expression))
expression = "#expression coment"

# Rules:

# Não podemos começar um indentificador com número ou caracter não alfabetico;

# Não podemos usar palavras reservadas

# Talvez usaremos orientação a objetos para criar as funções de análise
