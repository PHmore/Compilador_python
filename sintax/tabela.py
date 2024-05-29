# Tabela de Ação e Goto para SLR
tabela_slr = {
    'Estados': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    'Ação': {
        0: {'int': 'S3', 'float': 'S4', 'char': 'S5', 'void': 'S6', '$': 'acc'},
        1: {'$': 'acc'},
        2: {'int': 'S3', 'float': 'S4', 'char': 'S5', 'void': 'S6', '$': 'R3'},
        3: {'Identificador': 'S7'},
        4: {'Identificador': 'S8'},
        5: {'Identificador': 'S9'},
        6: {'Identificador': 'S10'},
        7: {';': 'R6'},
        8: {'(': 'S11'},
        9: {'(': 'S12'},
        10: {'(': 'S13'},
        11: {'Tipo': 'S14'},
        12: {'Tipo': 'S15'},
        13: {'Tipo': 'S16'},
        14: {'Identificador': 'S17'},
        15: {'Identificador': 'S18'},
        16: {'Identificador': 'S19'},
        17: {')': 'R7'},
        18: {')': 'R8'},
        19: {')': 'R9'},
    },
    'Goto': {
        0: {'DeclaraçãoLista': 1, 'Declaração': 2, 'DeclaraçãoVariável': 3, 'DeclaraçãoFunção': 4, 'Tipo': 5},
        1: {},
        2: {'DeclaraçãoLista': 6, 'Declaração': 7, 'DeclaraçãoVariável': 8, 'DeclaraçãoFunção': 9, 'Tipo': 10},
        3: {},
        4: {},
        5: {},
        6: {'Declaração': 11, 'DeclaraçãoVariável': 12, 'DeclaraçãoFunção': 13, 'Tipo': 14},
        7: {},
        8: {},
        9: {},
        10: {},
        11: {'DeclaraçãoLista': 15, 'Declaração': 16, 'DeclaraçãoVariável': 17, 'DeclaraçãoFunção': 18, 'Tipo': 19},
        12: {},
        13: {},
        14: {},
        15: {},
        16: {},
        17: {},
        18: {},
        19: {},
    }
}

# Exibição da Tabela
print("Tabela de Ação e Goto para SLR:")
print("{:<10} {:<20} {:<20}".format("Estado", "Ação", "Goto"))
for estado in tabela_slr['Estados']:
    acoes = tabela_slr['Ação'].get(estado, {})
    goto = tabela_slr['Goto'].get(estado, {})
    print("{:<10} {:<20} {:<20}".format(estado, str(acoes), str(goto)))
