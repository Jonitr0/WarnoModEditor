import os
import re
import unittest
from diff_match_patch import diff_match_patch

from antlr4 import *
from antlr4.tree.Trees import Trees

from src.ndf_parser.antlr_output.NdfGrammarLexer import NdfGrammarLexer
from src.ndf_parser.antlr_output.NdfGrammarParser import NdfGrammarParser

from src.ndf_parser.object_generator import napo_generator
from src.ndf_parser.napo_entities.napo_collection import *
from src.ndf_parser.napo_entities.napo_assignment import NapoAssignment
from src.ndf_parser.ndf_converter import napo_to_ndf_converter


def compare_strings(orig: str, generated: str) -> (str, str, bool):
    # remove comments (single line)
    orig = re.sub(r'//.*', "", orig)
    generated = re.sub(r'//.*', "", generated)
    # strip of all filler characters and commata
    for char in [" ", "\n", "\r", "\t"]:
        orig = orig.replace(char, "")
        generated = generated.replace(char, "")
    # make everything lowercase (ndf isn't case sensitive, good enough for our purposes)
    orig = orig.lower()
    generated = generated.lower()

    return orig, generated, orig == generated


def generate_napo(file_name: str) -> [NapoAssignment]:
    input_stream = FileStream(file_name, encoding="utf8")

    lexer = NdfGrammarLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = NdfGrammarParser(stream)
    tree = parser.ndf_file()

    listener = napo_generator.NapoGenerator(parser)
    walker = ParseTreeWalker()
    walker.walk(listener, tree)

    return NapoFile(listener.assignments)


def napo_roundtrip(file_name: str):
    converter = napo_to_ndf_converter.NapoToNdfConverter()
    napo_file = generate_napo(file_name)
    return converter.convert(napo_file), napo_file


# for debugging
def print_tree(tree, parser):
    print(Trees.toStringTree(tree, None, parser))


class TestNapo(unittest.TestCase):
    def test_primitives(self):
        self.roundtrip_test("primitives.ndf")

    def test_datastructures(self):
        self.roundtrip_test("datastructures.ndf")

    def test_object(self):
        self.roundtrip_test("Airplane.ndf")

    def test_gd_contantes(self):
        self.object_comparison_test("GDConstantes.ndf")
        self.roundtrip_test("GDConstantes.ndf")

    def test_get_val_constantes(self):
        self.get_val_test("GDConstantes.ndf", "EShowGhostOverSpecificTerrainConditionFilterType\\None", 0)
        self.get_val_test("GDConstantes.ndf", "Constantes\\DefaultGhostColors\\GhostColor", [255, 255, 255, 255])

    def test_set_val_constantes(self):
        #self.set_val_test("GDConstantes.ndf", "EShowGhostOverSpecificTerrainConditionFilterType\\None",
        #                  10, [NapoDatatype.Integer])
        self.set_val_test("GDConstantes.ndf", "Constantes\\DefaultGhostColors\\GhostColor",
                          [1, 1, 1, 1], [NapoDatatype.Integer]*4)

    def roundtrip_test(self, file_name: str):
        with open(file_name, encoding="utf-8") as f:
            orig = f.read()
        generated, _ = napo_roundtrip(file_name)
        orig_cmp, generated_cmp, equal = compare_strings(orig, generated)
        try:
            self.assertTrue(equal)
        except AssertionError as e:
            dmp = diff_match_patch()
            patches = dmp.patch_make(orig_cmp, generated_cmp)
            diff = dmp.patch_toText(patches)
            print(diff)
            print("original:\n")
            print(orig)
            print("generated:\n")
            print(generated)
            raise e

    def object_comparison_test(self, file_name: str):
        with open(file_name, encoding="utf-8") as f:
            orig = f.read()
        generated, orig_napo = napo_roundtrip(file_name)
        with open("tmp.txt", encoding="utf-8", mode="x") as f:
            f.write(generated)
            generated_napo = generate_napo("tmp.txt")
        os.remove("tmp.txt")
        if orig_napo != generated_napo:
            raise Exception("Assignments not equal")


    def get_val_test(self, file_name: str, path: str, expected):
        napo_file = generate_napo(file_name)
        res = napo_file.get_value(path)
        if res != expected:
            print("found:\n")
            print(res)
            print(type(res))
            print("expected:\n")
            print(expected)
            print(type(expected))
            raise Exception("Find results not equal")

    def set_val_test(self, file_name: str, path: str, value, dtypes: [NapoDatatype]):
        # set value on napo
        napo_file = generate_napo(file_name)
        napo_file.set_value(path, value, dtypes)
        # convert to string
        converter = napo_to_ndf_converter.NapoToNdfConverter()
        napo_str = converter.convert(napo_file)
        # write to a new file
        with open("tmp.txt", encoding="utf-8", mode="x") as f:
            f.write(napo_str)
            generated_napo = generate_napo("tmp.txt")
        os.remove("tmp.txt")

        res = generated_napo.get_value(path)
        if res != value:
            print("found:\n")
            print(res)
            print(type(res))
            print("expected:\n")
            print(value)
            print(type(value))
            raise Exception("Find results not equal after setting value")

