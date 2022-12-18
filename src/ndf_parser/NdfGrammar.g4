grammar NdfGrammar;

ndf_file : builtin_type EOF;
builtin_type : boolean | integer | string | builtin_type builtin_type;
boolean : K_TRUE | K_FALSE;
string : STRING;
integer : INT | HEXNUMBER;

// case insnensitivity

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

K_TRUE : T R U E ;
K_FALSE : F A L S E;

// other lexer rules

WS : [ \t\r\n]+ -> skip ;
STRING : '"' ( '\\"' | '\\\'' | . )*? '"' | '\'' ( '\\"' | '\\\'' | . )*? '\'';
INT : '-'? [0-9]+;
HEXNUMBER : '0' X [0-9a-f]+ ;