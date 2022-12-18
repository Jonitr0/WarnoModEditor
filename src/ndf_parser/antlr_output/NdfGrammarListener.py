# Generated from NdfGrammar.g4 by ANTLR 4.11.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .NdfGrammarParser import NdfGrammarParser
else:
    from NdfGrammarParser import NdfGrammarParser

# This class defines a complete listener for a parse tree produced by NdfGrammarParser.
class NdfGrammarListener(ParseTreeListener):

    # Enter a parse tree produced by NdfGrammarParser#ndf_file.
    def enterNdf_file(self, ctx:NdfGrammarParser.Ndf_fileContext):
        pass

    # Exit a parse tree produced by NdfGrammarParser#ndf_file.
    def exitNdf_file(self, ctx:NdfGrammarParser.Ndf_fileContext):
        pass


    # Enter a parse tree produced by NdfGrammarParser#builtin_type.
    def enterBuiltin_type(self, ctx:NdfGrammarParser.Builtin_typeContext):
        pass

    # Exit a parse tree produced by NdfGrammarParser#builtin_type.
    def exitBuiltin_type(self, ctx:NdfGrammarParser.Builtin_typeContext):
        pass


    # Enter a parse tree produced by NdfGrammarParser#boolean.
    def enterBoolean(self, ctx:NdfGrammarParser.BooleanContext):
        pass

    # Exit a parse tree produced by NdfGrammarParser#boolean.
    def exitBoolean(self, ctx:NdfGrammarParser.BooleanContext):
        pass


    # Enter a parse tree produced by NdfGrammarParser#string.
    def enterString(self, ctx:NdfGrammarParser.StringContext):
        pass

    # Exit a parse tree produced by NdfGrammarParser#string.
    def exitString(self, ctx:NdfGrammarParser.StringContext):
        pass


    # Enter a parse tree produced by NdfGrammarParser#integer.
    def enterInteger(self, ctx:NdfGrammarParser.IntegerContext):
        pass

    # Exit a parse tree produced by NdfGrammarParser#integer.
    def exitInteger(self, ctx:NdfGrammarParser.IntegerContext):
        pass



del NdfGrammarParser