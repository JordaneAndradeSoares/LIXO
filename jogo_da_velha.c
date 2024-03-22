#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int verificarVencedor(int SIZE, int tabuleiro[SIZE][SIZE], int jogador)
{
    for (int i = 0; i < SIZE; i++)
    {
        if ((tabuleiro[i][0] == jogador && tabuleiro[i][1] == jogador && tabuleiro[i][2] == jogador) ||
            (tabuleiro[0][i] == jogador && tabuleiro[1][i] == jogador && tabuleiro[2][i] == jogador))
        {
            return jogador;
        }
    }

    if ((tabuleiro[0][0] == jogador && tabuleiro[1][1] == jogador && tabuleiro[2][2] == jogador) ||
        (tabuleiro[0][2] == jogador && tabuleiro[1][1] == jogador && tabuleiro[2][0] == jogador))
    {
        return jogador;
    }

    return 0;
}

int verificarEmpate(int SIZE, int tabuleiro[SIZE][SIZE])
{
    for (int i = 0; i < SIZE; i++)
    {
        for (int j = 0; j < SIZE; j++)
        {
            if (tabuleiro[i][j] == 0)
            {
                return 0; // Ainda há movimentos possíveis
            }
        }
    }

    return 1; // Tabuleiro cheio, empate
}

int main()
{
    srand(time(NULL));
    int tamanho = 3, matriz[tamanho][tamanho], linha_bot, coluna_bot, linha_hu, coluna_hu;

    for (int i = 0; i < tamanho; i++)
    {
        for (int j = 0; j < tamanho; j++)
        {
            matriz[i][j] = 0;
        }
    }

    while (1)
    {
        // Jogada do BOT
        while (1)
        {
            linha_bot = rand() % tamanho;
            coluna_bot = rand() % tamanho;

            if (matriz[linha_bot][coluna_bot] == 0)
            {
                matriz[linha_bot][coluna_bot] = 1;
                break;
            }
        }

        // Imprimir o tabuleiro após a jogada do BOT
        printf("Jogada do BOT:\n");
        for (int i = 0; i < tamanho; i++)
        {
            for (int j = 0; j < tamanho; j++)
            {
                printf("%d ", matriz[i][j]);
            }
            printf("\n");
        }
        printf("\n");

        // Verificar vitória do BOT
        int vitoria_bot = verificarVencedor(tamanho, matriz, 1);
        if (vitoria_bot == 1)
        {
            printf("BOT venceu!\n");
            break;
        }

        // Verificar empate
        if (verificarEmpate(tamanho, matriz))
        {
            printf("Empate!\n");
            break;
        }

        // Jogada do humano
        while (1)
        {
            printf("Digite uma linha (1, 2 ou 3): ");
            scanf("%d", &linha_hu);
            printf("Digite uma coluna (1, 2 ou 3): ");
            scanf("%d", &coluna_hu);

            if (matriz[linha_hu - 1][coluna_hu - 1] == 0)
            {
                matriz[linha_hu - 1][coluna_hu - 1] = 2;
                break;
            }
            else
            {
                printf("Ocupado. Tente outra escolha.\n");
            }
        }

        // Verificar vitória do humano
        int vitoria_hu = verificarVencedor(tamanho, matriz, 2);
        if (vitoria_hu == 2)
        {
            printf("Humano venceu!\n");
            break;
        }

        // Imprimir o tabuleiro após a jogada do humano
        printf("Jogada do humano:\n");
        for (int i = 0; i < tamanho; i++)
        {
            for (int j = 0; j < tamanho; j++)
            {
                printf("%d ", matriz[i][j]);
            }
            printf("\n");
        }
        printf("\n");

        // Verificar empate
        if (verificarEmpate(tamanho, matriz))
        {
            printf("Empate!\n");
            break;
        }
    }

    return 0;
}
