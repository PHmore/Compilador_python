class Grammar:
    def __init__(self, productions):
        self.productions = productions
        self.non_terminals = set()
        self.terminals = set()
        self.start_symbol = None
        self._process_grammar()

    def _process_grammar(self):
        for lhs in self.productions:
            if self.start_symbol is None:
                self.start_symbol = lhs
            self.non_terminals.add(lhs)
        for lhs, rhs_list in self.productions.items():
            for rhs in rhs_list:
                for symbol in rhs:
                    if symbol not in self.non_terminals:
                        self.terminals.add(symbol)

class Item:
    def __init__(self, lhs, rhs, dot):
        self.lhs = lhs
        self.rhs = rhs
        self.dot = dot

    def __eq__(self, other):
        return self.lhs == other.lhs and self.rhs == other.rhs and self.dot == other.dot

    def __hash__(self):
        return hash((self.lhs, tuple(self.rhs), self.dot))

    def __str__(self):
        return f"{self.lhs} -> {' '.join(self.rhs[:self.dot] + ['.'] + self.rhs[self.dot:])}"

def closure(items, grammar):
    closure_set = set(items)
    added = True

    while added:
        added = False
        new_items = set(closure_set)
        for item in closure_set:
            if item.dot < len(item.rhs):
                next_symbol = item.rhs[item.dot]
                if next_symbol in grammar.non_terminals:
                    for prod in grammar.productions[next_symbol]:
                        new_item = Item(next_symbol, prod, 0)
                        if new_item not in closure_set:
                            new_items.add(new_item)
                            added = True
        closure_set = new_items

    return closure_set

def goto(items, symbol, grammar):
    goto_set = set()
    for item in items:
        if item.dot < len(item.rhs) and item.rhs[item.dot] == symbol:
            goto_set.add(Item(item.lhs, item.rhs, item.dot + 1))
    return closure(goto_set, grammar)

def items(grammar):
    start_item = Item(grammar.start_symbol, grammar.productions[grammar.start_symbol][0], 0)
    start_state = closure([start_item], grammar)
    states = [start_state]
    symbols = grammar.non_terminals.union(grammar.terminals)
    transitions = {}

    added = True
    while added:
        added = False
        new_states = states.copy()
        for state in states:
            for symbol in symbols:
                new_state = goto(state, symbol, grammar)
                if new_state and new_state not in states:
                    new_states.append(new_state)
                    transitions[(states.index(state), symbol)] = len(new_states) - 1
                    added = True
        states = new_states

    return states, transitions

def getTabela(productions):

    grammar = Grammar(productions)

    # Generate the states and transitions
    states, transitions = items(grammar)

    # Print the states
    for i, state in enumerate(states):
        print(f"State {i}:")
        for item in state:
            print(f"  {item}")

    # Print the transitions
    print("\nTransitions:")
    for (state, symbol), target_state in transitions.items():
        print(f"  State {state} -- {symbol} --> State {target_state}")

    # Create a mapping of productions to unique indices
    production_indices = {}
    index = 1
    for lhs, rhs_list in grammar.productions.items():
        for rhs in rhs_list:
            production_indices[(lhs, tuple(rhs))] = index
            index += 1

    def create_tables(grammar, states, transitions, production_indices):
        action_table = {}
        goto_table = {}

        for i, state in enumerate(states):
            action_table[i] = {}
            goto_table[i] = {}
            for item in state:
                if item.dot < len(item.rhs):
                    symbol = item.rhs[item.dot]
                    if symbol in grammar.terminals:
                        target_state = transitions.get((i, symbol))
                        if target_state is not None:
                            action_table[i][symbol] = f's{target_state}'
                else:
                    if item.lhs == grammar.start_symbol and item.rhs == grammar.productions[grammar.start_symbol][0]:
                        action_table[i]['$'] = 'acc'
                    else:
                        prod_index = production_indices[(item.lhs, tuple(item.rhs))]
                        for terminal in grammar.terminals.union({'$'}):
                            if terminal not in action_table[i]:
                                action_table[i][terminal] = f'r{prod_index}'

            for symbol in grammar.non_terminals:
                target_state = transitions.get((i, symbol))
                if target_state is not None:
                    goto_table[i][symbol] = target_state

        return action_table, goto_table

    # Create the ACTION and GOTO tables
    action_table, goto_table = create_tables(grammar, states, transitions, production_indices)

    # Generate the production dictionary
    production_dict = {}
    for (lhs, rhs), index in production_indices.items():
        production_dict[index] = {'left': lhs, 'right': list(rhs)}

    # Create the final table structure
    tabela_slr = {
        'Ação': action_table,
        'Goto': goto_table,
        'Produção': production_dict
    }

    return tabela_slr




# productions = {
#     'S': [['PROGRAMA']],
#     'PROGRAMA': [['DECVAR']],
#     'DECVAR': [['int', 'id',';']],
# }

# tabela_slr = getTabela(productions)

# # Print the final table structure
# import pprint
# pprint.pprint(tabela_slr)