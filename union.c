#include <stdio.h>
#include <stdlib.h>

union tipo {
    char texto[200];
    float valor_quebrado;
    int valor_inteiro;
};

int main () {

    union tipo x;

    printf("Entre com um valor inteiro: ");
    scanf("%d", &x.valor_inteiro);
    printf("Valor inteiro: %d\n\n", x.valor_inteiro);

    printf("Entre com um valor quebrado: ");
    scanf("%f", &x.valor_quebrado);
    printf("Valor quebrado: %f\n\n", x.valor_quebrado);

    printf("Entre com um texto curto: ");
    scanf("%s", &x.texto);
    printf("Texto: %s\n\n", x.texto);

    printf("Valor inteiro FINAL: %d\n", x.valor_inteiro);
    printf("Valor quebrado FINAL: %f\n", x.valor_quebrado);
    printf("Texto FINAL: %s\n", x.texto);

    return 0;
}