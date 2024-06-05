class LR0Parser:
    def __init__(self):
        # Tabela de análise LR(0)
        self.action = {
            0: {'a': 's1', '$': 'ACCEPT'},
            1: {'a': 's1'},
        }
        self.goto = {
            0: {'A': 2}
        }
        self.productions = {
            0: ('A', ['A', 'a']),
            1: ('A', ['a'])
        }

    def parse(self, input_str):
        stack = [0]
        input_str += '$'
        pointer = 0

        while True:
            state = stack[-1]
            symbol = input_str[pointer]

            if symbol in self.action[state]:
                action = self.action[state][symbol]

                if action.startswith('s'):
                    stack.append(int(action[1:]))
                    pointer += 1
                elif action == 'ACCEPT':
                    print("Aceito")
                    break
            elif symbol in self.goto[state]:
                stack.append(self.goto[state][symbol])
            else:
                print("Erro de análise sintática")
                break

    def print_table(self):
        print("Tabela ACTION:")
        for state, transitions in self.action.items():
            for symbol, action in transitions.items():
                print(f"({state}, {symbol}): {action}")
        print("\nTabela GOTO:")
        for state, transitions in self.goto.items():
            for symbol, next_state in transitions.items():
                print(f"({state}, {symbol}): {next_state}")

# Função para solicitar entrada ao usuário
def get_input():
    return input("Digite a entrada: ")

# Exemplo de uso
parser = LR0Parser()
parser.print_table()
input_str = get_input()
parser.parse(input_str)
