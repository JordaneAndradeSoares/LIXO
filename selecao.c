#include <stdlib.h>
#include <stdio.h>

void troca(int *a, int *b)
{
    int temp = *a;
    *a = *b;
    *b = temp;
}

void selectionSort(int arr[], int n)
{
    // Percorre o array
    for (int i = 0; i < n - 1; i++)
    {
        // Encontra o índice do menor elemento no restante do array
        for (int j = i + 1; j < n; j++)
            if (arr[j] < arr[i])
            {
                // Troca o menor elemento com o primeiro não ordenado
                troca(&arr[j], &arr[i]);
            }
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
    /*O método de ordenação por seleção é um algoritmo simples e intuitivo que percorre repetidamente um array,
    selecionando o menor (ou maior) elemento e trocando-o com o primeiro elemento não classificado. Esse processo é
    repetido para os elementos subsequentes até que todo o array esteja ordenado. Apesar de sua simplicidade e facilidade
    de implementação, o método de seleção tem uma complexidade de tempo quadrática O(n^2), tornando-o menos eficiente para
    grandes conjuntos de dados em comparação com algoritmos mais avançados. No entanto, sua simplicidade o torna útil para pequenos
    conjuntos de dados ou quando o overhead" (custo adicional associado a determinada atividade que não contribui diretamente
    para o resultado desejado, mas é inevitável ou necessário para a execução da tarefa principal)
    de outros algoritmos pode superar os benefícios em termos de desempenho.*/

    int arr[] = {64, 25, 12, 22, 11};
    int n = sizeof(arr) / sizeof(arr[0]);

    printf("Array original: ");
    imprimirArray(arr, n);

    selectionSort(arr, n);

    printf("Array ordenado: ");
    imprimirArray(arr, n);

    return 0;
}
