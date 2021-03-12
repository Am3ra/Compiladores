%{
void yyerror (char *s);

%}

%start programa

%token IF
%token VAR
%token FLOAT
%token INT
%token ELSE
%token PROGRAM
%token PRINT
%token PLUS 
%token MINUS 
%token TIMES 
%token DIVIDE 
%token LPAREN 
%token RPAREN 
%token SCOLON  
%token LBRACKET 
%token RBRACKET 
%token COMMA 
%token COLON 
%token ASSIGN
%token NE 
%token LT 
%token GT 
%token CTEF 
%token CTEI
%token ID 
%token CTESTRING 

%%

programa : PROGRAM ID SCOLON vars bloque {}
         | PROGRAM ID SCOLON bloque {}
        ;


vars : VAR declaracion {} ;

declaracion : nombre COLON tipo SCOLON  {}
                   | nombre COLON tipo SCOLON declaracion {}
            ;

tipo : INT  {}
     | FLOAT {}
        ;


bloque : LBRACKET estatutos RBRACKET {};

estatutos : estatuto {}
                | estatuto estatutos {}
                ;

estatuto : asignacion {}
                   | condicion {}
                   | escritura {}
                   ;

asignacion : ID ASSIGN expresion SCOLON {};

escritura : PRINT LPAREN contenido RPAREN SCOLON {};


contenido : CTESTRING {}
                | expresion {}
                | CTESTRING COMMA contenido {}
                | expresion COMMA contenido {}
                ;

expresion : exp relop exp {}
                | exp {}
                ;

nombre : ID {}
                | ID COMMA nombre {}
                ;

condicion : IF LPAREN expresion RPAREN bloque SCOLON {}
                    | IF LPAREN expresion RPAREN bloque ELSE bloque SCOLON {}
                    ;


relop : LT  {}
                | GT {}
                | NE {}
                ;

exp : termino {}
            | termino addop exp {}
            ;

addop : PLUS 
                | MINUS 
                ;

termino : factor
                | factor mulop termino
                ;


mulop : TIMES
                | DIVIDE
                ;

 factor : LPAREN expresion RPAREN
                | addop varcte               
                ;

varcte : ID
                | CTEF
                | CTEI
                ;

%%

int main (void) {
    return yyparse();

}

void yyerror(char *s){fprintf (stderr, "%s\n",s);}