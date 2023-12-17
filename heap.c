#include <stdlib.h>
#include <stdio.h>

void troca(int *a, int *b)
{
    int temp = *a;
    *a = *b;
    *b = temp;
}

void maxHeapify(int arr[], int n, int i)
{
    int maior = i;
    int esquerda = 2 * i + 1;
    int direita = 2 * i + 2;

    if (esquerda < n && arr[esquerda] > arr[maior])
        maior = esquerda;

    if (direita < n && arr[direita] > arr[maior])
        maior = direita;

    if (maior != i)
    {
        troca(&arr[i], &arr[maior]);
        maxHeapify(arr, n, maior);
    }
}

void heapSort(int arr[], int n)
{
    // Construir o heap (reorganizar o array)
    for (int i = n / 2 - 1; i >= 0; i--)
        maxHeapify(arr, n, i);

    // Extrair elementos um por um do heap
    for (int i = n - 1; i > 0; i--)
    {
        troca(&arr[0], &arr[i]);
        maxHeapify(arr, i, 0);
    }
}

void imprimirArray(int arr[], int n)
{
    for (int i = 0; i < n; i++)
        printf("%d ", arr[i]);
    printf("\n");
}

int main()
{
    /*O Heap Sort é um algoritmo de ordenação eficiente que utiliza uma estrutura de dados chamada heap para organizar os elementos do array.
    Inicialmente, constrói-se um heap a partir do array, garantindo que a propriedade do heap seja mantida (por exemplo, um heap máximo em que cada
    nó pai é maior ou igual aos seus filhos). Em seguida, o algoritmo realiza repetidas extrações do elemento máximo (ou mínimo) do heap,
    colocando-o no final do array. Esse processo é repetido até que todos os elementos sejam extraídos e o array esteja completamente ordenado.
    O Heap Sort possui uma complexidade de tempo média de O(n log n), tornando-o eficiente para grandes conjuntos
    de dados, embora sua principal desvantagem seja uma menor eficiência em termos de cache comparada a alguns outros algoritmos de ordenação.*/

    int arr[] = {12, 11, 13, 5, 6, 7};
    int n = sizeof(arr) / sizeof(arr[0]);

    printf("Array original: ");
    imprimirArray(arr, n);

    heapSort(arr, n);

    printf("Array ordenado: ");
    imprimirArray(arr, n);

    return 0;
}
