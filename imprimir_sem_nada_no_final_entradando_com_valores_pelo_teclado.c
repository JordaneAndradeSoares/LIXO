#include <stdio.h>
#include <stdlib.h>

void imprime_sem_nada_no_final (int a, int b) {

    // valor de entrada positivo
    if (a > 0) { 
        if (b < a) {
            printf("%d, ", b);
            imprime_sem_nada_no_final(a, b + 1);
        }
    
        else {
            printf("%d", b);
        }
    }
    
    // valor de entrada negativo
    else if (a < 0) { 
        if (b > a) {
            printf("%d, ", a - b);
            imprime_sem_nada_no_final(a, b - 1);
        }
        
        else {
            printf("%d", a - b);
        }
    }

    // valor de entrada = zero
    else printf("%d", b); 
}

int main () {
    int tamanho = 10;
    int b = 0;
    int a = b;
    
    for (int i = 0; i < tamanho; i++) {
        printf ("\n\nEntre com o inteiro numero %d: ", i+1);
        scanf ("%d", &a);

        printf ("Lista completa %d: ", i + 1);
        imprime_sem_nada_no_final (a, b);       
    }
    
    return 0;
}