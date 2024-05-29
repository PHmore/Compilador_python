# Exemplo gerado pelo chat gpt de um analisador sintático que emprega o uso do SLR

# Definição da gramática
grammar = {
    'S': ['E'],
    'E': ['E + T', 'T'],
    'T': ['T * F', 'F'],
    'F': ['( E )', 'id']
}

# Construção dos conjuntos de itens de núcleo
def calculate_closure(item, grammar):
    queue = [item]
    closure = set(queue)
    while queue:
        current_item = queue.pop(0)
        dot_index = current_item.index('.')
        if dot_index < len(current_item) - 1 and current_item[dot_index + 1] in grammar:
            next_symbol = current_item[dot_index + 1]
            for production in grammar[next_symbol]:
                new_item = (next_symbol, ['.'] + production)
                if new_item not in closure:
                    closure.add(new_item)
                    queue.append(new_item)
    return closure

def calculate_goto(items, symbol, grammar):
    goto_set = set()
    for item in items:
        dot_index = item.index('.')
        if dot_index < len(item) - 1 and item[dot_index + 1] == symbol:
            new_item = item[:dot_index] + [symbol, '.'] + item[dot_index + 2:]
            goto_set.add(tuple(new_item))
    return calculate_closure(new_item, grammar)

# Construção da tabela de análise
def build_table(grammar):
    table = {}
    items = calculate_closure(('S', ['.'] + grammar['S']), grammar)
    for i, item in enumerate(items):
        if item[2] == '.' and len(item) > 3:
            for production in grammar[item[0]]:
                if item[1] in production:
                    table[(i, item[1])] = (i, 'REDUCE', production)
        else:
            for symbol in grammar.keys():
                goto = calculate_goto(items, symbol, grammar)
                if goto:
                    table[(i, symbol)] = (items.index(goto), 'GOTO')
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
        if action == 'REDUCE':
            production = value
            stack = stack[:-len(production[1])]
            state = stack[-1]
            symbol = production[0]
            stack.append(symbol)
            state = stack[-1]
            stack.append(table[(state, symbol)][0])
        elif action == 'GOTO':
            stack.append(symbol)
            stack.append(value)
            i += 1
        elif action == 'ACCEPT':
            return True

# Construção da tabela de análise
table = build_table(grammar)

# Exemplo de entrada
input_string = 'id + id * id'

# Execução da análise sintática
if parse_input(input_string, table, grammar):
    print("A entrada é válida!")
else:
    print("A entrada não é válida!")
