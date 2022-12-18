from antlr4 import *
from src.ndf_parser.antlr_output.NdfGrammarListener import NdfGrammarListener
from src.ndf_parser.antlr_output.NdfGrammarParser import NdfGrammarParser


class CustomNdfListener(NdfGrammarListener):
    def exitBoolean(self, ctx: NdfGrammarParser.BooleanContext):
        print("Found a boolean: " + ctx.getText())

    def exitString(self, ctx:NdfGrammarParser.StringContext):
        print("Found a string: " + ctx.getText())

    def exitInteger(self, ctx:NdfGrammarParser.IntegerContext):
        print("Found an int: " + ctx.getText())
