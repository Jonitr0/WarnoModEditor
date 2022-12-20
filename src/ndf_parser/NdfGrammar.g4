 grammar NdfGrammar;

// --- parser rules --- //

// general structure

ndf_file : block* EOF;
block : assignment;
assignment : id K_IS r_value;
r_value : arithmetic | concatination | builtin_type_value;
id : ID (':' builtin_type_label)?;

// operations

arithmetic : '(' arithmetic ')' | arithmetic OP arithmetic | int_value | float_value;
concatination : concatination '+' concatination | string_value | map_value | vector_value;

// builtin types: labels

builtin_type_label : K_BOOL | K_STRING | K_INT | K_FLOAT | pair_label | list_label | map_label;
pair_label : K_PAIR '<' builtin_type_label ',' builtin_type_label '>';
list_label : K_LIST '<' builtin_type_label '>';
map_label : K_MAP '<' builtin_type_label ',' builtin_type_label '>';

// builtin types: values

builtin_type_value : bool_value | string_value | int_value | float_value | pair_value | vector_value | map_value;
bool_value : K_TRUE | K_FALSE;
string_value : STRING;
int_value : INT | HEXNUMBER;
float_value: FLOAT;
pair_value: '(' builtin_type_value ',' builtin_type_value ')';
vector_value: '[' (builtin_type_value (',' builtin_type_value)* ','?)? ']';
map_value: K_MAP '[' (pair_value (',' pair_value)* ','?)? ']';

// --- lexer rules --- //

// keywords

K_TRUE : T R U E;
K_FALSE : F A L S E;
K_MAP : M A P;
K_IS : I S;
K_DIV : D I V;

K_BOOL : B O O L;
K_STRING : S T R I N G;
K_INT : I N T;
K_FLOAT : F L O A T;

K_PAIR : P A I R;
K_LIST : L I S T;

// data types

STRING : '"' ( '\\"' | . )*? '"' | '\'' ( '\\\'' | . )*? '\'';
INT : '-'? [0-9]+;
FLOAT: '-'? ( [0-9]+'.'[0-9]* | [0-9]*'.'[0-9]+ );
HEXNUMBER : '0' X [0-9a-f]+;

// other lexer rules

ID : [a-zA-Z0-9]+ ;
OP : '+' | '-' | '*' | K_DIV ;
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