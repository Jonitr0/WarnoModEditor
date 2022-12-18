import sys
from antlr4 import *
from src.ndf_parser.antlr_output.NdfGrammarLexer import NdfGrammarLexer
from src.ndf_parser.antlr_output.NdfGrammarParser import NdfGrammarParser


def main(argv):
    input_stream = FileStream(argv[1])
    lexer = NdfGrammarLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = NdfGrammarParser(stream)
    tree = parser.startRule()


if __name__ == '__main__':
    main(sys.argv)