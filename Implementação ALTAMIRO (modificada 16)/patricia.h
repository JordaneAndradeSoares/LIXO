// O grupo deverá estar identificado no cabeçalho de TODOS os arquivos do código-fonte:
// Jordane Andrade Soares

#ifndef PATRICIA
#define PATRICIA

#include "item.h"
#include "palavra.h"

#define D 8 /* depende de TipoChave */

typedef size_t TipoIndexAmp;
typedef unsigned char TipoDib;

typedef char TipoCaractereDif;

typedef enum
{
    Interno,
    Externo
} TipoNo;

typedef struct TipoPatNo *TipoArvore;

typedef struct IndicePat
{
    TipoCaractereDif Letra;
    TipoIndexAmp Posicao;
} IndicePat;

typedef struct TipoPatNo
{
    TipoNo nt;
    union
    {
        struct
        {
            IndicePat Index;
            TipoArvore Esq, Dir;
        } NInterno;
        TipoItem Item;
    } NO;
} TipoPatNo;

void ImprimePatricia(TipoArvore p);
TipoDib Bit(IndicePat i, TipoItem k, int contador[]);
short EExterno(TipoArvore p);
TipoArvore CriaNoInt(IndicePat i, TipoArvore *Esq, TipoArvore *Dir);
TipoArvore CriaNoExt(TipoItem k);
TipoArvore InsereEntre(TipoItem k, TipoArvore *t, IndicePat i, int contador[]);
TipoArvore InserePatricia(TipoItem k, TipoArvore *t, int contador[]);

void ImprimeRelevanciaPatricia(float *vetorRelevancia, int NDoc);
void PesquisaPatricia(TipoArvore Arvore, Palavra palavras[], int qtdePalavras, int NDoc, int contador[]);

#endif
