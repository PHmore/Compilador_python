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
            for rhs in self.productions[lhs]:
                for symbol in rhs:
                    if symbol and symbol not in self.productions:
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
                elif new_state is None and symbol in grammar.terminals:
                    # Se o próximo estado não puder ser alcançado e o símbolo for terminal,
                    # adicionamos uma transição para um estado de aceitação se a produção
                    # correspondente puder produzir vazio
                    for item in state:
                        if item.dot == len(item.rhs) and symbol in grammar.productions[item.lhs][0]:
                            transitions[(states.index(state), symbol)] = 'acc'
                            added = True
        states = new_states

    return states, transitions


def print_slr_table(tabela_slr, grammar):
    print("Tabela SLR:")
    print("-----------")
    print("Terminais:", grammar.terminals)
    print("Não-Terminais:", grammar.non_terminals)
    print("\nTabela Ação:")
    for state, actions in tabela_slr['Ação'].items():
        print(f"Estado {state}: {actions}")

    print("\nTabela Goto:")
    for state, gotos in tabela_slr['Goto'].items():
        print(f"Estado {state}: {gotos}")


def generate_table(productions):
    grammar = Grammar(productions)

    # Generate the states and transitions
    states, transitions = items(grammar)

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
                    next_symbol = item.rhs[item.dot + 1] if item.dot + 1 < len(item.rhs) else None
                    if symbol in grammar.terminals:
                        target_state = transitions.get((i, symbol))
                        if target_state is not None:
                            action_table[i][symbol] = f's{target_state}'
                    else:
                        # Se o símbolo é um não-terminal, precisamos considerar o lookahead
                        for lookahead in grammar.terminals.union({'$'}):
                            goto_state = transitions.get((i, symbol))
                            if goto_state is not None and (goto_state, lookahead) in transitions:
                                target_state = transitions[(goto_state, lookahead)]
                                goto_table[i][symbol] = target_state
                else:
                    if item.lhs == grammar.start_symbol and item.rhs == grammar.productions[grammar.start_symbol][0]:
                        action_table[i]['$'] = 'acc'
                    else:
                        prod_index = production_indices[(item.lhs, tuple(item.rhs))]
                        for terminal in grammar.terminals.union({'$'}):
                            if terminal not in action_table[i]:
                                action_table[i][terminal] = f'r{prod_index}'

        return action_table, goto_table


    # Create a generator that yields the tables as needed
    def table_generator():
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

        print_slr_table(tabela_slr, grammar)

        yield tabela_slr

    return table_generator()

