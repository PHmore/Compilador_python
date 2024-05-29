# A gramática foi tirada do chat gpt, mas ainda apresenta erros provavelmente deverá ser feita na mão

# !Existem erros em relação a tabela e a indexação da pilha, estudar o funcionamento da pilha em uso no algoritmo

class SLRParser:
    def __init__(self, tabela):
        self.tabela = tabela

    def parse(self, tokens):
        stack = [0,0]  # Inicializa a pilha com o estado inicial
        entrada = tokens + ['$']  # Adiciona o símbolo de fim de entrada

        idx = 0  # Índice para percorrer os tokens de entrada

        while True:
            print('Pilha: ',stack);
            estado_atual = stack[-1]  # Estado atual no topo da pilha
            print('Estado atual: ', estado_atual)
            proximo_simbolo = entrada[idx]  # Próximo símbolo da entrada
            print('Próximo simbolo: ', proximo_simbolo)

            # Verifica se há uma ação para o estado atual e o próximo símbolo
            acao = self.tabela['Ação'][estado_atual].get(proximo_simbolo)

            if acao is None:
                # Se não há ação, a entrada é inválida para a gramática
                print("Erro: Entrada inválida para a gramática.")
                return False

            if acao == 'acc':
                # Aceitação: a análise foi bem-sucedida
                print("Análise sintática concluída com sucesso.")
                return True

            elif acao[0] == 'S':
                # Shift: empilha o próximo estado e avança na entrada
                novo_estado = int(acao[1:])
                stack.append(novo_estado)
                idx += 1

            elif acao[0] == 'R':
                # Reduce: aplica a redução utilizando a produção indicada
                num_producao = int(acao[1:])
                print('Número de produção: ',num_producao)
                producao = self.tabela['Productions'][num_producao]

                for _ in range(len(producao['right'])):
                    print('Tamanho da linha de produção: ',len(producao['right']))
                    print('Pilha para retirar: ',stack)
                    stack.pop()

                estado_atual = stack[-1]
                print('Estado atual: ',estado_atual)
                
                simbolo_nao_terminal = producao['left']
                print('Simbolo não terminal: ',simbolo_nao_terminal)

                proximo_estado = self.tabela['Goto'][estado_atual][simbolo_nao_terminal]
                print('Proximo estado: ',proximo_estado)
                stack.append(proximo_estado)

            else:
                print("Erro: Ação desconhecida.")
                return False


# Exemplo de utilização

# Tabela de análise SLR
tabela_slr = {
    'Estados': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    'Productions': {
        1: {'left': 'Programa', 'right': ['DeclaraçãoLista']},
        2: {'left': 'DeclaraçãoLista', 'right': ['Declaração', 'DeclaraçãoLista']},
        3: {'left': 'DeclaraçãoLista', 'right': []},  # Produção vazia para epsilon
        4: {'left': 'Declaração', 'right': ['DeclaraçãoVariável']},
        5: {'left': 'Declaração', 'right': ['DeclaraçãoFunção']},
        6: {'left': 'DeclaraçãoVariável', 'right': ['Tipo', 'Identificador', ';']},
        7: {'left': 'DeclaraçãoVariável', 'right': ['Tipo', 'Identificador', '[', 'Número', ']', ';']},
        8: {'left': 'DeclaraçãoFunção', 'right': ['Tipo', 'Identificador', '(', 'ListaParâmetros', ')', 'DeclaraçãoComposta']},
        9: {'left': 'Tipo', 'right': ['int']},
        10: {'left': 'Tipo', 'right': ['float']},
        11: {'left': 'Tipo', 'right': ['char']},
        12: {'left': 'Tipo', 'right': ['void']},
        13: {'left': 'ListaParâmetros', 'right': ['ListaVazia']},
        14: {'left': 'ListaParâmetros', 'right': ['Tipo', 'Identificador', ',', 'ListaParâmetros']},
        15: {'left': 'DeclaraçãoComposta', 'right': ['{', 'DeclaraçãoLista', '}']},
    },

    'Ação': {
        0: {'int': 'S3', 'float': 'S4', 'char': 'S5', 'void': 'S6', '$': 'acc'},
        1: {'$': 'acc'},
        2: {'int': 'S3', 'float': 'S4', 'char': 'S5', 'void': 'S6', '$': 'R3'},
        3: {'Identificador': 'S7',';':'R4'},
        4: {'Identificador': 'S8'},
        5: {'Identificador': 'S9'},
        6: {'Identificador': 'S10'},
        7: {';': 'R6'},
        8: {'(': 'S11'},
        9: {'(': 'S12'},
        10: {'(': 'S13'},
        11: {'Tipo': 'S14'},
        12: {'Tipo': 'S15'},
        13: {'Tipo': 'S16'},
        14: {'Identificador': 'S17'},
        15: {'Identificador': 'S18'},
        16: {'Identificador': 'S19'},
        17: {')': 'R7'},
        18: {')': 'R8'},
        19: {')': 'R9'},
    },
    'Goto': {
        0: {'DeclaraçãoLista': 1, 'Declaração': 2, 'DeclaraçãoVariável': 3, 'DeclaraçãoFunção': 4, 'Tipo': 5},
        1: {},
        2: {'DeclaraçãoLista': 6, 'Declaração': 7, 'DeclaraçãoVariável': 8, 'DeclaraçãoFunção': 9, 'Tipo': 10},
        3: {},
        4: {},
        5: {},
        6: {'Declaração': 11, 'DeclaraçãoVariável': 12, 'DeclaraçãoFunção': 13, 'Tipo': 14},
        7: {},
        8: {},
        9: {},
        10: {},
        11: {'DeclaraçãoLista': 15, 'Declaração': 16, 'DeclaraçãoVariável': 17, 'DeclaraçãoFunção': 18, 'Tipo': 19},
        12: {},
        13: {},
        14: {},
        15: {},
        16: {},
        17: {},
        18: {},
        19: {},
    }
}

# Tokens de entrada (simplificados para este exemplo)
tokens = ['int', 'Identificador', ';']

# Cria o analisador sintático SLR
parser = SLRParser(tabela_slr)

# Realiza a análise sintática
parser.parse(tokens)
