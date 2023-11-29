#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main()
{
    int pimbamento = 1000;
    clock_t pimba_1, pimba_2;

    pimba_1 = clock();
    pimbada(pimbamento);
    pimba_2 = clock();

    double duracao = ((double)(pimba_2 - pimba_1)) / CLOCKS_PER_SEC;
    printf("Tempo: %lf\n", duracao);
    printf("Pimba 1: %d\n", pimba_1);
    printf("Pimba 2: %d", pimba_2);
}