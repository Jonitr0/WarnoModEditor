grammar NdfGrammar;

ndf_file : builtin_type ;
builtin_type : T_BOOLEAN ;

T_BOOLEAN : ('true'|'false') ;