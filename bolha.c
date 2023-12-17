#include <stdlib.h>
#include <stdio.h>

void troca(int *a, int *b)
{
    int c = *a;
    *a = *b;
    *b = c;
}

/*O algoritmo de ordenação Bubble Sort funciona percorrendo repetidamente um array e comparando elementos adjacentes.
Em cada passagem, o algoritmo compara pares de elementos e os troca se estiverem na ordem errada, movendo o maior elemento em direção ao final do array.
Esse processo é repetido até que nenhum elemento precise ser trocado em uma passagem completa, indicando que o array está ordenado. O nome "Bubble"
refere-se à forma como os elementos maiores "borbulham" para o final do array durante o processo de ordenação. Apesar de sua simplicidade e
facilidade de implementação, o Bubble Sort pode ser ineficiente para
grandes conjuntos de dados, especialmente quando comparado a algoritmos mais avançados como o QuickSort */

int main()
{
    int flag = 1, numeros[] = {2, 5, 3, 6, 4, 7, 1};
    int n = sizeof(numeros) / sizeof(numeros[0]);

    printf("\nOriginal: ");
    for (int i = 0; i < n; i++)
    {
        printf("%d ", numeros[i]);
    }

    while (flag)
    {
        flag = 0;
        for (int i = 0; i < n - 1; i++)
        {
            if (numeros[i] > numeros[i + 1])
            {
                troca(&numeros[i + 1], &numeros[i]);
                flag = 1;
            }
        }
    }

    printf("\nCrescente: ");
    for (int i = 0; i < n; i++)
    {
        printf("%d ", numeros[i]);
    }

    flag = 1;
    while (flag)
    {
        flag = 0;
        for (int i = 0; i < n - 1; i++)
        {
            if (numeros[i] < numeros[i + 1])
            {
                troca(&numeros[i + 1], &numeros[i]);
                flag = 1;
            }
        }
    }

    printf("\nDecrescente: ");
    for (int i = 0; i < n; i++)
    {
        printf("%d ", numeros[i]);
    }

    return 0;
}
