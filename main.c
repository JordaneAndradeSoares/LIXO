#include <stdio.h>
#include <stdlib.h>

int variavel_global = 1;

void print(int i, int a){

    if (i == 1){
        printf("Tabuada do 10 de 1 ao 10:\n\n");
    }

    printf("%d x %02d = %03d\n", a, i++, a*i);
    variavel_global = i;
}

int main(int i, int a){
    a = 10;
    i = variavel_global;

    if (i > 10){
        return 0;

    } else {
        print(i, a);
        main(i, a);
    }
}