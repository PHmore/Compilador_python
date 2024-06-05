import makeTablenew
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


import graphviz

class SLRParser:
    def __init__(self, tabela):
        self.tabela = tabela
        self.tree = None

    def parse(self, tokens):
        stack = ['$', 0]  # Inicializa a pilha com o estado inicial
        entrada = tokens + ['$']  # Adiciona o símbolo de fim de entrada
        tree_stack = []  # Pilha para construção da árvore sintática

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
                self.tree = tree_stack[-1] if tree_stack else None
                return True

            elif acao.startswith('s'):
                # Shift: empilha o próximo estado e avança na entrada
                novo_estado = int(acao[1:])
                stack.append(proximo_simbolo)
                stack.append(novo_estado)
                tree_stack.append((proximo_simbolo, []))  # Adiciona o símbolo à pilha da árvore
                idx += 1

            elif acao.startswith('r'):
                # Reduce: aplica a redução utilizando a produção indicada
                num_producao = int(acao[1:])
                print('Número de produção: ', num_producao)
                producao = self.tabela['Produção'][num_producao]
                print('Produção: ', producao)

                # Remove da pilha o número de símbolos da produção à direita vezes 2 pq estamos colocando os estados na pilha também, se não for produção vazia
                tamanho_direita = len(producao['right']) * 2
                print('Tamanho da linha de produção: ', tamanho_direita / 2, ' Tamanho a ser removido: ', tamanho_direita)
                if tamanho_direita > 0:
                    if len(stack) < tamanho_direita:
                        print("Erro: Tentativa de remover mais elementos da pilha do que disponíveis.")
                        return False
                    children = []
                    for _ in range(tamanho_direita):
                        print('Pilha para retirar: ', stack)
                        if len(stack) % 2 == 0:  # Remove e coleta os símbolos
                            children.append(tree_stack.pop())
                        stack.pop()

                    children.reverse()
                    tree_stack.append((producao['left'], children))  # Adiciona a redução à árvore

                if not stack:
                    print("Erro: Pilha vazia após redução.")
                    return False

                print('Pilha após redução: ', stack)

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

    def build_tree_graph(self, tree, dot=None):
        if dot is None:
            dot = graphviz.Digraph()

        if isinstance(tree, tuple):
            label, children = tree
            node_id = str(id(tree))
            dot.node(node_id, label)
            for child in children:
                child_id = self.build_tree_graph(child, dot)
                dot.edge(node_id, child_id)
            return node_id
        else:
            node_id = str(id(tree))
            dot.node(node_id, tree)
            return node_id

    def save_tree_image(self, filename='tree'):
        if self.tree is None:
            print("Erro: Nenhuma árvore sintática foi gerada.")
            return

        dot = graphviz.Digraph()
        self.build_tree_graph(self.tree, dot)
        dot.render(filename, format='png')
        print(f"Árvore sintática salva como {filename}.png")



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
    'LISTA_ID': [['IDENTIFIER'], ['LISTA_ID', ',', 'IDENTIFIER']],
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
    'FATOR': [['SINAL', 'IDENTIFIER', 'DIMENSAO2'],['SINAL' ,'CONSTANTE'], ['texto'],['FATOR'],['(','EXPRESSÃO',')']],
    'SINAL': [['+'],['-'],['ε']],
}

"""
Léxico

self.accepting = {1: 'IDENTIFIER', 2: 'INTEGER', 4: 'IDENTIFIER_ERROR', 5: 'FLOAT', 6: '+', 7: '-', 8: '*',
                          9: '/', 10: '==', 11: '=', 12: '<', 13: '>', 14: '(', 15: ')', 16: '{', 17: '}', 18: '[',
                          19: ']', 20: ';', 21: ',', 22: '.', 24: 'LITERAL', 25: '<=', 26: '>=', 28: '!=', 29: '#',
                          31: 'COMMENT', 32: 'COMMENT_ERROR', 34: 'LIBRARY', 35: 'LIBRARY_ERROR', 36: '%', 37: '\\n',
                          38: '\\t', 41: 'CHAR', 42: 'CHAR_ERROR', 43: '&', 45: 'TYPE'
                          }
        self.reserved_words = ['if', 'else', 'for', 'while', 'int', 'float', 'double', 'char', 'return', 'main', 'void',
                               'switch', 'case', 'break', 'continue', 'typedef', 'struct', 'union', 'enum', 'sizeof',
                               'static', 'const', 'volatile', 'extern', 'register', 'auto', 'signed', 'unsigned', 'do',
                               'short', 'long', 'printf', 'define', 'include', 'scanf']
Exemplo:
                           

"""

productions = {
    'S': [['PROGRAMA']],
    'PROGRAMA': [['LIBS','DECLARACOES']],
    'DECLARACOES': [['DECVAR','PRINCIPAL']],
    # 'DECLARACOES': [['DECLARACAO','DECLARACOES',],['DECLARACAO',],],
    # 'DECLARACAO':[['DECFUN'],['DECVAR'],],
    'LIBS':[['LIB','LIBS'],['LIB']],
    'LIB':[['#','include','LIBRARY']],
    'DECVAR': [['TIPO','IDENTIFIER',';']],
    'PRINCIPAL': [['TIPORET','main','(','PARAMETRO',')','BLOCO']],
    'DECFUN': [['TIPORET','IDENTIFIER','(','PARAMETRO',')','BLOCO']],
    'PARAMETRO':[['IDENTIFIER','(','PARAMETRO',')'],['IDENTIFIER'],['void']],
    'TIPORET':[['int'],['char'],['float'],['void']],
    'TIPO':[['int'],['char'],['float']],
    'IF':[['if','(','EXPBOOL',')','BLOCOIF']],
    'BLOCO': [['{','CODIGOS','}']],
    'BLOCOIF': [['{','CODIGOSIF','}','else','{','KEYPRINT','}']],
    'CODIGOS': [['KEYWORDS'],['FATOR','RETORNO'],['ATT','RETORNO']],
    'CODIGOSIF': [['ATTSOMA']],
    'ATTSOMA': [['ATT','=','NUM',';',]],
    'ATT':[['IDENTIFIER','+'],],
    'RETORNO': [['return','FATOR',';']],
    'KEYWORDS':[['IF'],['while'],['for'],['printf','(',')']],
    'KEYPRINT':[['printf','(','LITERAL',')',';']],
    'EXPBOOL':[['IDENTIFIER','OPBOOL','INTEGER'],['INTEGER','OPBOOL','INTEGER']],
    'FATOR':[['IDENTIFIER','OPERATOR','INTEGER']],
    'NUM':[['INTEGER'],['IDENTIFIER']],
    'OPERATOR':[['+'],['-'],['*'],['/']],
    'UNIOPERATOR':[['++'],['--']],
    'OPBOOL':[['=='],['<='],['>='],['!=']],
    }

tabela_slr = makeTablenew.getTabela(productions)

tokens = ['#','include','LIBRARY','int','id','(',')','{','printf','}']
tokens1= ['#','include','LIBRARY','int','id',';']
tokens2= ['#','include','LIBRARY','int','id',';','int','id','(',')','{','printf','}']

token_ex = ['#','include','LIBRARY','\n','\n','\n','int','IDENTIFIER',';','\n','\n','void','main','(','void',')','{','\n','\n','if','(','INTEGER','==','INTEGER',')','\n','{','\n','IDENTIFIER','+','=','INTEGER',';','\n','}','else','\n','{','\n','printf','(','LITERAL',')',';','\n','}','\n','}','\n']
    
    
    
    
    
   
   
while '\n' in token_ex:
    token_ex.remove('\n')

print(token_ex)

# Cria o analisador sintático SLR
parser = SLRParser(tabela_slr)

# Realiza a análise sintática
# parser.parse(tokens)
# parser.parse(tokens1)
# parser.parse(tokens2)
if parser.parse(token_ex):
    parser.save_tree_image('tree')
