import makeTable


# Primeiro devemos criar as tabelas

# Faremos a coleção canônica de itens


# s1 significa empilhar e se mover para o estado 1

# r1 significa reduzir pela regra 1 
# Para apagar na pilha sempre o dobro do lado direito da redução
# Após feita a redução é lido o item reduzido apartir do último estado registrado na pilha

'''
S'->S
S->(L)|a
L->L,S|S

Item 0
S'->.S
S->.(L)
L->.L,S|S
'''


class SLRParser:
    def __init__(self, tabela):
        self.tabela = tabela

    def parse(self, tokens):
        stack = ['$',0]  # Inicializa a pilha com o estado inicial
        entrada = tokens + ['$']  # Adiciona o símbolo de fim de entrada

        idx = 0  # Índice para percorrer os tokens de entrada

        while True:
            if not stack:
                print("Erro: Pilha vazia.")
                return False

            print('\nPilha: ', stack)

            estado_atual = stack[-1]  # Estado atual no topo da pilha
            print('Estado atual: ', estado_atual)

            proximo_simbolo = entrada[idx]  # Próximo símbolo da entrada
            print('Próximo simbolo (lookahead): ', proximo_simbolo)

            # Verifica se há uma ação para o estado atual e o próximo símbolo
            acao = self.tabela['Ação'][estado_atual].get(proximo_simbolo)

            print('Ação: ', acao)

            if acao is None:
                # Se não há ação, a entrada é inválida para a gramática
                print("Erro: Entrada inválida para a gramática.")
                return False

            if acao == 'acc':
                # Aceitação: a análise foi bem-sucedida
                print("Análise sintática concluída com sucesso.")
                return True

            elif acao.startswith('s'):
                # Shift: empilha o próximo estado e avança na entrada
                novo_estado = int(acao[1:])
                stack.append(proximo_simbolo)
                stack.append(novo_estado)
                idx += 1

            elif acao.startswith('r'):
                # Reduce: aplica a redução utilizando a produção indicada
                num_producao = int(acao[1:])
                print('Número de produção: ', num_producao)
                producao = self.tabela['Produção'][num_producao]
                print('Produção: ', producao)

                # Remove da pilha o número de símbolos da produção à direita vezes 2 pq estamos colocando os estados na pilha também, se não for produção vazia
                tamanho_direita = len(producao['right']) * 2
                print('Tamanho da linha de produção: ', tamanho_direita/2,' Tamanho a ser removido: ',tamanho_direita)
                if tamanho_direita > 0:
                    if len(stack) < tamanho_direita:
                        print("Erro: Tentativa de remover mais elementos da pilha do que disponíveis.")
                        return False
                    for _ in range(tamanho_direita):
                        print('Pilha para retirar: ', stack)
                        stack.pop()

                if not stack:
                    print("Erro: Pilha vazia após redução.")
                    return False
                
                print('Pilha após redução: ',stack)

                estado_atual = stack[-1]
                print('Estado atual após redução: ', estado_atual)

                simbolo_nao_terminal = producao['left']
                print('Simbolo não terminal: ', simbolo_nao_terminal)

                proximo_estado = self.tabela['Goto'][estado_atual].get(simbolo_nao_terminal)
                print('Próximo estado: ', proximo_estado)

                # Adiciona o simbolo não terminal a pilha e o estado atual deve continuar sendo um número
                stack.append(simbolo_nao_terminal)

                if proximo_estado is None:
                    print("Erro: Estado de goto não encontrado.")
                    return False

                stack.append(proximo_estado)
                print('Pilha após redução: ', stack)

            else:
                print("Erro: Ação desconhecida.")
                return False



# Exemplo de utilização

# Tabela de análise SLR
# tabela_slr = {'Ação': {0: {'int': 's2'},
#           1: {'$': 'r2', ';': 'r2', 'id': 'r2', 'int': 'r2'},
#           2: {'id': 's4'},
#           3: {'$': 'acc'},
#           4: {';': 's5'},
#           5: {'$': 'r3', ';': 'r3', 'id': 'r3', 'int': 'r3'}},
#  'Goto': {0: {'DECVAR': 1, 'PROGRAMA': 3}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}},
#  'Produção': {1: {'left': 'S', 'right': ['PROGRAMA']},
#               2: {'left': 'PROGRAMA', 'right': ['DECVAR']},
#               3: {'left': 'DECVAR', 'right': ['int', 'id', ';']}}}
"""
productions = {
    'S': [['PROGRAMA']],
    'PROGRAMA': [['SEÇÃO_FUNÇÕES', 'PRINCIPAL']],
    'SEÇÃO_FUNÇÕES': [['LISTA_FUNÇÕES'], ['ε']],
    'LISTA_FUNÇÕES': [['DEC_FUNÇÃO'], ['LISTA_FUNÇÕES', 'DEC_FUNÇÃO']],
    'DEC_FUNÇÃO': [['TIPO_RETORNO', 'id', '(', 'PARÂMETROS', ')', 'BLOCO']],
    'TIPO_RETORNO': [['TIPO'], ['void']],
    'TIPO': [['TIPO_BASE', 'DIMENSÃO']],
    'TIPO_BASE': [['char'], ['float'], ['int'], ['boolean']],
    'DIMENSÃO': [['DIMENSÃO', '[', 'num_int', ']'], ['ε']],
    'PARÂMETROS': [['LISTA_PARÂMETROS'], ['ε']],
    'LISTA_PARÂMETROS': [['TIPO', 'id'], ['LISTA_PARÂMETROS', ',', 'TIPO', 'id']],
    'PRINCIPAL': [['main', '(', ')', 'BLOCO']],
    'BLOCO': [['{', 'SEÇÃO_VARIAVEIS', 'SEÇÃO_COMANDOS', '}']],
    'SEÇÃO_VARIAVEIS': [['LISTA_VARIAVEIS'], ['ε']],
    'LISTA_VARIAVEIS': [['TIPO', 'LISTA_ID', ';'], ['LISTA_VARIAVEIS', 'TIPO', 'LISTA_ID', ';']],
    'LISTA_ID': [['identificador'], ['LISTA_ID', ',', 'identificador']],
    'SEÇÃO_COMANDOS': [['LISTA_COMANDOS'], ['ε']],
    'LISTA_COMANDOS': [['COMANDO'], ['LISTA_COMANDOS', 'COMANDO']],
    'COMANDO': [['LEITURA'], ['ESCRITA'], ['ATRIBUIÇÃO'], ['FUNÇÃO'], ['SELEÇÃO'], ['ENQUANTO'], ['RETORNO']],
    'LEITURA': [['scanf', '(', 'LISTA_TERMO_LEITURA', ')', ';']],
    'LISTA_TERMO_LEITURA': [['TERMO_LEITURA'], ['LISTA_TERMO_LEITURA', ',', 'TERMO_LEITURA']],
    'TERMO_LEITURA': [['id', 'DIMENSAO2']],
    'DIMENSAO2': [['DIMENSAO2', '[', 'EXPR_ADITIVA', ']', 'ε']],
    'ESCRITA': [['println', '(', 'LISTA_TERMO_ESCRITA', ')', ';']],
    'LISTA_TERMO_ESCRITA': [['TERMO_ESCRITA'], ['LISTA_TERMO_ESCRITA', ',', 'TERMO_ESCRITA']],
    'TERMO_ESCRITA': [['id', 'DIMENSAO2'], ['CONSTANTE'], ['texto']],
    'SELEÇÃO': [['if', '(', 'EXPRESSÃO', ')', 'BLOCO', 'SENÃO']],
    'SENÃO': [['else', 'BLOCO'], ['ε']],
    'ENQUANTO': [['while', '(', 'EXPRESSÃO', ')', 'BLOCO']],
    'ATRIBUIÇÃO': [['id', '=', 'COMPLEMENTO', ';']],
    'COMPLEMENTO': [['EXPRESSÃO'], ['FUNÇÃO']],
    'FUNÇÃO': [['func', 'id', '(', 'ARGUMENTOS', ')']],
    'ARGUMENTOS': [['LISTA_ARGUMENTOS'], ['ε']],
    'LISTA_ARGUMENTOS': [['EXPRESSÃO'], ['LISTA_ARGUMENTOS', ',', 'EXPRESSÃO']],
    'RETORNO': [['return', 'EXPRESSÃO', ';']],
    'EXPRESSÃO': [['EXPR_OU']],
    'EXPR_OU': [['EXPR_E'], ['EXPR_OU', '||', 'EXPR_E']],
    'EXPR_E': [['EXPR_RELACIONAL'], ['EXPR_E', '&&', 'EXPR_RELACIONAL']],
    'EXPR_RELACIONAL': [['EXPR_ADITIVA'], ['EXPR_ADITIVA', 'opRelacional', 'EXPR_ADITIVA']],
    'EXPR_ADITIVA': [['EXPR_MULTIPLICATIVA'], ['EXPR_ADITIVA', 'OP_ADITIVO', 'EXPR_MULTIPLICATIVA']],
    'OP_ADITIVO': [['+'], ['-']],
    'EXPR_MULTIPLICATIVA': [['FATOR'], ['EXPR_MULTIPLICATIVA', 'OP_MULTIPLICATIVO', 'FATOR']],
    'OP_MULTIPLICATIVO': [['*'], ['/'], ['%']],
    'FATOR': [['SINAL', 'identificador', 'DIMENSAO2'],['SINAL' ,'CONSTANTE'], ['texto'],['FATOR'],['(','EXPRESSÃO',')']],
    'SINAL': [['+'],['-'],['ε']],
}
"""

productions = {
    'S': [['PROGRAMA']],
    'PROGRAMA': [['DECVAR'],['DECFUN']],
    'DECVAR': [['DEC',';']],
    'DECFUN': [['DEC','(',')','BLOCO']],
    'BLOCO': [['{','}']],
    'DEC':[['int','id']]
    }

tabela_slr = makeTable.getTabela(productions)
print('\nA tabela foi instaciada:\n',tabela_slr)

# Tokens de entrada (simplificados para este exemplo)
# tokens = ['int','identificador', '(', ')', '{', 'int', 'id', ';', 'float', 'id', '[', 'num_int', ']', ';', 'char', 'id', ';', 'boolean', 'id', '=', 'true', ';', 'id', '=', 'num_int', ';', 'id', '=', 'texto', ';', 'if', '(', 'id', '>', 'num_int', ')', '{', 'id', '[', 'num_int', ']', '=', 'num_dec', ';', '}', 'else', '{', 'id', '[', 'num_int', ']', '=', 'num_dec', ';', '}', 'while', '(', 'id', ')', '{', 'id', '--', ';', '}', 'return', 'num_int', ';', '}']
tokens = ['int','id','(',')','{','}']


# Cria o analisador sintático SLR
parser = SLRParser(tabela_slr)

# Realiza a análise sintática
parser.parse(tokens)
