// O grupo deverá estar identificado no cabeçalho de TODOS os arquivos do código-fonte:
// Jordane Andrade Soares

#ifndef LISTA
#define LISTA

#include "indice.h"

typedef struct TipoCelula *TipoApontador;

typedef struct TipoCelula
{
    IndiceInvertido Item;
    TipoApontador Prox;
} TipoCelula;

typedef struct
{
    TipoApontador Primeiro, Ultimo;
} TipoLista;

void FLVazia(TipoLista *Lista);
int Vazia(TipoLista Lista);
void Insere(IndiceInvertido x, TipoLista *Lista, int contador[]);
void Retira(TipoApontador p, TipoLista *Lista, IndiceInvertido *Item);
void Imprime(TipoLista Lista);

#endif
