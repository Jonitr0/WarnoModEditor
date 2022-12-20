import sys
from antlr4 import *
from antlr4.tree.Trees import Trees

from src.ndf_parser.antlr_output.NdfGrammarLexer import NdfGrammarLexer
from src.ndf_parser.antlr_output.NdfGrammarParser import NdfGrammarParser

from src.ndf_parser.custom_listener import custom_ndf_listener


def main(argv):
    input_stream = FileStream(argv[1])
    lexer = NdfGrammarLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = NdfGrammarParser(stream)
    tree = parser.ndf_file()

    listener = custom_ndf_listener.CustomNdfListener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)

    print(Trees.toStringTree(tree, None, parser))


if __name__ == '__main__':
    main(sys.argv)
