// O grupo deverá estar identificado no cabeçalho de TODOS os arquivos do código-fonte:
// Jordane Andrade Soares

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#include "hash.h"
#include "patricia.h"

void ParaMinusculo(Palavra p, int tamanho)
{
    for (int i = 0; i < tamanho; i++)
    {
        if (p[i] >= 'A' && p[i] <= 'Z')
        {
            p[i] += 32;
        }
    }
}

void RemoveEspeciais(Palavra p)
{
    char *src = p;
    char *dest = p;

    while (*src)
    {
        if (isalnum((unsigned char)*src) || *src == ' ')
        {
            *dest++ = *src;
        }

        src++;
    }

    *dest = '\0';
}

int main()
{
    char controle;   // variavel que controla do menu de escolha
    int contador[4]; // vetor que guarda a quantidade de comparações da inserção e pesquina na hash e patricia

    FILE *entrada = fopen("entrada.txt", "r"); // leitura do arquivo "entrada.txt"
    FILE *leitura = NULL;

    TipoDicionario Tabela;
    TipoArvore Arvore = NULL; // CORRIGIDO: Inicialize a árvore como NULL
    TipoChave Chave;
    TipoPesos Pesos;
    TipoItem Item;

    InicializaHash(Tabela);
    GeraPesosHash(Pesos);

    while (1)
    {
        int N2; // quantidade de arquivos para ler as informações (já havia uma variavel chamada N)

        contador[0] = 0; // 0. inserções hash
        contador[1] = 0; // 1. inserções patricia
        contador[2] = 0; // 2. pesquisa hash
        contador[3] = 0; // 3. pesquisa patricia

        printf("\na) receber o arquivo de entrada com os textos a serem indexados;");
        printf("\nb) construir os indices invertidos");
        printf("\nc) imprimir os indices invertidos");
        printf("\nd) buscar nos indices invertidos construidos");
        printf("\ne) sair da loop");
        printf("\n   escolha: ");

        scanf(" %c", &controle); // entrada do controle, o espaço é necessario para o funcionamento correto do scanf
        printf("\n");            // printf para manter o visual bonito

        if (controle == 'a') // comando igual 'a' (receber entrada)
        {
            if (entrada == NULL) // testando se o arquivo foi aberto
                return 0;        // encerrando se o arquivo NÃO foi aberto

            fscanf(entrada, "%d", &N2); // lendo N
            fgetc(entrada);             // ignorando o "\n"
        }

        else if (controle == 'b') // comando igual 'b' (construir os indices invertidos)
        {
            printf("Quantidade de arquivos: %d\n", N2);
            for (int i = 0; i < N2; i++)
            {
                char nome_do_arquivo[200];
                fscanf(entrada, "%s", nome_do_arquivo); // lendo o nome do arquivo de onde ler as informações
                printf("Nome do arquivo %d = %s\n", i + 1, nome_do_arquivo);
                leitura = fopen(nome_do_arquivo, "r"); // abrindo o arquivo para ler as informações

                if (leitura == NULL) // testando se o arquivo foi aberto
                    return 0;        // encerrando se o arquivo NÃO foi aberto

                char conteudo[200];

                // lendo o arquivo do começo ao fim e salvando em um buffer
                fseek(leitura, 0, SEEK_END);
                long tamanho = ftell(leitura); // pega tamanho do arquivo
                fseek(leitura, 0, SEEK_SET);

                char *buffer = malloc(tamanho + 1);
                fread(buffer, 1, tamanho, leitura);
                buffer[tamanho] = '\0';

                char *token = strtok(buffer, " \t\r\n");

                while (token != NULL)
                {
                    TipoItem Elemento;
                    IndiceInvertido Indice;

                    Indice.IdDoc = i + 1;
                    Indice.Qtde = 1;

                    strcpy(Elemento.Chave, token);
                    ParaMinusculo(Elemento.Chave, strlen(Elemento.Chave)); // minimização dos caracteres
                    RemoveEspeciais(Elemento.Chave);                       // remoção de caractere especial

                    // 0. inserindo na hash
                    FLVazia(&Elemento.Indices);
                    Insere(Indice, &Elemento.Indices, &contador[0]);
                    InsereHash(Elemento, Pesos, Tabela, &contador[0]);

                    // 1. inserindo na patricia
                    Arvore = InserePatricia(Elemento, &Arvore, &contador[1]);

                    token = strtok(NULL, " \t\r\n");
                }

                printf("Contador insere HASH: %d\n", contador[0]);
                printf("Contador insere PATRICIA: %d\n", contador[1]);
                fclose(leitura);
            }

            fclose(entrada); // fechando o arquivo
        }

        else if (controle == 'c') // comando igual a 'c' (imprimir os indices invertidos)
        {
            printf("HASH DESORDENADA:\n"); // print puramente visual
            ImprimeHash(Tabela);           // imprimindo a tabela hash normal
            printf("\nHASH ORDENADA:\n");  // print puramente visual
            ImprimeOrdenado(Tabela);       // copiando a hash e ordenando a copia dela

            printf("\nPATRICIA (naturalmente ordenada):\n"); // print puramente visual
            ImprimePatricia(Arvore);                         // imprimindo a árvore patricia
        }

        else if (controle == 'd') // comando igual a 'd' (buscar nos indices invertidos construidos)
        {
            // entrando com a quantidade de elementos para pesquisar
            int QTDEPalavras = 0;
            printf("Quantas palavras quer buscar: ");
            scanf("%d", &QTDEPalavras);
            getchar();

            Palavra ListaDePalavras[QTDEPalavras];

            for (int i = 0; i < QTDEPalavras; i++)
            {
                // entrando com os elementos para pesquisar
                printf("Insira a palavra %d: ", i + 1);
                scanf("%s", ListaDePalavras[i]);
                printf("Palavra '%s' inserida\n", ListaDePalavras[i]);

                // normalizando elementos que quero pesquisar
                ParaMinusculo(ListaDePalavras[i], strlen(ListaDePalavras[i]));
                RemoveEspeciais(ListaDePalavras[i]);
            }

            // 2. pesquisa hash
            printf("HASH:\n");
            float *tfidf = TFIDFHash(Tabela, Pesos, ListaDePalavras, QTDEPalavras, N2, &contador[2]);
            for (int i = 0; i < N2; i++)
                printf("Relevancia Doc. #%d = %f\n", i + 1, tfidf[i]);

            // 3. pesquisa patricia
            PesquisaPatricia(Arvore, ListaDePalavras, QTDEPalavras, N2, &contador[3]);

            printf("Contador pesquisa HASH: %d\n", contador[2]);
            printf("Contador pesquisa PATRICIA: %d\n", contador[3]);
        }

        else if (controle == 'e') // comando igual a 'e' (fechar o loop)
            return 0;             // encerrando a execução

        else
            printf("Comando errado\n");
    }
}