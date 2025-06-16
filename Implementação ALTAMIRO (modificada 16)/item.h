// O grupo deverá estar identificado no cabeçalho de TODOS os arquivos do código-fonte:
// Jordane Andrade Soares

#ifndef ITEM
#define ITEM
#define TAMANHO_CHAVE 200

typedef char TipoChave[TAMANHO_CHAVE];

#include "lista.h"

typedef struct TipoItem // tipo item é usado na PATRICIA e na HASH
{
    TipoChave Chave;
    TipoLista Indices;
} TipoItem;

#endif
