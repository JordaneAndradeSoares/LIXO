// O grupo deverá estar identificado no cabeçalho de TODOS os arquivos do código-fonte:
// Jordane Andrade Soares

#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <string.h>
#include <math.h>
#include "hash.h"

void ImpHash(TipoListaHash Lista)
{
    TipoApontadorHash Aux;
    Aux = Lista.Primeiro->Prox;
    while (Aux != NULL)
    {
        printf("%.*s ", N, Aux->Item.Chave);
        Imprime(Aux->Item.Indices);
        Aux = Aux->Prox;
    }
}

void ImprimeHash(TipoDicionario Tabela)
{
    int i;
    for (i = 0; i < M; i++)
    {
        printf("[%d] => ", i);
        if (!VaziaHash(Tabela[i]))
            ImpHash(Tabela[i]);
        putchar('\n');
    }
}

void FLVaziaHash(TipoListaHash *Lista)
{
    Lista->Primeiro = (TipoCelulaHash *)malloc(sizeof(TipoCelulaHash));
    Lista->Ultimo = Lista->Primeiro;
    Lista->Primeiro->Prox = NULL;
}

short VaziaHash(TipoListaHash Lista)
{
    return (Lista.Primeiro == Lista.Ultimo);
}

void InsHash(TipoItem x, TipoListaHash *Lista)
{
    Lista->Ultimo->Prox = (TipoCelulaHash *)malloc(sizeof(TipoCelulaHash));
    Lista->Ultimo = Lista->Ultimo->Prox;
    Lista->Ultimo->Item = x;
    Lista->Ultimo->Prox = NULL;
}

void RetHash(TipoApontadorHash p, TipoListaHash *Lista, TipoItem *Item)
{
    /* -- Obs.: o item a ser retirado o seguinte ao apontado por p -- */
    TipoApontadorHash q;
    if (VaziaHash(*Lista) || p == NULL || p->Prox == NULL)
    {
        printf(" Erro Lista vazia ou posicao nao existe\n");
        return;
    }
    q = p->Prox;
    *Item = q->Item;
    p->Prox = q->Prox;
    if (p->Prox == NULL)
        Lista->Ultimo = p;
    free(q);
}

void GeraPesosHash(TipoPesos p)
{
    /* Gera valores randomicos entre 1 e 10.000 */
    int i, j;
    struct timeval semente;

    /* Utilizar o tempo como semente para a funcao srand() */
    gettimeofday(&semente, NULL);
    srand((int)(semente.tv_sec + 1000000 * semente.tv_usec));

    for (i = 0; i < N; i++)
        for (j = 0; j < TAMALFABETO; j++)
            p[i][j] = 1 + (int)(10000.0 * rand() / (RAND_MAX + 1.0));
}

TipoIndice Hash(TipoChave Chave, TipoPesos p, int *contador)
{
    int i;
    unsigned int Soma = 0;
    int comp = strlen(Chave);

    for (i = 0; i < comp; i++)
    {
        (*contador)++;
        Soma += p[i][(unsigned int)Chave[i]];
    }

    return (Soma % M);
}

void InicializaHash(TipoDicionario T)
{
    int i;
    for (i = 0; i < M; i++)
        FLVaziaHash(&T[i]);
}

TipoApontadorHash PesquisaHash(TipoChave Ch, TipoPesos p, TipoDicionario T, int contador[])
{
    /* Obs.: TipoApontadorHash de retorno aponta para o item anterior da lista */
    TipoIndice i;
    TipoApontadorHash Ap;
    i = Hash(Ch, p, contador);

    if (VaziaHash(T[i]))
    {
        (*contador)++;
        return NULL; /* Pesquisa sem sucesso */
    }
    else
    {
        (*contador)++;
        Ap = T[i].Primeiro;

        while (Ap->Prox->Prox != NULL && strncmp(Ch, Ap->Prox->Item.Chave, sizeof(TipoChave)))
        {
            (*contador)++;
            (*contador)++;
            Ap = Ap->Prox;
        }

        if (!strncmp(Ch, Ap->Prox->Item.Chave, sizeof(TipoChave)))
        {
            (*contador)++;
            return Ap;
        }
        else
        {
            (*contador)++;
            return NULL; /* Pesquisa sem sucesso */
        }
    }
}

void InsereHash(TipoItem x, TipoPesos p, TipoDicionario T, int contador[])
{
    TipoApontadorHash auxiliar = PesquisaHash(x.Chave, p, T, contador);
    if (auxiliar == NULL)
    {
        (*contador)++;
        InsHash(x, &T[Hash(x.Chave, p, contador)]);
    }
    else
    {
        (*contador)++;
        while (auxiliar != NULL && strcmp(auxiliar->Item.Chave, x.Chave) != 0)
        {
            (*contador)++;
            (*contador)++;
            auxiliar = auxiliar->Prox;
        }

        if (auxiliar != NULL)
        {
            (*contador)++;
            Insere(x.Indices.Primeiro->Prox->Item, &auxiliar->Item.Indices, contador);
            return;
        }

        InsHash(x, &T[Hash(x.Chave, p, contador)]);
        printf(" Registro ja  esta  presente\n");
    }
}

void RetiraHash(TipoItem x, TipoPesos p, TipoDicionario T, int contador[])
{
    TipoApontadorHash Ap;
    Ap = PesquisaHash(x.Chave, p, T, contador);
    if (Ap == NULL)
        printf(" Registro nao esta  presente\n");
    else
        RetHash(Ap, &T[Hash(x.Chave, p, contador)], &x);
}

int ContaElementosHash(TipoDicionario Tabela)
{
    int contador = 0;
    for (int i = 0; i < M; i++)
    {
        TipoApontadorHash aux = Tabela[i].Primeiro->Prox;
        while (aux != NULL)
        {
            contador++;
            aux = aux->Prox;
        }
    }
    return contador;
}

void PreencheVetorHash(TipoDicionario Tabela, TipoItem *vetor)
{
    int pos = 0;
    for (int i = 0; i < M; i++)
    {
        TipoApontadorHash aux = Tabela[i].Primeiro->Prox;
        while (aux != NULL)
        {
            vetor[pos++] = aux->Item;
            aux = aux->Prox;
        }
    }
}

int comparaChave(const void *a, const void *b)
{
    TipoItem *itemA = (TipoItem *)a;
    TipoItem *itemB = (TipoItem *)b;
    return strcmp(itemA->Chave, itemB->Chave);
}

void ImprimeVetorHash(TipoItem *vetor, int tamanho)
{
    for (int i = 0; i < tamanho; i++)
    {
        printf("%.*s: ", N, vetor[i].Chave);

        TipoApontador aux = vetor[i].Indices.Primeiro->Prox;
        while (aux != NULL)
        {
            printf("<%d, %d> ", aux->Item.IdDoc, aux->Item.Qtde);
            aux = aux->Prox;
        }
        printf("\n");
    }
}

void ImprimeOrdenado(TipoDicionario Tabela)
{
    int tamanho = ContaElementosHash(Tabela);
    if (tamanho == 0)
    {
        printf("Tabela vazia!\n");
        return;
    }

    TipoItem *vetor = (TipoItem *)malloc(tamanho * sizeof(TipoItem));
    if (vetor == NULL)
    {
        printf("Erro de alocação de memória!\n");
        exit(1);
    }

    PreencheVetorHash(Tabela, vetor);
    qsort(vetor, tamanho, sizeof(TipoItem), comparaChave);
    ImprimeVetorHash(vetor, tamanho);
    free(vetor);
}

float WIJ(TipoDicionario Tabela, TipoPesos Pesos, Palavra Palavra, int Doc, int QtdeDocs, int contador[])
{
    TipoApontadorHash termo = PesquisaHash(Palavra, Pesos, Tabela, contador);
    if (termo == NULL)
    {
        (*contador)++;
        return 0;
    }

    int fji = 0;

    if (Vazia(termo->Prox->Item.Indices))
    {
        (*contador)++;
        return 0;
    }

    TipoApontador Auxiliar = termo->Prox->Item.Indices.Primeiro->Prox;

    while (Auxiliar != NULL && Auxiliar->Item.IdDoc != Doc)
    {

        Auxiliar = Auxiliar->Prox;
    }

    if (Auxiliar == NULL)
    {
        return 0;
    }

    fji = Auxiliar->Item.Qtde;
    float NDocs = log2(QtdeDocs);
    int dj = 0;

    TipoApontador Auxiliar2 = termo->Prox->Item.Indices.Primeiro->Prox;
    while (Auxiliar2 != NULL)
    {
        dj++;
        Auxiliar2 = Auxiliar2->Prox;
    }

    return fji * (log2(NDocs) / dj);
}

float R(TipoDicionario Tabela, TipoPesos Pesos, Palavra *ListaPalavras, int Tamanho, int Doc, int QtdeDocs, int contador[])
{
    int ni = 0;

    for (int i = 0; i < M; i++)
    {
        (*contador)++;
        if (VaziaHash(Tabela[i]))
        {
            (*contador)++;
            continue;
        }

        TipoApontadorHash Auxiliar = Tabela[i].Primeiro->Prox;

        while (Auxiliar != NULL)
        {
            (*contador)++;
            ni++;
            Auxiliar = Auxiliar->Prox;
        }
    }

    float soma = 0;
    for (int i = 0; i < Tamanho; i++)
    {
        (*contador)++;
        float wij = WIJ(Tabela, Pesos, ListaPalavras[i], Doc, QtdeDocs, contador);
        soma += wij;
    }

    return 1.0 / ni * soma;
}

float *TFIDFHash(TipoDicionario Tabela, TipoPesos Pesos, Palavra *ListaPalavras, int Tamanho, int QtdeDocs, int contador[])
{
    float *Relevancia = (float *)calloc(QtdeDocs, sizeof(float));

    for (int i = 0; i < QtdeDocs; i++)
    {
        (*contador)++;
        Relevancia[i] = R(Tabela, Pesos, ListaPalavras, Tamanho, i + 1, QtdeDocs, contador);
    }

    return Relevancia;
}
