// O grupo deverá estar identificado no cabeçalho de TODOS os arquivos do código-fonte:
// Jordane Andrade Soares

#ifndef HASH
#define HASH

#include "item.h"
#include "palavra.h"

#define M 50
#define N 200
#define TAMALFABETO 256

typedef unsigned TipoPesos[N][TAMALFABETO];
typedef unsigned int TipoIndice;
typedef struct TipoCelulaHash *TipoApontadorHash;
typedef struct TipoCelulaHash
{
    TipoItem Item;
    TipoApontadorHash Prox;
} TipoCelulaHash;

typedef struct TipoListaHash
{
    TipoCelulaHash *Primeiro, *Ultimo;
} TipoListaHash;

typedef TipoListaHash TipoDicionario[M];

void ImpHash(TipoListaHash Lista);
void ImprimeHash(TipoDicionario Tabela);
void FLVaziaHash(TipoListaHash *Lista);
short VaziaHash(TipoListaHash Lista);
void InsHash(TipoItem x, TipoListaHash *Lista);
void RetHash(TipoApontadorHash p, TipoListaHash *Lista, TipoItem *Item);
void GeraPesosHash(TipoPesos p);
TipoIndice Hash(TipoChave Chave, TipoPesos p, int *contador);
void InicializaHash(TipoDicionario T);
TipoApontadorHash PesquisaHash(TipoChave Ch, TipoPesos p, TipoDicionario T, int *contador);
void InsereHash(TipoItem x, TipoPesos p, TipoDicionario T, int *contador);
void RetiraHash(TipoItem x, TipoPesos p, TipoDicionario T, int *contador);
int ContaElementosHash(TipoDicionario Tabela);
void PreencheVetorHash(TipoDicionario Tabela, TipoItem *vetor);
int comparaChave(const void *a, const void *b);
void ImprimeVetorHash(TipoItem *vetor, int tamanho);
void ImprimeOrdenado(TipoDicionario Tabela);
float WIJ(TipoDicionario Tabela, TipoPesos Pesos, Palavra Palavra, int Doc, int QtdeDocs, int *contador);
float R(TipoDicionario Tabela, TipoPesos Pesos, Palavra *ListaPalavras, int Tamanho, int Doc, int QtdeDocs, int *contador);
float *TFIDFHash(TipoDicionario Tabela, TipoPesos Pesos, Palavra *ListaPalavras, int Tamanho, int QtdeDocs, int *contador);

#endif