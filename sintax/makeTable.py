class Grammar:
    def __init__(self, productions):
        self.productions = productions
        self.terminals = set()
        self.non_terminals = set()
        self.start_symbol = list(productions.keys())[0]
        self.compute_terminals_and_non_terminals()

    def compute_terminals_and_non_terminals(self):
        for head, bodies in self.productions.items():
            self.non_terminals.add(head)
            for body in bodies:
                for symbol in body:
                    if symbol.isalpha() and symbol.islower():
                        self.terminals.add(symbol)
                    else:
                        self.non_terminals.add(symbol)
        # Adicionando explicitamente os caracteres especiais como terminais
        self.terminals.update(['(', ')', '+', '*', 'id'])

    def augmented_grammar(self):
        augmented_productions = {'S\'': [[self.start_symbol]]}
        augmented_productions.update(self.productions)
        return augmented_productions


class Item:
    def __init__(self, head, body, dot_position):
        self.head = head
        self.body = body
        self.dot_position = dot_position

    def __eq__(self, other):
        return (self.head == other.head and self.body == other.body and
                self.dot_position == other.dot_position)

    def __hash__(self):
        return hash((self.head, tuple(self.body), self.dot_position))

    def __repr__(self):
        return f"{self.head} -> {' '.join(self.body[:self.dot_position])} . {' '.join(self.body[self.dot_position:])}"


def closure(items, grammar):
    closure_set = set(items)
    while True:
        new_items = set(closure_set)
        for item in closure_set:
            if item.dot_position < len(item.body):
                symbol = item.body[item.dot_position]
                if symbol in grammar.non_terminals:
                    for production in grammar.productions[symbol]:
                        new_item = Item(symbol, production, 0)
                        new_items.add(new_item)
        if new_items == closure_set:
            return closure_set
        closure_set = new_items


def goto(items, symbol, grammar):
    goto_set = set()
    for item in items:
        if item.dot_position < len(item.body) and item.body[item.dot_position] == symbol:
            goto_set.add(Item(item.head, item.body, item.dot_position + 1))
    return closure(goto_set, grammar)


def items(grammar):
    start_item = Item('S\'', [grammar.start_symbol], 0)
    start_closure = closure([start_item], grammar)
    canonical_collection = [start_closure]
    states = {frozenset(start_closure): 0}

    transitions = {}
    while True:
        new_states = set()
        for state in canonical_collection:
            for symbol in grammar.terminals | grammar.non_terminals:
                goto_state = goto(state, symbol, grammar)
                if goto_state and frozenset(goto_state) not in states:
                    new_states.add(frozenset(goto_state))
                    states[frozenset(goto_state)] = len(states)
                if goto_state:
                    transitions[(frozenset(state), symbol)] = frozenset(goto_state)
        if not new_states:
            break
        canonical_collection.extend(new_states)

    return canonical_collection, transitions, states


def build_action_and_goto_tables(canonical_collection, transitions, states, grammar):
    action_table = {}
    goto_table = {}

    for i, state in enumerate(canonical_collection):
        action_table[i] = {}
        goto_table[i] = {}

        for item in state:
            if item.dot_position < len(item.body):
                symbol = item.body[item.dot_position]
                if symbol in grammar.terminals:
                    action_table[i][symbol] = 'S' + str(states[transitions[(frozenset(state), symbol)]])
            else:
                if item.head == 'S\'' and item.body == [grammar.start_symbol]:
                    action_table[i]['$'] = 'accept'
                else:
                    for prod_num, (head, bodies) in enumerate(grammar.productions.items(), start=1):
                        if (item.head, item.body) == (head, bodies):
                            for terminal in grammar.terminals:
                                action_table[i][terminal] = 'R' + str(prod_num)

        for non_terminal in grammar.non_terminals:
            if (frozenset(state), non_terminal) in transitions:
                goto_table[i][non_terminal] = states[transitions[(frozenset(state), non_terminal)]]

    return action_table, goto_table


productions = {
    'E': [['E', '+', 'T'], ['T']],
    'T': [['T', '*', 'F'], ['F']],
    'F': [['(', 'E', ')'], ['id']]
}

grammar = Grammar(productions)
canonical_collection, transitions, states = items(grammar)
action_table, goto_table = build_action_and_goto_tables(canonical_collection, transitions, states, grammar)

print("Action Table:")
for state, actions in action_table.items():
    print(state, actions)

print("\nGoto Table:")
for state, gotos in goto_table.items():
    print(state, gotos)
