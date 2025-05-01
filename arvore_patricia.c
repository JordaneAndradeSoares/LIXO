#define D 8 // número de bits considerados na chave (char = 8 bits)
#include <stdio.h>
#include <stdlib.h>

typedef enum {interno, externo} TIPO_NO;

// estrutura da árvore patricia
typedef struct tipo_no_patricia { 

    TIPO_NO nt;

    union {
        struct {
            char index; 
            struct tipo_no_patricia *esquerda, *direita;
        } no_interno;

        char chave;

    } NO;

} TIPO_NO_PATRICIA;

// insere uma nova chave criando um nó interno entre os nós existentes, no nível i
TIPO_NO_PATRICIA* criar_no_interno (int i, TIPO_NO_PATRICIA **esquerda, TIPO_NO_PATRICIA **direita) {
    TIPO_NO_PATRICIA *p;
    p = (TIPO_NO_PATRICIA*) malloc(sizeof(TIPO_NO_PATRICIA)); // acho que o ideal é adicionar uma verificação para checar se o malloc funcionou
    p->nt = interno; p->NO.no_interno.esquerda = *esquerda;
    p->NO.no_interno.direita = *direita; p->NO.no_interno.index = i;
    return p;
}

// cria um nó externo com a chave fornecida
TIPO_NO_PATRICIA* criar_no_externo(char chave) {
    TIPO_NO_PATRICIA *p;
    p = (TIPO_NO_PATRICIA*) malloc(sizeof(TIPO_NO_PATRICIA)); // acho que o ideal é adicionar uma verificação para checar se o malloc funcionou
    p->nt = externo; p->NO.chave = chave; 
    return p;
}

// retorna o bit na posição i (a partir do mais significativo) da chave
char bit(char i, char chave){
    int c, j;

    if (i == 0) return 0;

    else {
        c = chave;
        for (j = 1; j <= D - i; j++) c /= 2;
        return (c & 1);
    }
}

// retorna 1 se o nó for externo ou retorna 0 se caso contrário
short e_externo (TIPO_NO_PATRICIA *p) {
    return (p->nt == externo);
}

// insere entre os nos da arvore patricia
TIPO_NO_PATRICIA* inserir_entre (char chave, TIPO_NO_PATRICIA **t, int i) { 
    TIPO_NO_PATRICIA *p;

    if (e_externo(*t) || i < (*t)->NO.no_interno.index) {
        p = criar_no_externo(chave);

        if (bit(i, chave) == 1)
            return (criar_no_interno(i,t,&p));
        else 
            return (criar_no_interno(i,&p,t));  
    } 
    
    else {
        if (bit((*t)->NO.no_interno.index, chave) == 1)
            (*t)->NO.no_interno.direita = inserir_entre(chave, &(*t)->NO.no_interno.direita, i);
        else
            (*t)->NO.no_interno.esquerda = inserir_entre(chave, &(*t)->NO.no_interno.esquerda, i);
        return (*t);
    }
}

// insere uma chave nova na árvore Patricia, se ela ainda não existir
TIPO_NO_PATRICIA* inserir (char chave, TIPO_NO_PATRICIA **t) {
    TIPO_NO_PATRICIA *p;
    
    if (*t == NULL) 
        return(criar_no_externo(chave));
    else {
        p = *t;
        while (!e_externo(p)){
            if (bit(p->NO.no_interno.index, chave) == 1)
                p = p->NO.no_interno.direita;
            else 
                p = p->NO.no_interno.esquerda;
            } 
    }
    
    int i = 1;
    while ((i <= D) & (bit((int)i, chave) == bit((int)i, p->NO.chave)))
        i++;

    if (i > D) {
        printf ("ERRO! A chave ja esta na arvore\n");
        return (*t);
    } else
        return (inserir_entre(chave, t, i)); 
}

// imprimi a arvore patricia
void imprime_arvore(TIPO_NO_PATRICIA *t, int *j) {
    if (t == NULL) return;
    
    if (e_externo(t)){
        printf("Chave %d: %c\n", *j, t->NO.chave);
        (*j)++;
    } else {
        imprime_arvore(t->NO.no_interno.esquerda, j);
        imprime_arvore(t->NO.no_interno.direita, j);
    }
}

// pesquisa um elemento na arvore patricia
void pesquisa (char chave, TIPO_NO_PATRICIA *t) {
    if (e_externo(t)) {
        if (chave == t->NO.chave)
            printf("Elemento '%c' encontrado\n", chave);
        else 
            printf("Elemento '%c' NAO encontrado\n", chave);
        return;
    }

    if (bit(t->NO.no_interno.index, chave) == 0)
        pesquisa(chave, t->NO.no_interno.esquerda);
    else
        pesquisa(chave, t->NO.no_interno.direita);
}

int main () {

    TIPO_NO_PATRICIA *t = NULL;
    int i = 0, j = 1;
    char conteudo;

    for (i = 0; i < 4; i++) {
        printf("Ensira UMA letra para guardar na arvore: "); 
        scanf(" %c", &conteudo); // o espaço antes do %c é importante para o scanf não pegar o enter quando essa tecla for precionada
        t = inserir(conteudo, &t); 
    }

    printf("\n");
    imprime_arvore(t, &j);

    for (i = 0; i < 4; i++) {
        printf("\nEnsira UMA letra para procurar na arvore: ");
        scanf(" %c", &conteudo); // o espaço antes do %c é importante para o scanf não pegar o enter quando essa tecla for precionada
        pesquisa(conteudo, t);
    }
    
    return 0;
}