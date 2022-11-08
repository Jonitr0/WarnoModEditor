grammar ndf_grammar;
expr: left=expr op=('*'|'/') right=expr        # InfixExpr
    | left=expr op=('+'|'-') right=expr        # InfixExpr
    | atom=INT                                 # NumberExpr
    | '(' expr ')'                             # ParenExpr
    | atom=HELLO                               # HelloExpr
    | atom=BYE                                 # ByeExpr
    ;

HELLO: ('hello'|'hi')  ;
BYE  : ('bye'| 'tata') ;
INT  : [0-9]+         ;
WS   : [ \t]+ -> skip ;