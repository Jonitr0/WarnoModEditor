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

// for case insensitivity

fragment A : [aA];
fragment B : [bB];
fragment C : [cC];
fragment D : [dD];
fragment E : [eE];
fragment F : [fF];
fragment G : [gG];
fragment H : [hH];
fragment I : [iI];
fragment J : [jJ];
fragment K : [kK];
fragment L : [lL];
fragment M : [mM];
fragment N : [nN];
fragment O : [oO];
fragment P : [pP];
fragment Q : [qQ];
fragment R : [rR];
fragment S : [sS];
fragment T : [tT];
fragment U : [uU];
fragment V : [vV];
fragment W : [wW];
fragment X : [xX];
fragment Y : [yY];
fragment Z : [zZ];

// keywords

K_EXPORT : E X P O R T;
K_IS : I S;
K_TEMPLATE : T E M P L A T E;
K_UNNAMED : U N A M E D;
K_NIL : N I L;
K_PRIVATE : P R I V A T E;
K_INT : I N T;
K_STRING : S T R I N G;
K_TRUE : T R U E;
K_FALSE : F A L S E;
K_DIV : D I V;
K_MAP : M A P;

// simple types

T_BOOLEAN : ('true','false');

// TODO: define chars (UTF-8 without whitespaces and special chars)