%{

#include "scanner.h"

%}

%%
"if"        return IF;
"int"       return INT;
"print"     return PRINT;
"else"      return ELSE ;
"var"       return VAR;
"float"      return FLOAT ;
"program"   return PROGRAM ;

\+            return PLUS ;
\-            return MINUS ;
\/            return TIMES ;
\*            return DIVIDE ;
\(           return LPAREN ;
\)           return RPAREN ;
;          return SCOLON  ;
\{           return LBRACKET ;
\}          return RBRACKET ;
\,            return COMMA ;
\:            return COLON ;
\=            return ASSIGN;
\<\>            return NE ;
\<            return LT ;
\>           return GT ;
[1-9][0-9]*.[0-9]*            return CTEF ;
[1-9][0-9]*            return CTEI;
[a-zA-Z]+            return ID ;
\"[a-zA-Z]*\"            return CTESTRING;
.           printf("UNEXPECTED TOKEN");

%%
int yywrap(void)
{
    return 1;
}