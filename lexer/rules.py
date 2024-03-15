#obs: devemos usar um autômato deterministico para diminuir o gasto computacional segue o link do video que explica um pouco sobre: https://youtu.be/mCwQoM8KaZk
#palavras chave em python: https://www.delftstack.com/pt/tutorial/python-3-basic-tutorial/keywords-and-identifiers/

# Devemos primeiramente estudar as regras de sintaxé do python e classifica-las bem como criar o regex correspondente para cada uma

# Rules:

# Não podemos começar um indentificador com número ou caracter não alfabetico;

# Não podemos usar palavras reservadas

# Talvez usaremos orientação a objetos para criar as funções de análise

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
    pattern = re.compile('^[A-Za-z]*')
    return re.findall(pattern,expression)

expression = "Helloworld"
print(ID(expression))
