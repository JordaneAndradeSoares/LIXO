#include <stdlib.h>
#include <stdio.h>

/* O algoritmo de ordenação QuickSort é um método eficiente e de divisão e conquista para ordenar arrays.
Ele seleciona um elemento do array como pivô e rearranja os outros elementos, colocando os menores à
esquerda e os maiores à direita do pivô. Em seguida, o QuickSort é aplicado recursivamente às duas
sub-sequências resultantes. A escolha estratégica do pivô influencia a eficiência do algoritmo, sendo comum escolher o
elemento do meio. A principal vantagem do QuickSort é sua eficiência média de tempo O(n log n), tornando-o mais rápido em muitos
casos do que algoritmos de ordenação mais simples, como Bubble Sort ou Insertion Sort. No entanto, o QuickSort pode ser sensível à
escolha inadequada do pivô em certos casos, levando à pior complexidade de tempo O(n^2). Essa instabilidade pode ser mitigada por
abordagens como a escolha aleatória do pivô ou a utilização do algoritmo de três pivôs.
*/

void troca(int *a, int *b)
{
    int c = *a;
    *a = *b;
    *b = c;
}

int particiona(int *numeros, int esquerda, int direita)
{
    // Escolhe o pivô como o elemento do meio
    int pivo = numeros[(esquerda + direita) / 2];

    while (esquerda <= direita)
    {
        // Encontra elemento na parte esquerda que deve estar à direita do pivô
        while (numeros[esquerda] < pivo)
            esquerda++;

        // Encontra elemento na parte direita que deve estar à esquerda do pivô
        while (numeros[direita] > pivo)
            direita--;

        // Troca os elementos encontrados
        if (esquerda <= direita)
        {
            troca(&numeros[esquerda], &numeros[direita]);
            esquerda++;
            direita--;
        }
    }

    return esquerda;
}

void quicksort(int *numeros, int esquerda, int direita)
{
    if (esquerda < direita)
    {
        // Obtém o índice do pivô após a partição
        int indice_pivo = particiona(numeros, esquerda, direita);

        // Aplica o QuickSort recursivamente nas sub-sequências
        quicksort(numeros, esquerda, indice_pivo - 1);
        quicksort(numeros, indice_pivo, direita);
    }
}

int main()
{
    int numeros[] = {2, 5, 3, 6, 4, 7, 1};
    int n = sizeof(numeros) / sizeof(numeros[0]);

    printf("Array original: ");
    for (int i = 0; i < n; i++)
    {
        printf("%d ", numeros[i]);
    }

    // Aplica o QuickSort
    quicksort(numeros, 0, n - 1);

    printf("\nArray ordenado: ");
    for (int i = 0; i < n; i++)
    {
        printf("%d ", numeros[i]);
    }

    return 0;
}
