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
        # Estado : { token : ação }
        
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
        # Estado: {'Nterminal':ProxEstado,}
        
        0: {'E': 1,'T': 2,'F': 3},
        4: {'E': 8,'T': 2,'F': 3},
        6: {'T': 9,'F': 3},
        7: {'F': 10},
    },

    'Productions' : {
        1: {'left': 'PROGRAMA', 'right': ['SEÇÃOFUNÇÕES', 'PRINCIPAL']},
        2: {'left': 'SEÇÃOFUNÇÕES', 'right': ['LISTAFUNÇÕES']},
        3: {'left': 'SEÇÃOFUNÇÕES', 'right': ['ε']},
        4: {'left': 'LISTAFUNÇÕES', 'right': ['DECFUNÇÃO']},
        5: {'left': 'LISTAFUNÇÕES', 'right': ['LISTAFUNÇÕES', 'DECFUNÇÃO']},
        6: {'left': 'DECFUNÇÃO', 'right': ['TIPORETORNO', 'id', '(', 'PARÂMETROS', ')', 'BLOCO']},
        7: {'left': 'TIPORETORNO', 'right': ['TIPO']},
        8: {'left': 'TIPORETORNO', 'right': ['void']},
        9: {'left': 'TIPO', 'right': ['TIPOBASE', 'DIMENSÃO']},
        10: {'left': 'TIPOBASE', 'right': ['char']},
        11: {'left': 'TIPOBASE', 'right': ['float']},
        12: {'left': 'TIPOBASE', 'right': ['int']},
        13: {'left': 'TIPOBASE', 'right': ['boolean']},
        14: {'left': 'DIMENSÃO', 'right': ['DIMENSÃO', '[', 'num_int', ']']},
        15: {'left': 'DIMENSÃO', 'right': ['ε']},
        16: {'left': 'PARÂMETROS', 'right': ['LISTAPARÂMETROS']},
        17: {'left': 'PARÂMETROS', 'right': ['ε']},
        18: {'left': 'LISTAPARÂMETROS', 'right': ['TIPO', 'id']},
        19: {'left': 'LISTAPARÂMETROS', 'right': ['LISTAPARÂMETROS', ',', 'TIPO', 'id']},
        20: {'left': 'PRINCIPAL', 'right': ['main', '(', ')', 'BLOCO']},
        21: {'left': 'BLOCO', 'right': ['{', 'SEÇÃOVARIAVEIS', 'SEÇÃOCOMANDOS', '}']},
        22: {'left': 'SEÇÃOVARIAVEIS', 'right': ['LISTAVARIAVEIS']},
        23: {'left': 'SEÇÃOVARIAVEIS', 'right': ['ε']},
        24: {'left': 'LISTAVARIAVEIS', 'right': ['TIPO', 'LISTAID', ';']},
        25: {'left': 'LISTAVARIAVEIS', 'right': ['LISTAVARIAVEIS', 'TIPO', 'LISTAID', ';']},
        26: {'left': 'LISTAID', 'right': ['identificador']},
        27: {'left': 'LISTAID', 'right': ['LISTAID', ',', 'identificador']},
        28: {'left': 'SEÇÃOCOMANDOS', 'right': ['LISTACOMANDOS']},
        29: {'left': 'SEÇÃOCOMANDOS', 'right': ['ε']},
        30: {'left': 'LISTACOMANDOS', 'right': ['COMANDO']},
        31: {'left': 'LISTACOMANDOS', 'right': ['LISTACOMANDOS', 'COMANDO']},
        32: {'left': 'COMANDO', 'right': ['LEITURA']},
        33: {'left': 'COMANDO', 'right': ['ESCRITA']},
        34: {'left': 'COMANDO', 'right': ['ATRIBUIÇÃO']},
        35: {'left': 'COMANDO', 'right': ['FUNÇÃO']},
        36: {'left': 'COMANDO', 'right': ['SELEÇÃO']},
        37: {'left': 'COMANDO', 'right': ['ENQUANTO']},
        38: {'left': 'COMANDO', 'right': ['RETORNO']},
        39: {'left': 'LEITURA', 'right': ['scanf', '(', 'LISTATERMOLEITURA', ')', ';']},
        40: {'left': 'LISTATERMOLEITURA', 'right': ['TERMOLEITURA']},
        41: {'left': 'LISTATERMOLEITURA', 'right': ['LISTATERMOLEITURA', ',', 'TERMOLEITURA']},
        42: {'left': 'TERMOLEITURA', 'right': ['id', 'DIMENSAO2']},
        43: {'left': 'DIMENSAO2', 'right': ['DIMENSAO2', '[', 'EXPR_ADITIVA', ']']},
        44: {'left': 'DIMENSAO2', 'right': ['ε']},
        45: {'left': 'ESCRITA', 'right': ['println', '(', 'LISTATERMOESCRITA', ')', ';']},
        46: {'left': 'LISTATERMOESCRITA', 'right': ['TERMOESCRITA']},
        47: {'left': 'LISTATERMOESCRITA', 'right': ['LISTATERMOESCRITA', ',', 'TERMOESCRITA']},
        48: {'left': 'TERMOESCRITA', 'right': ['id', 'DIMENSAO2']},
        49: {'left': 'TERMOESCRITA', 'right': ['CONSTANTE']},
        50: {'left': 'TERMOESCRITA', 'right': ['texto']},
        51: {'left': 'SELEÇÃO', 'right': ['if', '(', 'EXPRESSÃO', ')', 'BLOCO', 'SENÃO']},
        52: {'left': 'SENÃO', 'right': ['else', 'BLOCO']},
        53: {'left': 'SENÃO', 'right': ['ε']},
        54: {'left': 'ENQUANTO', 'right': ['while', '(', 'EXPRESSÃO', ')', 'BLOCO']},
        55: {'left': 'ATRIBUIÇÃO', 'right': ['id', '=', 'COMPLEMENTO', ';']},
        56: {'left': 'COMPLEMENTO', 'right': ['EXPRESSÃO']},
        57: {'left': 'COMPLEMENTO', 'right': ['FUNÇÃO']},
        58: {'left': 'FUNÇÃO', 'right': ['func', 'id', '(', 'ARGUMENTOS', ')']},
        59: {'left': 'ARGUMENTOS', 'right': ['LISTAARGUMENTOS']},
        60: {'left': 'ARGUMENTOS', 'right': ['ε']},
        61: {'left': 'LISTAARGUMENTOS', 'right': ['EXPRESSÃO']},
        62: {'left': 'LISTAARGUMENTOS', 'right': ['LISTAARGUMENTOS', ',', 'EXPRESSÃO']},
        63: {'left': 'RETORNO', 'right': ['return', 'EXPRESSÃO', ';']},
        64: {'left': 'EXPRESSÃO', 'right': ['EXPR_OU']},
        65: {'left': 'EXPR_OU', 'right': ['EXPR_E']},
        66: {'left': 'EXPR_OU', 'right': ['EXPR_OU', '||', 'EXPR_E']},
        67: {'left': 'EXPR_E', 'right': ['EXPR_RELACIONAL']},
        68: {'left': 'EXPR_E', 'right': ['EXPR_E', '&&', 'EXPR_RELACIONAL']},
        69: {'left': 'EXPR_RELACIONAL', 'right': ['EXPR_ADITIVA']},
        70: {'left': 'EXPR_RELACIONAL', 'right': ['EXPR_ADITIVA', 'opRelacional', 'EXPR_ADITIVA']},
        71: {'left': 'EXPR_ADITIVA', 'right': ['EXPR_MULTIPLICATIVA']},
        72: {'left': 'EXPR_ADITIVA', 'right': ['EXPR_ADITIVA', 'OP_ADITIVO', 'EXPR_MULTIPLICATIVA']},
        73: {'left': 'OP_ADITIVO', 'right': ['+']},
        74: {'left': 'OP_ADITIVO', 'right': ['-']},
        75: {'left': 'EXPR_MULTIPLICATIVA', 'right': ['FATOR']},
        76: {'left': 'EXPR_MULTIPLICATIVA', 'right': ['EXPR_MULTIPLICATIVA', 'OP_MULTIPLICATIVO', 'FATOR']},
        77: {'left': 'OP_MULTIPLICATIVO', 'right': ['*']},
        78: {'left': 'OP_MULTIPLICATIVO', 'right': ['/']},
        79: {'left': 'OP_MULTIPLICATIVO', 'right': ['%']},
        80: {'left': 'FATOR', 'right': ['SINAL', 'identificador', 'DIMENSAO2']},
        81: {'left': 'FATOR', 'right': ['SINAL', 'CONSTANTE']},
        82: {'left': 'FATOR', 'right': ['texto']},
        83: {'left': 'FATOR', 'right': ['!', 'FATOR']},
        84: {'left': 'FATOR', 'right': ['(', 'EXPRESSÃO', ')']},
        85: {'left': 'CONSTANTE', 'right': ['num_int']},
        86: {'left': 'CONSTANTE', 'right': ['num_dec']},
        87: {'left': 'SINAL', 'right': ['+']},
        88: {'left': 'SINAL', 'right': ['-']},
        89: {'left': 'SINAL', 'right': ['ε']}
        }

}

# Tokens de entrada (simplificados para este exemplo)
tokens = ['int', 'x',';']

# Cria o analisador sintático SLR
parser = SLRParser(tabela_slr)

# Realiza a análise sintática
parser.parse(tokens)
