#include <stdio.h>
#include <stdlib.h>

int par(num){
    if (num % 2 == 0)
        return 1;  // 1 seria o caso verdadeiro
    return 0; //0 seria o caso falso
}

void main(){
    int i = 5;
    float f = 3.45;
    char c = 'G';

    printf(par(i));  //mostra o resultado da função par() para i

    printf("Olá, mundo!");

    for (int j = 0; j < 5; j++){
        printf("Compilador", j);
    }
}