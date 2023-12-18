#include <stdio.h>
#include <stdlib.h>

int main()
{
    int valor_de_entrada, valor_lido;

    printf("Entre com um valor: ");
    scanf("%d", &valor_de_entrada);

    FILE *arquivo = fopen("arquivo.txt", "w");

    if (arquivo == NULL)
    {
        fprintf(stderr, "Não foi possível abrir o arquivo.\n");
        return 1;
    }

    fprintf(arquivo, "%d", valor_de_entrada);

    fclose(arquivo);
    arquivo = fopen("arquivo.txt", "r");

    while (fscanf(arquivo, "%d", &valor_lido) == 1)
    {
        printf("Valor lido: %d\n", valor_lido);
    }

    fclose(arquivo);

    return 0;
}
