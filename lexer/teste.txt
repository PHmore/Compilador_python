#include <stdio.h>

int par(num){
    if (num % 2 == 0){
        return 1;}
    else{
    return 0;}
}

void main(){
    int i = 5;
    float f = 3.45;
    char c = 'G';

    printf(par(i));

    printf("Olá, mundo!");

    for (int j = 0; j < 5; j++){
        printf("Compilador", j);
    }
}