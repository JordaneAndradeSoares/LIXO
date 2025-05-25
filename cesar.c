#include <stdio.h>
#include <string.h>

void faz_cifra_de_cesar(char *texto, int deslocamento)
{
    int tamanho = strlen(texto);

    for (int i = 0; i < tamanho; i++)
    {
        if (texto[i] >= 'A' && texto[i] <= 'Z')
            texto[i] = ((texto[i] - 'A' + deslocamento) % 26) + 'A';
    }
}

void desfaz_cifra_de_cesar(char *texto, int deslocamento)
{
    int tamanho = strlen(texto);

    for (int i = 0; i < tamanho; i++)
    {
        if (texto[i] >= 'A' && texto[i] <= 'Z')
            texto[i] = ((texto[i] + 'A' - deslocamento) % 26) + 'A';
    }
}

int main()
{
    char texto[100];

    int escolha;
    int deslocamento;

    printf("Deslocamento da cifra de Cesar: ");
    scanf("%d", &deslocamento);

    printf("Fazer os desfazer (1 ou 2): ");
    scanf("%d", &escolha);

    printf("\nEntrada (completamente em MAIUSCULO): ");
    scanf("%s", texto);

    if (escolha == 1)
    {
        faz_cifra_de_cesar(texto, deslocamento);
        printf("Saida faz cifra de Cesar: %s\n", texto);
    }

    if (escolha == 2)
    {
        desfaz_cifra_de_cesar(texto, deslocamento);
        printf("Saida desfaz cifra de Cesar: %s\n", texto);
    }

    return 0;
}
