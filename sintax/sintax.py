import makeTablenew

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

token_ex = ['#','include','LIBRARY','\n','\n','\n','int','IDENTIFIER',';','\n','\n','void','main','(','void',')','{','\n','\n','if','(','INTEGER','==','INTEGER',')','\n','{','\n','IDENTIFIER','+','=','INTEGER',';','\n','}','else','\n','{','\n','printf','(','LITERAL',')',';','\n','}','\n','}','\n']
    
while '\n' in token_ex:
    token_ex.remove('\n')

print(token_ex)

parser = SLRParser(tabela_slr)

if parser.parse(token_ex):
    parser.save_tree_image('tree')
