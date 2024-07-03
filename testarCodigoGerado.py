import sys
import math

def minhaFuncao():
    x = 10
    print("Valor de x: " + x)

def main():
    numero = 0
    letra = 'K'
    print("A letra é " + letra)
    if numero == 0:
        print("O número é zero!")
    else:
        print("O número não é zero...")
    for i in range(0, 5):
        print("Hello World (for)")
    while numero < 5:
        print("Hello world (while)")
        numero += 1

if __name__ == '__main__':
    main()