# Generated from NdfGrammar.g4 by ANTLR 4.11.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .NdfGrammarParser import NdfGrammarParser
else:
    from NdfGrammarParser import NdfGrammarParser

# This class defines a complete generic visitor for a parse tree produced by NdfGrammarParser.

class NdfGrammarVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by NdfGrammarParser#ndf_file.
    def visitNdf_file(self, ctx:NdfGrammarParser.Ndf_fileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NdfGrammarParser#builtin_type.
    def visitBuiltin_type(self, ctx:NdfGrammarParser.Builtin_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NdfGrammarParser#boolean.
    def visitBoolean(self, ctx:NdfGrammarParser.BooleanContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NdfGrammarParser#string.
    def visitString(self, ctx:NdfGrammarParser.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by NdfGrammarParser#integer.
    def visitInteger(self, ctx:NdfGrammarParser.IntegerContext):
        return self.visitChildren(ctx)



del NdfGrammarParser