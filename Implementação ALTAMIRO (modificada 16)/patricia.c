// O grupo deverá estar identificado no cabeçalho de TODOS os arquivos do código-fonte:
// Jordane Andrade Soares

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <sys/time.h>
#include "patricia.h"

void ImprimePatricia(TipoArvore p)
{
    if (p == NULL)
        return;

    if (p->nt == Externo)
    {
        printf("%s: ", p->NO.Item.Chave);
        TipoCelula *pAux = p->NO.Item.Indices.Primeiro->Prox;

        while (pAux != NULL)
        {
            printf("< %d, %d > ", pAux->Item.Qtde, pAux->Item.IdDoc);
            pAux = pAux->Prox;
        }

        printf("\n");
    }
    else
    {
        ImprimePatricia(p->NO.NInterno.Esq);
        ImprimePatricia(p->NO.NInterno.Dir);
    }
}

TipoDib Bit(IndicePat i, TipoItem k, int contador[])
{
    if (i.Posicao >= strlen(k.Chave))
    {
        (*contador)++;
        return 0;
    }

    (*contador)++;
    return k.Chave[i.Posicao] >= i.Letra ? 1 : 0;
}

IndicePat Compara(TipoItem a, TipoItem b, int *contador)
{
    int tamanho_a = strlen(a.Chave);
    int tamanho_b = strlen(b.Chave);
    int menor = (tamanho_a < tamanho_b) ? tamanho_a : tamanho_b;
    (*contador)++;

    TipoIndexAmp Posicao = 0;

    while (Posicao < menor && a.Chave[Posicao] == b.Chave[Posicao])
    {
        (*contador)++;
        (*contador)++;
        Posicao++;
    }

    TipoCaractereDif Dif;
    if (Posicao < menor)
    {
        (*contador)++;
        Dif = (a.Chave[Posicao] >= b.Chave[Posicao]) ? a.Chave[Posicao] : b.Chave[Posicao];
        (*contador)++;
    }
    else
    {
        (*contador)++;
        if (tamanho_a > tamanho_b)
        {
            (*contador)++;
            Dif = a.Chave[Posicao];
        }
        else
        {
            (*contador)++;
            Dif = b.Chave[Posicao];
        }
    }

    IndicePat Indice = {Dif, Posicao};
    return Indice;
}

short EExterno(TipoArvore p)
{
    /* Verifica se p^ e nodo externo */
    return (p->nt == Externo);
}

TipoArvore CriaNoInt(IndicePat i, TipoArvore *Esq, TipoArvore *Dir)
{
    TipoArvore p;
    p = (TipoArvore)malloc(sizeof(TipoPatNo));
    p->nt = Interno;
    p->NO.NInterno.Esq = *Esq;
    p->NO.NInterno.Dir = *Dir;
    p->NO.NInterno.Index = i;
    return p;
}

TipoArvore CriaNoExt(TipoItem k)
{
    TipoArvore p;
    p = (TipoArvore)malloc(sizeof(TipoPatNo));
    p->nt = Externo;
    p->NO.Item = k;
    return p;
}

TipoArvore InsereEntre(TipoItem k, TipoArvore *t, IndicePat i, int contador[])
{
    TipoArvore p;
    if (EExterno(*t) || (i.Posicao < (*t)->NO.NInterno.Index.Posicao))
    {
        (*contador)++;
        (*contador)++;
        p = CriaNoExt(k); /* cria um novo no externo */

        if (Bit(i, k, contador) == 1)
        {
            (*contador)++;
            return (CriaNoInt(i, t, &p));
        }
        else
        {
            (*contador)++;
            return (CriaNoInt(i, &p, t));
        }
    }
    else
    {
        (*contador)++;
        if (Bit((*t)->NO.NInterno.Index, k, contador) == 1)
        {
            (*contador)++;
            (*t)->NO.NInterno.Dir = InsereEntre(k, &(*t)->NO.NInterno.Dir, i, contador);
        }
        else
        {
            (*contador)++;
            (*t)->NO.NInterno.Esq = InsereEntre(k, &(*t)->NO.NInterno.Esq, i, contador);
        }

        return (*t);
    }
}

TipoArvore InserePatricia(TipoItem k, TipoArvore *t, int contador[])
{
    TipoArvore p;

    if (*t == NULL)
    {
        (*contador)++;
        return (CriaNoExt(k));
    }
    else
    {
        (*contador)++;
        p = *t;
        while (!EExterno(p))
        {
            (*contador)++;
            if (Bit(p->NO.NInterno.Index, k, contador) == 1)
            {
                (*contador)++;
                p = p->NO.NInterno.Dir;
            }
            else
            {
                (*contador)++;
                p = p->NO.NInterno.Esq;
            }
        }

        IndicePat i = Compara(k, p->NO.Item, contador);

        if (i.Posicao == strlen(k.Chave) && i.Posicao == strlen(p->NO.Item.Chave))
        {
            (*contador)++;
            (*contador)++;
            // printf("Erro: chave ja esta na arvore\n");
            return (*t);
        }
        else
        {
            (*contador)++;
            return (InsereEntre(k, t, i, contador));
        }
    }
}

void ImprimeRelevanciaPatricia(float *vetorRelevancia, int NDoc)
{
    for (int i = 0; i < NDoc; i++)
    {
        printf("Relevancia Doc. #%d = %.6f\n", i + 1, vetorRelevancia[i]);
    }
}

void PesquisaPatricia(TipoArvore Arvore, Palavra palavras[], int qtdePalavras, int NDoc, int contador[])
{
    float *vetorRelevancia = (float *)malloc(NDoc * sizeof(float));

    for (int i = 0; i < NDoc; i++)
    {
        (*contador)++;
        vetorRelevancia[i] = 0.0;
    }

    for (int p = 0; p < qtdePalavras; p++)
    {
        (*contador)++;

        TipoItem itemBusca;
        strcpy(itemBusca.Chave, palavras[p]);
        FLVazia(&itemBusca.Indices);

        TipoArvore no = Arvore;

        // Busca na Patricia
        while (no != NULL && !EExterno(no))
        {
            (*contador)++;
            if (Bit(no->NO.NInterno.Index, itemBusca, contador) == 1)
            {
                (*contador)++;
                no = no->NO.NInterno.Dir;
            }
            else
            {
                (*contador)++;
                no = no->NO.NInterno.Esq;
            }
        }

        if (no != NULL && strcmp(no->NO.Item.Chave, itemBusca.Chave) == 0)
        {
            (*contador)++;

            // Palavra encontrada — Calcula relevância
            TipoCelula *aux = no->NO.Item.Indices.Primeiro->Prox;

            // Conta DF
            int DF = 0;
            while (aux != NULL)
            {
                DF++;
                aux = aux->Prox;
                (*contador)++;
            }

            aux = no->NO.Item.Indices.Primeiro->Prox;

            while (aux != NULL)
            {
                (*contador)++;

                int idDoc = aux->Item.IdDoc;
                int tf = aux->Item.Qtde;

                float idf = log10((float)NDoc / DF);
                vetorRelevancia[idDoc - 1] += tf * idf;

                aux = aux->Prox;
            }
        }
    }

    // Imprime a relevância total
    printf("PATRICIA:\n");
    ImprimeRelevanciaPatricia(vetorRelevancia, NDoc); // por ser apenas um print não vou contar as comparações dessa função

    free(vetorRelevancia);
}
