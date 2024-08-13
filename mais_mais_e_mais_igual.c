#include <stdio.h>
#include <stdlib.h>

int main(){
    int a = 0;
    int b = 0;
    
    printf("\nTestes com '++':\n");

    printf("Teste 1: %d\n", a++);
    printf("Teste 2: %d\n", a);
    
    printf("\nTestes com '+=':\n");
    
    printf("Teste 3: %d\n", b+=1);
    printf("Teste 4: %d\n\n", b);
    
    return 0;
}