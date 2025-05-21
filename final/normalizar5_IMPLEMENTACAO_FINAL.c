#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Função para substituir caracteres acentuados por versões sem acento
char substituir_caractere(unsigned char c1, unsigned char c2)
{
    // UTF-8: c1 == 0xC3 indica caractere acentuado comum
    if (c1 == 0xC3)
    {
        switch (c2)
        {
        case 0xA1: // á
        case 0xA0: // à
        case 0xA2: // â
        case 0xA3: // ã
        case 0xA4: // ä
            return 'a';
        case 0xA9: // é
        case 0xA8: // è
        case 0xAA: // ê
        case 0xAB: // ë
            return 'e';
        case 0xAD: // í
        case 0xAC: // ì
        case 0xAE: // î
        case 0xAF: // ï
            return 'i';
        case 0xB3: // ó
        case 0xB2: // ò
        case 0xB4: // ô
        case 0xB5: // õ
        case 0xB6: // ö
            return 'o';
        case 0xBA: // ú
        case 0xB9: // ù
        case 0xBB: // û
        case 0xBC: // ü
            return 'u';
        case 0xA7: // ç
            return 'c';
        default:
            return '?'; // caractere desconhecido
        }
    }
    return 0;
}

char *normalizar(char *chave)
{
    int len = strlen(chave);
    char *resultado = calloc(len + 1, sizeof(char));
    int j = 0;

    for (int i = 0; i < len; i++)
    {
        unsigned char c = chave[i];
        if (c <= 0x7F)
        { // ASCII comum
            resultado[j++] = c;
        }
        else if ((unsigned char)c == 0xC3 && i + 1 < len)
        {
            char substituto = substituir_caractere(chave[i], chave[i + 1]);
            if (substituto)
                resultado[j++] = substituto;
            i++; // pular o segundo byte do caractere UTF-8
        }
    }

    resultado[j] = '\0';
    return resultado;
}

int main(void)
{
    FILE *pont_arq;
    char c;
    char buffer[200]; // espaço para armazenar o conteúdo do arquivo
    int i = 0;

    pont_arq = fopen("entrada.txt", "r");
    if (pont_arq == NULL)
    {
        printf("Erro ao tentar abrir o arquivo!");
        return 0;
    }

    printf("Entrada: ");
    while ((c = fgetc(pont_arq)) != EOF && i < sizeof(buffer) - 1)
    {
        buffer[i++] = c;
        printf("%c", c);
    }

    buffer[i] = '\0'; // finaliza a string
    fclose(pont_arq); // fecha o arquivo

    char *saida = normalizar(buffer);
    printf("\nSaida: %s\n", saida);

    free(saida); // libera a memória alocada dinamicamente
    return 0;
}
