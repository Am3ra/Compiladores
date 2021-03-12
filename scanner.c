#include <stdio.h>
#include "scanner.h"

extern int yylex();
extern int yylineno;
extern char *yytext;

char *names[] = {NULL, 'PLUS',
                 'MINUS',
                 'TIMES',
                 'DIVIDE',
                 'LPAREN',
                 'RPAREN',
                 'SCOLON',
                 'LBRACKET',
                 'RBRACKET',
                 'COMMA',
                 'COLON',
                 'ASSIGN',
                 'NE',
                 'LT',
                 'GT',
                 'CTEF',
                 'CTEI',
                 'ID',
                 'CTESTRING'};


int main(int argc, char const *argv[])
{
    int ntoken, vtoken;
    ntoken = yylex();
    while(ntoken){
        printf("%d\n",ntoken);// probar que valor regresa con la temrinal
        ntoken = yylex();
    }
    return 0;
}
