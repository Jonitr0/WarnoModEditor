grammar NdfGrammar;

// --- parser rules --- //

// grammar structure

ndf_file : block* EOF;
block : assignment;
assignment : id K_IS builtin_type;
id : ID (':' builtin_type)?;

// builtin types

builtin_type : boolean | string | integer | float | pair | vector | map | builtin_type builtin_type;
boolean : K_TRUE | K_FALSE;
string : STRING;
integer : INT | HEXNUMBER;
float: FLOAT;
pair: '(' builtin_type ',' builtin_type ')';
vector: '[' (builtin_type (',' builtin_type)* ','?)? ']';
map: K_MAP '[' (pair (',' pair)* ','?)? ']';

// --- lexer rules --- //

// keywords

K_TRUE : T R U E ;
K_FALSE : F A L S E;
K_MAP : M A P;
K_IS : I S;

// data types

STRING : '"' ( '\\"' | . )*? '"' | '\'' ( '\\\'' | . )*? '\'';
INT : '-'? [0-9]+;
FLOAT: '-'? ( [0-9]+'.'[0-9]* | [0-9]*'.'[0-9]+ );
HEXNUMBER : '0' X [0-9a-f]+;

// other lexer rules

ID : [a-zA-Z0-9]+ ;
WS : [ \t\r\n]+ -> skip ;
COMMENT : '//' (.*? [\r\n] | ~[\r\n]*? EOF) -> skip ;

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