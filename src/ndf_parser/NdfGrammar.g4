grammar NdfGrammar;

// --- parser rules --- //

// general structure

ndf_file : assignment* EOF;
assignment : ( export | private_prefix )? id K_IS r_value;
private_prefix: K_PRIVATE;
export: K_EXPORT;
r_value : concatination | arithmetic | builtin_type_value | object | assignment | obj_reference_value | special_value;
object : obj_type '(' ( block )* ')';
obj_type : ID;
block : assignment | member_assignment;
member_assignment : id '=' ( r_value | assignment );
id : ID (':' builtin_type_label)?;

// operations

arithmetic : '(' arithmetic ')' | arithmetic op arithmetic | '-' arithmetic | atom;
atom : int_value | float_value | hex_value | obj_reference_value;
op: '+' | '-' | '*' | K_DIV;
concatination : concatination '+' concatination | string_value | map_value | vector_value;

// builtin types: labels

builtin_type_label : K_BOOL | K_STRING | K_INT | K_FLOAT | pair_label | list_label | map_label;
pair_label : K_PAIR '<' builtin_type_label ',' builtin_type_label '>';
list_label : K_LIST '<' builtin_type_label '>';
map_label : K_MAP '<' builtin_type_label ',' builtin_type_label '>';

// builtin types: values

builtin_type_value : primitive_value | data_structure_value;
primitive_value: bool_value | string_value | int_value | hex_value | float_value | guid_value;
data_structure_value: pair_value | vector_value | map_value;
bool_value : K_TRUE | K_FALSE;
string_value : STRING;
int_value : INT;
hex_value: HEXNUMBER;
float_value: FLOAT;
guid_value: GUID;
pair_value: '(' r_value ',' r_value ')';
vector_value: '[' (r_value (',' r_value)* ','?)? ']';
map_value: K_MAP '[' (pair_value (',' pair_value)* ','?)? ']';
obj_reference_value: ('$'|'~')?  (ID|'/')* ID | obj_reference_value '|' obj_reference_value;

// special types: values

special_value : rgba_value;
rgba_value : K_RGBA '[' INT ',' INT ',' INT ',' INT ']';

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

K_EXPORT : E X P O R T;
K_PRIVATE : P R I V A T E;

// special keywords

K_RGBA : R G B A;

// data types

STRING : '"' ( '\\"' | . )*? '"' | '\'' ( '\\\'' | . )*? '\'';
INT : '-'? [0-9]+;
FLOAT: '-'? ( [0-9]+'.'[0-9]* | [0-9]*'.'[0-9]+ );
fragment HEXDIGIT : [0-9a-f];
HEXNUMBER : '0' X HEXDIGIT+;
GUID: 'GUID:{' (HEXDIGIT|'-')* '}';

// other lexer rules

ID : [a-zA-Z0-9_]+ ;
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