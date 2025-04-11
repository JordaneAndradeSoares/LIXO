#include <stdio.h>
#include <stdlib.h>

void imprime_sem_nada_no_final (int a, int b) {

    if (a < b){
        printf("%d - ", a);
        imprime_sem_nada_no_final(a + 1, b);
    }

    else {
        printf("%d", a);
    }
}

int main () {
    int a = 10;
    int b = 20 * a;
    
    printf ("\n\n\n");
    imprime_sem_nada_no_final (a, b);
    printf ("\n\n\n");

    return 0;
}