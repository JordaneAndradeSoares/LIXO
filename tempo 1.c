#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main()
{
    int tamanho = 999;
    double tempo;
    clock_t comeco, final;

    comeco = clock();

    for (int i = 0; i < tamanho; i++)
    {
        printf("Valor: %d\n", i + 1);
    }

    final = clock();
    tempo = ((double)(final - comeco)) / CLOCKS_PER_SEC;

    printf("Tempo gasto: %f segundos\n", tempo);

    return 0;
}