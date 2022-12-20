from antlr4 import *
from src.ndf_parser.antlr_output.NdfGrammarListener import NdfGrammarListener
from src.ndf_parser.antlr_output.NdfGrammarParser import NdfGrammarParser


class CustomNdfListener(NdfGrammarListener):
    def exitAssignment(self, ctx:NdfGrammarParser.AssignmentContext):
        print("Found an assignment: " + ctx.getText())
