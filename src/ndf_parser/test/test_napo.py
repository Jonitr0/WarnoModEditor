import re
import unittest
from diff_match_patch import diff_match_patch

from antlr4 import *

from src.ndf_parser.antlr_output.NdfGrammarLexer import NdfGrammarLexer
from src.ndf_parser.antlr_output.NdfGrammarParser import NdfGrammarParser

from src.ndf_parser.object_generator import napo_generator
from src.ndf_parser.ndf_converter import napo_to_ndf_converter


def compare_strings(orig: str, generated: str) -> (str, str, bool):
    # remove comments (single line)
    orig = re.sub(r'//.*', "", orig)
    generated = re.sub(r'//.*', "", generated)
    # strip of all filler characters
    for char in [" ", "\n", "\r", "\t"]:
        orig = orig.replace(char, "")
        generated = generated.replace(char, "")
    # make everything lowercase (ndf isn't case sensitive, good enough for our purposes)
    orig = orig.lower()
    generated = generated.lower()

    return orig, generated, orig == generated


def napo_roundtrip(file_name: str) -> str:
    input_stream = FileStream(file_name, encoding="utf8")

    lexer = NdfGrammarLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = NdfGrammarParser(stream)
    tree = parser.ndf_file()

    listener = napo_generator.NapoGenerator(parser)
    walker = ParseTreeWalker()
    walker.walk(listener, tree)

    converter = napo_to_ndf_converter.NapoToNdfConverter()
    return converter.convert(listener.assignments)


class TestNapo(unittest.TestCase):
    def test_primitives_roundtrip(self):
        with open("primitives.ndf", encoding="utf-8") as f:
            orig = f.read()
        generated = napo_roundtrip("primitives.ndf")
        orig, generated, equal = compare_strings(orig, generated)
        try:
            self.assertTrue(equal)
        except AssertionError as e:
            dmp = diff_match_patch()
            patches = dmp.patch_make(orig, generated)
            diff = dmp.patch_toText(patches)
            print(diff)
            raise e

