#include <stdio.h>
#include <stdlib.h>

// Função para imprimir uma sequência
void imprimir(int caminho[], int tamanho, int *contador) {
    (*contador)++;
    printf("Possibilidade %d: ", *contador);

    for (int i = 0; i < tamanho; i++) {
        printf("%d ", caminho[i]);
    }
    printf("\n");
}

// Função recursiva para gerar as possibilidades
int gerar(int n, int caminho[], int pos, int *contador) {
    if (n == 0) {
        imprimir(caminho, pos, contador);
        return 1;
    }

    int total = 0;

    // Pular 1 pedra
    if (n >= 1) {
        caminho[pos] = 1;
        total += gerar(n - 1, caminho, pos + 1, contador);
    }

    // Pular 2 pedras
    if (n >= 2) {
        caminho[pos] = 2;
        total += gerar(n - 2, caminho, pos + 1, contador);
    }

    return total;
}

int main() {

    printf("Sapo pulando pedras\n");
    
    int n;
    int caminho[100];
    int contador = 0;

    printf("Digite a quantidade de pedras: ");
    scanf("%d", &n);
    
    int total = gerar(n, caminho, 0, &contador);

    printf("Total de possibilidades: %d\n", total);

    return 0;
}