
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftPLUSMINUSleftTIMESDIVIDECLASS COLON COMMA CTEF CTEI CTESTRING DIVIDE DO DOT ELSE EQUAL FLOAT FROM FUNC GTHAN ID IF INHERIT INT LBRACE LBRACKET LPAREN LTHAN MAIN MINUS NOTEQ PLUS RBRACE RBRACKET READ RET RETURN RPAREN SAME SEMICOLON STRING THEN TIMES TO VAR WHILE WRITEprograma : declaraciones main declaraciones : var_def declaraciones\n                    | funcion_def declaraciones\n                    | clase_def declaraciones\n                    | empty clase_def : CLASS ID clase_op bloque_clase clase_op : INHERIT ID \n                | empty  bloque_clase : LBRACE op_var op_func RBRACE op_func : funcion_def\n                | empty funcion_def : FUNC ID LPAREN params RPAREN return_option bloque_func op_var : var_def\n                | empty return_option : RET type_simple\n                      | empty  params : ID COLON type_simple params_op\n               | empty params_op : COMMA params\n                    | empty  bloque_func : LBRACE op_var estatutos RBRACE main : MAIN LPAREN RPAREN bloque_func var_def : VAR type_compuesto    ID           SEMICOLON\n                | VAR type_simple       ID op_vardef  SEMICOLON  op_vardef : LBRACKET CTEI RBRACKET \n                  | LBRACKET CTEI RBRACKET LBRACKET CTEI RBRACKET \n                  | empty type_simple : INT\n                    | FLOAT\n                    | STRING  type_compuesto : ID  estatutos : estatuto\n                | estatuto estatutos\n                | empty  estatuto : asignacion\n                | expresion\n                | returns\n                | llamada_funcion SEMICOLON\n                | llamada_objeto SEMICOLON\n                | lectura\n                | escritura\n                | decision\n                | repeticion  asignacion : variable EQUAL expresion SEMICOLON  expresion : expresion binop expresion\n               | plus_minus expresion\n               | LPAREN expresion RPAREN\n               | var_cte  binop : SAME\n              | NOTEQ\n              | GTHAN \n              | LTHAN \n              | PLUS\n              | MINUS\n              | TIMES\n              | DIVIDE plus_minus : PLUS\n                   | MINUS  var_cte : variable\n                | CTEF\n                | CTEI  returns : RETURN expresion SEMICOLON  llamada_funcion : ID LPAREN param_llamada RPAREN  param_llamada : expresion\n                      | expresion COMMA param_llamada\n                      | empty  llamada_objeto : ID DOT ID LPAREN param_llamada RPAREN   lectura : READ LPAREN variable op_lectura RPAREN SEMICOLON  op_lectura : COMMA variable op_lectura \n                   | empty  variable : ID variable_op\n                  | llamada_objeto  variable_op : DOT ID \n                    | LBRACKET expresion RBRACKET \n                    | LBRACKET expresion RBRACKET LBRACKET expresion RBRACKET\n                    | empty\n                     escritura : WRITE LPAREN type_escritura op_escritura RPAREN SEMICOLON  type_escritura : CTESTRING \n                       | expresion  op_escritura : COMMA CTESTRING op_escritura \n                     | COMMA expresion op_escritura\n                     | empty  decision : IF LPAREN expresion RPAREN THEN LBRACE estatutos RBRACE op_decision  op_decision : ELSE LBRACE estatutos RBRACE \n                    | empty  repeticion : condicional \n                   | no_condicional  condicional : WHILE LPAREN expresion RPAREN DO LBRACE estatutos RBRACE  no_condicional : FROM variable EQUAL expresion TO expresion DO LBRACE estatutos RBRACE  empty : '
    
_lr_action_items = {'VAR':([0,3,4,5,31,38,39,42,43,92,94,95,],[7,7,7,7,-23,-6,7,7,-24,-12,-9,-21,]),'FUNC':([0,3,4,5,31,38,39,43,47,48,49,92,94,95,],[8,8,8,8,-23,-6,-90,-24,8,-13,-14,-12,-9,-21,]),'CLASS':([0,3,4,5,31,38,43,92,94,95,],[9,9,9,9,-23,-6,-24,-12,-9,-21,]),'MAIN':([0,2,3,4,5,6,12,13,14,31,38,43,92,94,95,],[-90,11,-90,-90,-90,-5,-2,-3,-4,-23,-6,-24,-12,-9,-21,]),'$end':([1,10,41,95,],[0,-1,-22,-21,]),'ID':([7,8,9,15,16,17,18,19,20,26,28,31,42,43,48,49,50,60,62,63,64,66,67,68,69,70,71,72,73,74,75,76,80,81,82,83,84,85,87,90,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,115,116,117,118,119,120,121,122,123,127,129,130,134,142,144,146,147,148,150,153,160,168,169,171,173,176,177,179,183,184,185,186,188,190,191,193,],[16,21,22,24,-31,25,-28,-29,-30,35,40,-23,-90,-24,-13,-14,76,76,-35,-36,-37,-72,-40,-41,-42,-43,-59,111,111,-48,111,-90,-86,-87,-57,-58,-60,-61,111,35,111,-49,-50,-51,-52,-53,-54,-55,-56,-38,-39,111,-46,-59,-90,-72,111,134,-71,111,-76,111,111,111,111,-45,-47,-62,-73,111,-44,111,111,-74,111,111,111,111,-67,-68,-77,76,76,-75,-90,-88,76,-83,-85,76,-89,-84,]),'INT':([7,45,54,],[18,18,18,]),'FLOAT':([7,45,54,],[19,19,19,]),'STRING':([7,45,54,],[20,20,20,]),'LPAREN':([11,21,31,42,43,48,49,50,60,62,63,64,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,115,117,118,119,121,122,123,127,129,130,134,142,144,146,147,148,153,160,168,169,171,173,176,177,179,183,184,185,186,188,190,191,193,],[23,26,-23,-90,-24,-13,-14,73,73,-35,-36,-37,-72,-40,-41,-42,-43,-59,73,73,-48,73,115,120,121,122,-86,-87,-57,-58,-60,-61,123,73,-49,-50,-51,-52,-53,-54,-55,-56,-38,-39,73,-46,-59,-90,-72,73,-71,73,-76,73,73,73,-45,-47,-62,147,73,-44,73,73,-74,73,73,73,-67,-68,-77,73,73,-75,-90,-88,73,-83,-85,73,-89,-84,]),'COMMA':([18,19,20,52,74,84,85,109,110,111,112,117,119,127,129,132,134,136,137,138,139,148,162,164,165,169,179,],[-28,-29,-30,90,-48,-60,-61,-46,-59,-90,-72,-71,-76,-45,-47,146,-73,150,153,-78,-79,-74,150,153,153,-67,-75,]),'RPAREN':([18,19,20,23,26,36,37,52,74,84,85,89,90,91,109,110,111,112,113,115,117,119,126,127,129,131,132,133,134,136,137,138,139,140,141,146,147,148,149,151,152,154,158,159,162,164,165,169,172,174,175,179,],[-28,-29,-30,30,-90,46,-18,-90,-48,-60,-61,-17,-90,-20,-46,-59,-90,-72,129,-90,-71,-76,-19,-45,-47,145,-64,-66,-73,-90,-90,-78,-79,155,156,-90,-90,-74,161,-70,163,-82,-65,169,-90,-90,-90,-67,-69,-80,-81,-75,]),'LBRACE':([18,19,20,22,27,29,30,40,46,53,55,93,166,167,182,187,],[-28,-29,-30,-90,39,-8,42,-7,-90,42,-16,-15,176,177,185,190,]),'INHERIT':([22,],[28,]),'SEMICOLON':([24,25,32,34,51,65,66,74,84,85,109,110,111,112,114,117,119,127,128,129,134,143,145,148,161,163,169,179,],[31,-90,43,-27,-25,106,107,-48,-60,-61,-46,-59,-90,-72,130,-71,-76,-45,144,-47,-73,-26,-63,-74,171,173,-67,-75,]),'LBRACKET':([25,51,76,111,148,],[33,88,118,118,160,]),'RBRACE':([31,39,42,43,47,48,49,50,56,57,58,59,60,61,62,63,64,66,67,68,69,70,71,74,76,80,81,84,85,92,95,96,106,107,109,110,111,112,117,119,127,129,130,134,144,148,169,171,173,176,177,179,180,181,183,184,185,186,188,189,190,191,192,193,],[-23,-90,-90,-24,-90,-13,-14,-90,94,-10,-11,95,-32,-34,-35,-36,-37,-72,-40,-41,-42,-43,-59,-48,-90,-86,-87,-60,-61,-12,-21,-33,-38,-39,-46,-59,-90,-72,-71,-76,-45,-47,-62,-73,-44,-74,-67,-68,-77,-90,-90,-75,183,184,-90,-88,-90,-83,-85,191,-90,-89,193,-84,]),'RETURN':([31,42,43,48,49,50,60,62,63,64,66,67,68,69,70,71,74,76,80,81,84,85,106,107,109,110,111,112,117,119,127,129,130,134,144,148,169,171,173,176,177,179,183,184,185,186,188,190,191,193,],[-23,-90,-24,-13,-14,75,75,-35,-36,-37,-72,-40,-41,-42,-43,-59,-48,-90,-86,-87,-60,-61,-38,-39,-46,-59,-90,-72,-71,-76,-45,-47,-62,-73,-44,-74,-67,-68,-77,75,75,-75,-90,-88,75,-83,-85,75,-89,-84,]),'READ':([31,42,43,48,49,50,60,62,63,64,66,67,68,69,70,71,74,76,80,81,84,85,106,107,109,110,111,112,117,119,127,129,130,134,144,148,169,171,173,176,177,179,183,184,185,186,188,190,191,193,],[-23,-90,-24,-13,-14,77,77,-35,-36,-37,-72,-40,-41,-42,-43,-59,-48,-90,-86,-87,-60,-61,-38,-39,-46,-59,-90,-72,-71,-76,-45,-47,-62,-73,-44,-74,-67,-68,-77,77,77,-75,-90,-88,77,-83,-85,77,-89,-84,]),'WRITE':([31,42,43,48,49,50,60,62,63,64,66,67,68,69,70,71,74,76,80,81,84,85,106,107,109,110,111,112,117,119,127,129,130,134,144,148,169,171,173,176,177,179,183,184,185,186,188,190,191,193,],[-23,-90,-24,-13,-14,78,78,-35,-36,-37,-72,-40,-41,-42,-43,-59,-48,-90,-86,-87,-60,-61,-38,-39,-46,-59,-90,-72,-71,-76,-45,-47,-62,-73,-44,-74,-67,-68,-77,78,78,-75,-90,-88,78,-83,-85,78,-89,-84,]),'IF':([31,42,43,48,49,50,60,62,63,64,66,67,68,69,70,71,74,76,80,81,84,85,106,107,109,110,111,112,117,119,127,129,130,134,144,148,169,171,173,176,177,179,183,184,185,186,188,190,191,193,],[-23,-90,-24,-13,-14,79,79,-35,-36,-37,-72,-40,-41,-42,-43,-59,-48,-90,-86,-87,-60,-61,-38,-39,-46,-59,-90,-72,-71,-76,-45,-47,-62,-73,-44,-74,-67,-68,-77,79,79,-75,-90,-88,79,-83,-85,79,-89,-84,]),'PLUS':([31,42,43,48,49,50,60,62,63,64,66,67,68,69,70,71,72,73,74,75,76,80,81,82,83,84,85,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,117,118,119,121,122,123,127,128,129,130,132,134,135,139,140,141,142,144,146,147,148,153,157,160,165,168,169,170,171,173,176,177,178,179,183,184,185,186,188,190,191,193,],[-23,-90,-24,-13,-14,82,82,-35,102,-37,-72,-40,-41,-42,-43,-59,82,82,-48,82,-90,-86,-87,-57,-58,-60,-61,82,-49,-50,-51,-52,-53,-54,-55,-56,-38,-39,82,102,-59,-90,-72,102,102,82,-71,82,-76,82,82,82,102,102,-47,-62,102,-73,102,102,102,102,82,-44,82,82,-74,82,102,82,102,82,-67,102,-68,-77,82,82,102,-75,-90,-88,82,-83,-85,82,-89,-84,]),'MINUS':([31,42,43,48,49,50,60,62,63,64,66,67,68,69,70,71,72,73,74,75,76,80,81,82,83,84,85,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,117,118,119,121,122,123,127,128,129,130,132,134,135,139,140,141,142,144,146,147,148,153,157,160,165,168,169,170,171,173,176,177,178,179,183,184,185,186,188,190,191,193,],[-23,-90,-24,-13,-14,83,83,-35,103,-37,-72,-40,-41,-42,-43,-59,83,83,-48,83,-90,-86,-87,-57,-58,-60,-61,83,-49,-50,-51,-52,-53,-54,-55,-56,-38,-39,83,103,-59,-90,-72,103,103,83,-71,83,-76,83,83,83,103,103,-47,-62,103,-73,103,103,103,103,83,-44,83,83,-74,83,103,83,103,83,-67,103,-68,-77,83,83,103,-75,-90,-88,83,-83,-85,83,-89,-84,]),'CTEF':([31,42,43,48,49,50,60,62,63,64,66,67,68,69,70,71,72,73,74,75,76,80,81,82,83,84,85,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,115,117,118,119,121,122,123,127,129,130,134,142,144,146,147,148,153,160,168,169,171,173,176,177,179,183,184,185,186,188,190,191,193,],[-23,-90,-24,-13,-14,84,84,-35,-36,-37,-72,-40,-41,-42,-43,-59,84,84,-48,84,-90,-86,-87,-57,-58,-60,-61,84,-49,-50,-51,-52,-53,-54,-55,-56,-38,-39,84,-46,-59,-90,-72,84,-71,84,-76,84,84,84,-45,-47,-62,-73,84,-44,84,84,-74,84,84,84,-67,-68,-77,84,84,-75,-90,-88,84,-83,-85,84,-89,-84,]),'CTEI':([31,33,42,43,48,49,50,60,62,63,64,66,67,68,69,70,71,72,73,74,75,76,80,81,82,83,84,85,88,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,115,117,118,119,121,122,123,127,129,130,134,142,144,146,147,148,153,160,168,169,171,173,176,177,179,183,184,185,186,188,190,191,193,],[-23,44,-90,-24,-13,-14,85,85,-35,-36,-37,-72,-40,-41,-42,-43,-59,85,85,-48,85,-90,-86,-87,-57,-58,-60,-61,125,85,-49,-50,-51,-52,-53,-54,-55,-56,-38,-39,85,-46,-59,-90,-72,85,-71,85,-76,85,85,85,-45,-47,-62,-73,85,-44,85,85,-74,85,85,85,-67,-68,-77,85,85,-75,-90,-88,85,-83,-85,85,-89,-84,]),'WHILE':([31,42,43,48,49,50,60,62,63,64,66,67,68,69,70,71,74,76,80,81,84,85,106,107,109,110,111,112,117,119,127,129,130,134,144,148,169,171,173,176,177,179,183,184,185,186,188,190,191,193,],[-23,-90,-24,-13,-14,86,86,-35,-36,-37,-72,-40,-41,-42,-43,-59,-48,-90,-86,-87,-60,-61,-38,-39,-46,-59,-90,-72,-71,-76,-45,-47,-62,-73,-44,-74,-67,-68,-77,86,86,-75,-90,-88,86,-83,-85,86,-89,-84,]),'FROM':([31,42,43,48,49,50,60,62,63,64,66,67,68,69,70,71,74,76,80,81,84,85,106,107,109,110,111,112,117,119,127,129,130,134,144,148,169,171,173,176,177,179,183,184,185,186,188,190,191,193,],[-23,-90,-24,-13,-14,87,87,-35,-36,-37,-72,-40,-41,-42,-43,-59,-48,-90,-86,-87,-60,-61,-38,-39,-46,-59,-90,-72,-71,-76,-45,-47,-62,-73,-44,-74,-67,-68,-77,87,87,-75,-90,-88,87,-83,-85,87,-89,-84,]),'COLON':([35,],[45,]),'RBRACKET':([44,74,84,85,109,110,111,112,117,119,125,127,129,134,135,148,169,170,179,],[51,-48,-60,-61,-46,-59,-90,-72,-71,-76,143,-45,-47,-73,148,-74,-67,179,-75,]),'RET':([46,],[54,]),'SAME':([63,66,71,74,76,84,85,109,110,111,112,113,114,117,119,127,128,129,132,134,135,139,140,141,148,157,165,169,170,178,179,],[98,-72,-59,-48,-90,-60,-61,98,-59,-90,-72,98,98,-71,-76,98,98,-47,98,-73,98,98,98,98,-74,98,98,-67,98,98,-75,]),'NOTEQ':([63,66,71,74,76,84,85,109,110,111,112,113,114,117,119,127,128,129,132,134,135,139,140,141,148,157,165,169,170,178,179,],[99,-72,-59,-48,-90,-60,-61,99,-59,-90,-72,99,99,-71,-76,99,99,-47,99,-73,99,99,99,99,-74,99,99,-67,99,99,-75,]),'GTHAN':([63,66,71,74,76,84,85,109,110,111,112,113,114,117,119,127,128,129,132,134,135,139,140,141,148,157,165,169,170,178,179,],[100,-72,-59,-48,-90,-60,-61,100,-59,-90,-72,100,100,-71,-76,100,100,-47,100,-73,100,100,100,100,-74,100,100,-67,100,100,-75,]),'LTHAN':([63,66,71,74,76,84,85,109,110,111,112,113,114,117,119,127,128,129,132,134,135,139,140,141,148,157,165,169,170,178,179,],[101,-72,-59,-48,-90,-60,-61,101,-59,-90,-72,101,101,-71,-76,101,101,-47,101,-73,101,101,101,101,-74,101,101,-67,101,101,-75,]),'TIMES':([63,66,71,74,76,84,85,109,110,111,112,113,114,117,119,127,128,129,132,134,135,139,140,141,148,157,165,169,170,178,179,],[104,-72,-59,-48,-90,-60,-61,104,-59,-90,-72,104,104,-71,-76,104,104,-47,104,-73,104,104,104,104,-74,104,104,-67,104,104,-75,]),'DIVIDE':([63,66,71,74,76,84,85,109,110,111,112,113,114,117,119,127,128,129,132,134,135,139,140,141,148,157,165,169,170,178,179,],[105,-72,-59,-48,-90,-60,-61,105,-59,-90,-72,105,105,-71,-76,105,105,-47,105,-73,105,105,105,105,-74,105,105,-67,105,105,-75,]),'EQUAL':([66,71,76,111,112,117,119,124,134,148,169,179,],[-72,108,-90,-90,-72,-71,-76,142,-73,-74,-67,-75,]),'TO':([74,84,85,109,110,111,112,117,119,127,129,134,148,157,169,179,],[-48,-60,-61,-46,-59,-90,-72,-71,-76,-45,-47,-73,-74,168,-67,-75,]),'DO':([74,84,85,109,110,111,112,117,119,127,129,134,148,156,169,178,179,],[-48,-60,-61,-46,-59,-90,-72,-71,-76,-45,-47,-73,-74,167,-67,182,-75,]),'DOT':([76,111,],[116,116,]),'CTESTRING':([121,153,],[138,164,]),'THEN':([155,],[166,]),'ELSE':([183,],[187,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'programa':([0,],[1,]),'declaraciones':([0,3,4,5,],[2,12,13,14,]),'var_def':([0,3,4,5,39,42,],[3,3,3,3,48,48,]),'funcion_def':([0,3,4,5,47,],[4,4,4,4,57,]),'clase_def':([0,3,4,5,],[5,5,5,5,]),'empty':([0,3,4,5,22,25,26,39,42,46,47,50,52,60,76,90,111,115,136,137,146,147,162,164,165,176,177,183,185,190,],[6,6,6,6,29,34,37,49,49,55,58,61,91,61,119,37,119,133,151,154,133,133,151,154,154,61,61,188,61,61,]),'main':([2,],[10,]),'type_compuesto':([7,],[15,]),'type_simple':([7,45,54,],[17,52,93,]),'clase_op':([22,],[27,]),'op_vardef':([25,],[32,]),'params':([26,90,],[36,126,]),'bloque_clase':([27,],[38,]),'bloque_func':([30,53,],[41,92,]),'op_var':([39,42,],[47,50,]),'return_option':([46,],[53,]),'op_func':([47,],[56,]),'estatutos':([50,60,176,177,185,190,],[59,96,180,181,189,192,]),'estatuto':([50,60,176,177,185,190,],[60,60,60,60,60,60,]),'asignacion':([50,60,176,177,185,190,],[62,62,62,62,62,62,]),'expresion':([50,60,72,73,75,97,108,115,118,121,122,123,142,146,147,153,160,168,176,177,185,190,],[63,63,109,113,114,127,128,132,135,139,140,141,157,132,132,165,170,178,63,63,63,63,]),'returns':([50,60,176,177,185,190,],[64,64,64,64,64,64,]),'llamada_funcion':([50,60,176,177,185,190,],[65,65,65,65,65,65,]),'llamada_objeto':([50,60,72,73,75,87,97,108,115,118,120,121,122,123,142,146,147,150,153,160,168,176,177,185,190,],[66,66,112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,66,66,66,66,]),'lectura':([50,60,176,177,185,190,],[67,67,67,67,67,67,]),'escritura':([50,60,176,177,185,190,],[68,68,68,68,68,68,]),'decision':([50,60,176,177,185,190,],[69,69,69,69,69,69,]),'repeticion':([50,60,176,177,185,190,],[70,70,70,70,70,70,]),'variable':([50,60,72,73,75,87,97,108,115,118,120,121,122,123,142,146,147,150,153,160,168,176,177,185,190,],[71,71,110,110,110,124,110,110,110,110,136,110,110,110,110,110,110,162,110,110,110,71,71,71,71,]),'plus_minus':([50,60,72,73,75,97,108,115,118,121,122,123,142,146,147,153,160,168,176,177,185,190,],[72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,]),'var_cte':([50,60,72,73,75,97,108,115,118,121,122,123,142,146,147,153,160,168,176,177,185,190,],[74,74,74,74,74,74,74,74,74,74,74,74,74,74,74,74,74,74,74,74,74,74,]),'condicional':([50,60,176,177,185,190,],[80,80,80,80,80,80,]),'no_condicional':([50,60,176,177,185,190,],[81,81,81,81,81,81,]),'params_op':([52,],[89,]),'binop':([63,109,113,114,127,128,132,135,139,140,141,157,165,170,178,],[97,97,97,97,97,97,97,97,97,97,97,97,97,97,97,]),'variable_op':([76,111,],[117,117,]),'param_llamada':([115,146,147,],[131,158,159,]),'type_escritura':([121,],[137,]),'op_lectura':([136,162,],[149,172,]),'op_escritura':([137,164,165,],[152,174,175,]),'op_decision':([183,],[186,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> programa","S'",1,None,None,None),
  ('programa -> declaraciones main','programa',2,'p_programa','parser.py',58),
  ('declaraciones -> var_def declaraciones','declaraciones',2,'p_declaraciones','parser.py',63),
  ('declaraciones -> funcion_def declaraciones','declaraciones',2,'p_declaraciones','parser.py',64),
  ('declaraciones -> clase_def declaraciones','declaraciones',2,'p_declaraciones','parser.py',65),
  ('declaraciones -> empty','declaraciones',1,'p_declaraciones','parser.py',66),
  ('clase_def -> CLASS ID clase_op bloque_clase','clase_def',4,'p_clase_def','parser.py',74),
  ('clase_op -> INHERIT ID','clase_op',2,'p_clase_op','parser.py',79),
  ('clase_op -> empty','clase_op',1,'p_clase_op','parser.py',80),
  ('bloque_clase -> LBRACE op_var op_func RBRACE','bloque_clase',4,'p_bloque_clase','parser.py',88),
  ('op_func -> funcion_def','op_func',1,'p_op_func','parser.py',93),
  ('op_func -> empty','op_func',1,'p_op_func','parser.py',94),
  ('funcion_def -> FUNC ID LPAREN params RPAREN return_option bloque_func','funcion_def',7,'p_funcion_def','parser.py',99),
  ('op_var -> var_def','op_var',1,'p_op_var','parser.py',104),
  ('op_var -> empty','op_var',1,'p_op_var','parser.py',105),
  ('return_option -> RET type_simple','return_option',2,'p_return_option','parser.py',110),
  ('return_option -> empty','return_option',1,'p_return_option','parser.py',111),
  ('params -> ID COLON type_simple params_op','params',4,'p_params','parser.py',120),
  ('params -> empty','params',1,'p_params','parser.py',121),
  ('params_op -> COMMA params','params_op',2,'p_params_op','parser.py',128),
  ('params_op -> empty','params_op',1,'p_params_op','parser.py',129),
  ('bloque_func -> LBRACE op_var estatutos RBRACE','bloque_func',4,'p_bloque_func','parser.py',137),
  ('main -> MAIN LPAREN RPAREN bloque_func','main',4,'p_main','parser.py',142),
  ('var_def -> VAR type_compuesto ID SEMICOLON','var_def',4,'p_var_def','parser.py',161),
  ('var_def -> VAR type_simple ID op_vardef SEMICOLON','var_def',5,'p_var_def','parser.py',162),
  ('op_vardef -> LBRACKET CTEI RBRACKET','op_vardef',3,'p_op_vardef','parser.py',172),
  ('op_vardef -> LBRACKET CTEI RBRACKET LBRACKET CTEI RBRACKET','op_vardef',6,'p_op_vardef','parser.py',173),
  ('op_vardef -> empty','op_vardef',1,'p_op_vardef','parser.py',174),
  ('type_simple -> INT','type_simple',1,'p_type_simple','parser.py',184),
  ('type_simple -> FLOAT','type_simple',1,'p_type_simple','parser.py',185),
  ('type_simple -> STRING','type_simple',1,'p_type_simple','parser.py',186),
  ('type_compuesto -> ID','type_compuesto',1,'p_type_compuesto','parser.py',191),
  ('estatutos -> estatuto','estatutos',1,'p_estatutos','parser.py',196),
  ('estatutos -> estatuto estatutos','estatutos',2,'p_estatutos','parser.py',197),
  ('estatutos -> empty','estatutos',1,'p_estatutos','parser.py',198),
  ('estatuto -> asignacion','estatuto',1,'p_estatuto','parser.py',211),
  ('estatuto -> expresion','estatuto',1,'p_estatuto','parser.py',212),
  ('estatuto -> returns','estatuto',1,'p_estatuto','parser.py',213),
  ('estatuto -> llamada_funcion SEMICOLON','estatuto',2,'p_estatuto','parser.py',214),
  ('estatuto -> llamada_objeto SEMICOLON','estatuto',2,'p_estatuto','parser.py',215),
  ('estatuto -> lectura','estatuto',1,'p_estatuto','parser.py',216),
  ('estatuto -> escritura','estatuto',1,'p_estatuto','parser.py',217),
  ('estatuto -> decision','estatuto',1,'p_estatuto','parser.py',218),
  ('estatuto -> repeticion','estatuto',1,'p_estatuto','parser.py',219),
  ('asignacion -> variable EQUAL expresion SEMICOLON','asignacion',4,'p_asignacion','parser.py',224),
  ('expresion -> expresion binop expresion','expresion',3,'p_expresion','parser.py',261),
  ('expresion -> plus_minus expresion','expresion',2,'p_expresion','parser.py',262),
  ('expresion -> LPAREN expresion RPAREN','expresion',3,'p_expresion','parser.py',263),
  ('expresion -> var_cte','expresion',1,'p_expresion','parser.py',264),
  ('binop -> SAME','binop',1,'p_binop','parser.py',275),
  ('binop -> NOTEQ','binop',1,'p_binop','parser.py',276),
  ('binop -> GTHAN','binop',1,'p_binop','parser.py',277),
  ('binop -> LTHAN','binop',1,'p_binop','parser.py',278),
  ('binop -> PLUS','binop',1,'p_binop','parser.py',279),
  ('binop -> MINUS','binop',1,'p_binop','parser.py',280),
  ('binop -> TIMES','binop',1,'p_binop','parser.py',281),
  ('binop -> DIVIDE','binop',1,'p_binop','parser.py',282),
  ('plus_minus -> PLUS','plus_minus',1,'p_plus_minus','parser.py',287),
  ('plus_minus -> MINUS','plus_minus',1,'p_plus_minus','parser.py',288),
  ('var_cte -> variable','var_cte',1,'p_var_cte','parser.py',293),
  ('var_cte -> CTEF','var_cte',1,'p_var_cte','parser.py',294),
  ('var_cte -> CTEI','var_cte',1,'p_var_cte','parser.py',295),
  ('returns -> RETURN expresion SEMICOLON','returns',3,'p_returns','parser.py',301),
  ('llamada_funcion -> ID LPAREN param_llamada RPAREN','llamada_funcion',4,'p_llamada_funcion','parser.py',308),
  ('param_llamada -> expresion','param_llamada',1,'p_param_llamada','parser.py',322),
  ('param_llamada -> expresion COMMA param_llamada','param_llamada',3,'p_param_llamada','parser.py',323),
  ('param_llamada -> empty','param_llamada',1,'p_param_llamada','parser.py',324),
  ('llamada_objeto -> ID DOT ID LPAREN param_llamada RPAREN','llamada_objeto',6,'p_llamada_objeto','parser.py',335),
  ('lectura -> READ LPAREN variable op_lectura RPAREN SEMICOLON','lectura',6,'p_lectura','parser.py',341),
  ('op_lectura -> COMMA variable op_lectura','op_lectura',3,'p_op_lectura','parser.py',346),
  ('op_lectura -> empty','op_lectura',1,'p_op_lectura','parser.py',347),
  ('variable -> ID variable_op','variable',2,'p_variable','parser.py',357),
  ('variable -> llamada_objeto','variable',1,'p_variable','parser.py',358),
  ('variable_op -> DOT ID','variable_op',2,'p_variable_op','parser.py',366),
  ('variable_op -> LBRACKET expresion RBRACKET','variable_op',3,'p_variable_op','parser.py',367),
  ('variable_op -> LBRACKET expresion RBRACKET LBRACKET expresion RBRACKET','variable_op',6,'p_variable_op','parser.py',368),
  ('variable_op -> empty','variable_op',1,'p_variable_op','parser.py',369),
  ('escritura -> WRITE LPAREN type_escritura op_escritura RPAREN SEMICOLON','escritura',6,'p_escritura','parser.py',400),
  ('type_escritura -> CTESTRING','type_escritura',1,'p_type_escritura','parser.py',405),
  ('type_escritura -> expresion','type_escritura',1,'p_type_escritura','parser.py',406),
  ('op_escritura -> COMMA CTESTRING op_escritura','op_escritura',3,'p_op_escritura','parser.py',411),
  ('op_escritura -> COMMA expresion op_escritura','op_escritura',3,'p_op_escritura','parser.py',412),
  ('op_escritura -> empty','op_escritura',1,'p_op_escritura','parser.py',413),
  ('decision -> IF LPAREN expresion RPAREN THEN LBRACE estatutos RBRACE op_decision','decision',9,'p_decision','parser.py',421),
  ('op_decision -> ELSE LBRACE estatutos RBRACE','op_decision',4,'p_op_decision','parser.py',426),
  ('op_decision -> empty','op_decision',1,'p_op_decision','parser.py',427),
  ('repeticion -> condicional','repeticion',1,'p_repeticion','parser.py',435),
  ('repeticion -> no_condicional','repeticion',1,'p_repeticion','parser.py',436),
  ('condicional -> WHILE LPAREN expresion RPAREN DO LBRACE estatutos RBRACE','condicional',8,'p_condicional','parser.py',441),
  ('no_condicional -> FROM variable EQUAL expresion TO expresion DO LBRACE estatutos RBRACE','no_condicional',10,'p_no_condicional','parser.py',446),
  ('empty -> <empty>','empty',0,'p_empty','parser.py',461),
]
