// O grupo deverá estar identificado no cabeçalho de TODOS os arquivos do código-fonte:
// Jordane Andrade Soares

#include <stdlib.h>
#include <stdio.h>
#include "lista.h"
#define MAX 10

void FLVazia(TipoLista *Lista)
{
    Lista->Primeiro = (TipoApontador)malloc(sizeof(TipoCelula));
    Lista->Ultimo = Lista->Primeiro;
    Lista->Primeiro->Prox = NULL;
}

int Vazia(TipoLista Lista)
{
    return (Lista.Primeiro == Lista.Ultimo);
}

void Insere(IndiceInvertido x, TipoLista *Lista, int *contador)
{
    if (!Vazia(*Lista))
    {
        (*contador)++;
        TipoApontador auxiliar = Lista->Primeiro->Prox;

        while (auxiliar != NULL && auxiliar->Item.IdDoc != x.IdDoc)
        {
            (*contador)++;
            (*contador)++;
            auxiliar = auxiliar->Prox;
        }

        if (auxiliar)
        {
            (*contador)++;
            auxiliar->Item.Qtde++;
            return;
        }
    }

    Lista->Ultimo->Prox = (TipoApontador)malloc(sizeof(TipoCelula));
    Lista->Ultimo = Lista->Ultimo->Prox;
    Lista->Ultimo->Item = x;
    Lista->Ultimo->Prox = NULL;
}

void Retira(TipoApontador p, TipoLista *Lista, IndiceInvertido *Item)
{ /*  ---   Obs.: o item a ser retirado e  o seguinte ao apontado por  p --- */
    TipoApontador q;
    if (Vazia(*Lista) || p == NULL || p->Prox == NULL)
    {
        printf(" Erro   Lista vazia ou posi  c   a o n  a o existe\n");
        return;
    }
    q = p->Prox;
    *Item = q->Item;
    p->Prox = q->Prox;
    if (p->Prox == NULL)
        Lista->Ultimo = p;
    free(q);
}

void Imprime(TipoLista Lista)
{
    TipoApontador Aux;
    Aux = Lista.Primeiro->Prox;
    while (Aux != NULL)
    {
        printf("(%d, %d) ", Aux->Item.Qtde, Aux->Item.IdDoc);
        Aux = Aux->Prox;
    }
}