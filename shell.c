#include <stdlib.h>
#include <stdio.h>

void shellSort(int arr[], int n)
{
    for (int gap = n / 2; gap > 0; gap /= 2)
    {
        for (int i = gap; i < n; i++)
        {
            int temp = arr[i];
            int j;

            for (j = i; j >= gap && arr[j - gap] > temp; j -= gap)
            {
                arr[j] = arr[j - gap];
            }

            arr[j] = temp;
        }
    }
}

int main()
{
    /*O algoritmo de ordenação ShellSort é uma extensão do algoritmo de ordenação por inserção que visa melhorar a
    eficiência deste último. Ao invés de simplesmente percorrer os elementos e trocá-los um a um, o ShellSort divide o
    array em grupos, chamados "gaps", e aplica o algoritmo de ordenação por inserção a cada grupo separadamente. À medida
    que o algoritmo avança, os gaps são reduzidos progressivamente, e o processo de ordenação por inserção é repetido nos
    subconjuntos até que o array esteja praticamente ordenado. A escolha estratégica dos gaps influencia o desempenho do algoritmo, e
    geralmente, o último passo envolve um gap de tamanho 1, transformando o algoritmo em uma ordenação por inserção convencional para
    garantir que os elementos estejam totalmente ordenados. O ShellSort oferece melhorias significativas em relação à ordenação por
    inserção em termos de eficiência média, sendo particularmente útil quando se lida com conjuntos de dados de tamanhos moderados.*/

    int arr[] = {12, 34, 54, 2, 3};
    int n = sizeof(arr) / sizeof(arr[0]);

    printf("Array original: ");
    for (int i = 0; i < n; i++)
        printf("%d ", arr[i]);
    printf("\n");

    shellSort(arr, n);

    printf("Array ordenado: ");
    for (int i = 0; i < n; i++)
        printf("%d ", arr[i]);
    printf("\n");

    return 0;
}
