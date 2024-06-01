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

            elif acao.startswith('S'):
                # Shift: empilha o próximo estado e avança na entrada
                novo_estado = int(acao[1:])
                stack.append(proximo_simbolo)
                stack.append(novo_estado)
                idx += 1

            elif acao.startswith('R'):
                # Reduce: aplica a redução utilizando a produção indicada
                num_producao = int(acao[1:])
                print('Número de produção: ', num_producao)
                producao = self.tabela['Productions'][num_producao]
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
tabela_slr = {
    'productions ': {
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
    },

    'action_table' : {
        0: {'SEÇÃOFUNÇÕES': 'S1', 'PRINCIPAL': 'S2', 'PROGRAMA': 'G1'},
        1: {'LISTAFUNÇÕES': 'S3', 'ε': 'S4'},
        2: {'main': 'S5'},
        3: {'DECFUNÇÃO': 'S6'},
        4: {'$': 'ACCEPT'},
        5: {'(': 'S7'},
        6: {'TIPORETORNO': 'S8'},
        7: {'LISTAPARÂMETROS': 'S9', 'ε': 'S10'},
        8: {'TIPO': 'S11', 'void': 'S12'},
        9: {'id': 'S13'},
        10: {')': 'R17'},
        11: {'TIPOBASE': 'S14'},
        12: {'(': 'S15'},
        13: {'{': 'S16'},
        14: {'char': 'S17', 'float': 'S18', 'int': 'S19', 'boolean': 'S20'},
        15: {')': 'R60'},
        16: {'SEÇÃOVARIAVEIS': 'S21', 'SEÇÃOCOMANDOS': 'S22'},
        17: {'LISTAVARIAVEIS': 'S23', 'ε': 'S24'},
        18: {'{': 'S25'},
        19: {'main': 'S26'},
        20: {'}': 'R29'},
        21: {'TIPO': 'S27', 'ε': 'S28'},
        22: {'LISTACOMANDOS': 'S29', 'ε': 'S30'},
        23: {'identificador': 'S31'},
        24: {'}': 'R22'},
        25: {'TIPO': 'S32'},
        26: {'identificador': 'S33'},
        27: {'DECFUNÇÃO': 'S34'},
        28: {'ε': 'R31'}
    },

    'goto_table' : {
        0: {'SEÇÃOFUNÇÕES': 1, 'PRINCIPAL': 2, 'PROGRAMA': 1},
        1: {'LISTAFUNÇÕES': 3, 'ε': 4},
        2: {'main': 5},
        3: {'DECFUNÇÃO': 6},
        4: {'$': 'ACCEPT'},
        5: {'(': 7},
        6: {'TIPORETORNO': 8},
        7: {'LISTAPARÂMETROS': 9, 'ε': 10},
        8: {'TIPO': 11, 'void': 12},
        9: {'id': 13},
        10: {')': 'R17'},
        11: {'TIPOBASE': 14},
        12: {'(': 15},
        13: {'{': 16},
        14: {'char': 17, 'float': 18, 'int': 19, 'boolean': 20},
        15: {')': 'R60'},
        16: {'SEÇÃOVARIAVEIS': 21, 'SEÇÃOCOMANDOS': 22},
        17: {'LISTAVARIAVEIS': 23, 'ε': 24},
        18: {'{': 25},
        19: {'main': 26},
        20: {'}': 'R29'},
        21: {'TIPO': 27, 'ε': 28},
        22: {'LISTACOMANDOS': 29, 'ε': 30},
        23: {'identificador': 31},
        24: {'}': 'R22'},
        25: {'TIPO': 32},
        26: {'identificador': 33},
        27: {'DECFUNÇÃO': 34},
        28: {'ε': 'R31'}
    }

}

# Tokens de entrada (simplificados para este exemplo)
tokens = ['int','identificador', ';']

# Cria o analisador sintático SLR
parser = SLRParser(tabela_slr)

# Realiza a análise sintática
parser.parse(tokens)
