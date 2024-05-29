# Exemplo gerado pelo chatGPT de analisador sintático utilizando o LR(0)

# Definição da gramática LR(0) para expressões aritméticas simples em C
grammar = {
    'E': ['E + T', 'T'],
    'T': ['T * F', 'F'],
    'F': ['( E )', 'id']
}

# Construção do conjunto de itens LR(0)
def lr0_items(grammar):
    items = {}
    for nonterminal, productions in grammar.items():
        for production in productions:
            for i in range(len(production) + 1):
                items[(nonterminal, i)] = production[:i] + ['.'] + production[i:]
    return items

# Função para calcular o fecho de um conjunto de itens LR(0)
def closure_lr0(items, grammar):
    closure = set(items)
    while True:
        new_items = set()
        for item in closure:
            dot_index = item.index('.')
            if dot_index < len(item) - 1 and item[dot_index + 1] in grammar:
                for production in grammar[item[dot_index + 1]]:
                    new_item = (item[dot_index + 1], 0) + tuple(['.'] + production)
                    if new_item not in closure:
                        new_items.add(new_item)
        if not new_items:
            break
        closure.update(new_items)
    return closure

# Função para calcular o fecho de um conjunto de itens LR(0) após a leitura de um símbolo
def goto_lr0(items, symbol):
    goto = set()
    for item in items:
        dot_index = item.index('.')
        if dot_index < len(item) - 1 and item[dot_index + 1] == symbol:
            new_item = item[:dot_index] + (symbol, '.') + item[dot_index + 2:]
            goto.add(new_item)
    return closure_lr0(goto, grammar)

# Construção da tabela de análise LR(0)
def build_lr0_table(grammar):
    items = lr0_items(grammar)
    table = {}
    for i, item in enumerate(items):
        if item[1] == len(item) - 1:
            for j, symbol in enumerate(item):
                if symbol in grammar:
                    table[(i, symbol)] = ('REDUCE', item[:j])
        else:
            next_symbol = item[item.index('.') + 1]
            goto = goto_lr0({item}, next_symbol)
            for j, new_item in enumerate(goto):
                if new_item[1] == len(new_item) - 1:
                    for k, s in enumerate(new_item):
                        if s in grammar:
                            table[(i, s)] = ('REDUCE', new_item[:k])
                else:
                    table[(i, next_symbol)] = ('SHIFT', len(items) + j)
    return table

# Função para analisar a entrada usando a tabela de análise
def parse_input(input_string, table, grammar):
    stack = [0]
    input_string += '$'
    i = 0
    while True:
        state = stack[-1]
        symbol = input_string[i]
        if (state, symbol) not in table:
            return False
        action, value = table[(state, symbol)]
        if action == 'SHIFT':
            stack.append(symbol)
            stack.append(value)
            i += 1
        elif action == 'REDUCE':
            production = value
            stack = stack[:-len(production)]
            state = stack[-1]
            symbol = production[0]
            stack.append(symbol)
            stack.append(table[(state, symbol)][1])
        elif action == 'ACCEPT':
            return True

# Construção da tabela de análise LR(0)
lr0_table = build_lr0_table(grammar)

# Exemplo de entrada
input_string = 'id + id * id'

# Execução da análise sintática
if parse_input(input_string, lr0_table, grammar):
    print("A entrada é válida!")
else:
    print("A entrada não é válida!")
