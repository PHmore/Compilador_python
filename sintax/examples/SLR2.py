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
            print('Próximo simbolo: ', proximo_simbolo)

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
                producao = self.tabela['Productions'][num_producao]
                print('Produção: ', producao)

                # Remove da pilha o número de símbolos da produção à direita, se não for produção vazia
                tamanho_direita = len(producao['right'])
                print('Tamanho da linha de produção: ', tamanho_direita)
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

                estado_atual = stack[-1]
                print('Estado atual após redução: ', estado_atual)

                simbolo_nao_terminal = producao['left']
                print('Simbolo não terminal: ', simbolo_nao_terminal)

                proximo_estado = self.tabela['Goto'][estado_atual].get(simbolo_nao_terminal)
                print('Próximo estado: ', proximo_estado)

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
tabela_slr = {
    'Ação': {
        
        0: {'id': 's5','(':'s4',},
        1: {'+': 's6','$':'acc',},
        2: {'+': 'r2','*':'s7',')':'r2','$':'r2',},
        3: {'+': 'r4','*':'r4',')':'r4','$':'r4',},
        4: {'id': 's5','(':'s4',},
        5: {'+': 'r6','*':'r6',')':'r6','$':'r6',},
        6: {'id': 's5','(':'s4',},
        7: {'id': 's5','(':'s4',},
        8: {'+': 's6',')':'s11',},
        9: {'+': 'r1','*':'s7',')':'r1','$':'r1',},
        10: {'+': 'r3','*':'r3',')':'r3','$':'r3',},
        11: {'+': 'r5','*':'r5',')':'r5','$':'r5',},
    },

    'Goto': {
        
        0: {'E': 1,'T': 2,'F': 3},
        4: {'E': 8,'T': 2,'F': 3},
        6: {'T': 9,'F': 3},
        7: {'F': 10},
    },
    'Reduce':
    {
        'S':'_S'
    }
}

# Tokens de entrada (simplificados para este exemplo)
tokens = ['int', 'x',';']

# Cria o analisador sintático SLR
parser = SLRParser(tabela_slr)

# Realiza a análise sintática
parser.parse(tokens)
