#include <stdio.h>
#include <stdlib.h>

int main(){

    int a = 4;
    int b = 0;
    int c = 0;

    for (int i = 0; i < a; i++){
        printf("Print %02d (numerado de 01 a %02d)\n", ++b, a);
    }

    printf("\n");

    for (int i = 0; i < a; i++){
        printf("Print %02d (numerado de 00 a %02d)\n", c++, a - 1);
    }

    return 0;
}