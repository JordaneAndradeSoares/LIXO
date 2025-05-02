#define tamanho_fixo 150

#include <stdio.h>
#include <stdlib.h>

// aparentemente o union não gosta de mudar de nome
union union_union_inteiro { int inteiro; };
union union_union_float { float decimal; };
union union_union_char { char caracter; };

union union_union_vetor_inteiro { int vetor_inteiro[tamanho_fixo]; };
union union_union_vetor_float { float vetor_decimal[tamanho_fixo]; };
union union_union_vetor_char { char vetor_caracter[tamanho_fixo]; };

union union_union { union union_union_inteiro INTEIRO; union union_union_float DECIMAL; union union_union_char CARACTER; }; 
union union_union_vetor { union union_union_vetor_inteiro INTEIROS; union union_union_vetor_float DECIMAIS; union union_union_vetor_char CARACTERES; };

void escreve () {
    printf("\n\n----------------------------------------------------------\n\n");
}

int main () {

    union union_union union_union; // versao simples
    union union_union_vetor union_union_vetor; // versao dos vetores
   
    // inteiro
    escreve ();
    printf("Inteiros:\n\n");

    union_union.INTEIRO.inteiro = 0;
    printf("%d\n", union_union.INTEIRO.inteiro);

    for (int i = 0; i < tamanho_fixo; i++) union_union_vetor.INTEIROS.vetor_inteiro[i] = i + 1;
    for (int i = 0; i < tamanho_fixo; i++) printf("%d; ", union_union_vetor.INTEIROS.vetor_inteiro[i]);
    
    // decimal
    escreve ();
    printf("Decimais:\n\n");

    union_union.DECIMAL.decimal = 0.5;
    printf("%.1f\n", union_union.DECIMAL.decimal);

    for (int i = 0; i < tamanho_fixo; i++) union_union_vetor.DECIMAIS.vetor_decimal[i] = i + 0.5;
    for (int i = 0; i < tamanho_fixo; i++) printf("%.1f; ", union_union_vetor.DECIMAIS.vetor_decimal[i]);

    // char
    escreve ();
    printf("Caracteres:\n\n");

    union_union.CARACTER.caracter = 'A'; // precisar usar aspas SIMPLES
    printf("%c\n", union_union.CARACTER.caracter);

    for (int i = 0; i < tamanho_fixo; i++) union_union_vetor.CARACTERES.vetor_caracter[i] = 'A' + i; // precisar usar aspas SIMPLES; 'A' + i = A, B, C, D, E...
    for (int i = 0; i < tamanho_fixo; i++) printf("%c; ", union_union_vetor.CARACTERES.vetor_caracter[i]);

    escreve ();
    return 0;
}