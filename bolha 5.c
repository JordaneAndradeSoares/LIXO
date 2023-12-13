#include <stdio.h>
#include <stdlib.h>

int main()
{
    int ajudante, tamanho_do_vetor = 4, vetor[tamanho_do_vetor];

    for (int i = 0; i < tamanho_do_vetor; i++)
    {
        printf("Entre com o valor %d: ", i + 1);
        scanf("%d", &vetor[i]);
    }

    for (int i = 0; i < tamanho_do_vetor - 1; i++)
    {
        for (int j = 1; j < tamanho_do_vetor - i; j++)
        {
            if (vetor[j] < vetor[j - 1])
            {
                ajudante = vetor[j - 1];
                vetor[j - 1] = vetor[j];
                vetor[j] = ajudante;
            }
        }
    }

    printf("\n");

    for (int i = 0; i < tamanho_do_vetor; i++)
    {
        printf("Valor %d: %d\n", i + 1, vetor[i]);
    }

    return 0;
}