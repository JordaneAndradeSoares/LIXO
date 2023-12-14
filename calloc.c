#include <stdio.h>
#include <stdlib.h>

int main()
{
    int tamanho = 4, *vetor = calloc(4, sizeof(int));

    printf("Antes de preencher\n");
    for (int j = 0; j < tamanho; j++)
    {
        printf("Valor %d: %d\n", j + 1, vetor[j]);
    }

    printf("\nPreenchendo\n");
    for (int i = 0; i < tamanho; i++)
    {
        printf("Digite o %d valor aqui: ", i + 1);
        scanf("%d", &vetor[i]);
    }

    printf("\n");
    printf("Preenchido\n");

    for (int j = 0; j < tamanho; j++)
    {
        printf("Valor %d: %d\n", j + 1, vetor[j]);
    }

    return 0;
}