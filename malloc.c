#include <stdio.h>
#include <stdlib.h>

int main()
{
    int *vetor = malloc(sizeof(int)), escolha = 0, i = 0, j = 0;

    while (1)
    {
        printf("Escolha: 1. Sair ou 2. Entrar com um valor\n\n");
        scanf("%d", &escolha);

        if (escolha == 1)
        {
            break;
        }
        else if (escolha == 2)
        {
            printf("\nDigite um valor aqui: ");
            scanf("%d", &vetor[i]);
            i++;
        }
        else
        {
            printf("\nComando invalido\n");
        }
    }

    for (int j = 0; j < i; j++)
    {
        printf("Valor %d: %d\n", j + 1, vetor[j]);
    }

    return 0;
}