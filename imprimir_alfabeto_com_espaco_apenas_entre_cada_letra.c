#include <stdio.h>
#include <stdlib.h>

void imprimir (int comeco, int final) {

    // imprimi na tela todos as outras letras antes da letra final
    if (comeco < final) {
        printf("%c-", 'A' + comeco);
        imprimir(comeco + 1, final);
    }

    // imprimi na tela apenas a letra final
    else printf("%c", 'A' + comeco);
}

int main () {
    int comeco = 0;
    int final = 25;
    
    printf ("\n\n\n");
    imprimir (comeco, final);
    printf ("\n\n\n");

    return 0;
}