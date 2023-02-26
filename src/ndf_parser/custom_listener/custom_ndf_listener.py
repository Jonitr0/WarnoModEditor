from antlr4 import *
from src.ndf_parser.antlr_output.NdfGrammarListener import NdfGrammarListener
from src.ndf_parser.antlr_output.NdfGrammarParser import NdfGrammarParser


class CustomNdfListener(NdfGrammarListener):
    def exitMember_assignment(self, ctx:NdfGrammarParser.Member_assignmentContext):
        print("Found a member assignment: " + ctx.getText())

# TODO: generate list of Napo Entities from NDF primitive assignments
