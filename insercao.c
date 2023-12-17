
#include <stdlib.h>
#include <stdio.h>

void ordenacaoPorInsercao(int arr[], int n)
{
    int i, chave, j;
    for (i = 1; i < n; i++)
    {
        chave = arr[i];
        j = i - 1;

        // Move os elementos do arr[0..i-1] que são maiores que a chave
        // para uma posição à frente de sua posição atual
        while (j >= 0 && arr[j] > chave)
        {
            arr[j + 1] = arr[j];
            j = j - 1;
        }
        arr[j + 1] = chave;
    }
}

int main()
{
    /*O algoritmo de ordenação por inserção funciona construindo gradualmente uma sequência ordenada dentro do array,
    percorrendo cada elemento e inserindo-o na posição correta. Começando com o segundo elemento, o algoritmo compara este
    elemento com os anteriores na sequência ordenada e move os elementos maiores uma posição à frente para abrir espaço para a inserção.
    Esse processo é repetido até que todos os elementos estejam incorporados na sequência ordenada, resultando em um array totalmente ordenado.
    A eficiência do algoritmo depende da medida em que os elementos estão desordenados inicialmente, mas, em média, o algoritmo de ordenação
    por inserção possui uma complexidade de tempo de O(n^2). Apesar de ser menos eficiente em comparação com algoritmos como o QuickSort, o
    ordenação por inserção é uma escolha razoável para pequenos conjuntos de dados ou quando a maior parte do array já está ordenada.*/

    int arr[] = {12, 11, 13, 5, 6};
    int n = sizeof(arr) / sizeof(arr[0]);

    printf("Array original: ");
    for (int i = 0; i < n; i++)
        printf("%d ", arr[i]);
    printf("\n");

    ordenacaoPorInsercao(arr, n);

    printf("Array ordenado: ");
    for (int i = 0; i < n; i++)
        printf("%d ", arr[i]);
    printf("\n");

    return 0;
}
