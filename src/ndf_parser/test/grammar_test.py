import sys
from antlr4 import *
from antlr4.tree.Trees import Trees

from src.ndf_parser.antlr_output.NdfGrammarLexer import NdfGrammarLexer
from src.ndf_parser.antlr_output.NdfGrammarParser import NdfGrammarParser

from src.ndf_parser.object_generator import napo_generator
from src.ndf_parser.ndf_converter import napo_to_ndf_converter


def main(argv):
    input_stream = FileStream(argv[1], encoding="utf8")

    lexer = NdfGrammarLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = NdfGrammarParser(stream)
    tree = parser.ndf_file()

    listener = napo_generator.NapoGenerator(parser)
    walker = ParseTreeWalker()
    walker.walk(listener, tree)

    converter = napo_to_ndf_converter.NapoToNdfConverter()
    print(converter.convert(listener.assignments))

    #print(Trees.toStringTree(tree, None, parser))


if __name__ == '__main__':
    main(sys.argv)
