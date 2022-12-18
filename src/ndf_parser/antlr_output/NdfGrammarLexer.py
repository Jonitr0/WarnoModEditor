# Generated from NdfGrammar.g4 by ANTLR 4.11.1
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    return [
        4,0,1,14,6,-1,2,0,7,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,3,0,13,
        8,0,0,0,1,1,1,1,0,0,14,0,1,1,0,0,0,1,12,1,0,0,0,3,4,5,116,0,0,4,
        5,5,114,0,0,5,6,5,117,0,0,6,13,5,101,0,0,7,8,5,102,0,0,8,9,5,97,
        0,0,9,10,5,108,0,0,10,11,5,115,0,0,11,13,5,101,0,0,12,3,1,0,0,0,
        12,7,1,0,0,0,13,2,1,0,0,0,2,0,12,0
    ]

class NdfGrammarLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T_BOOLEAN = 1

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
 ]

    symbolicNames = [ "<INVALID>",
            "T_BOOLEAN" ]

    ruleNames = [ "T_BOOLEAN" ]

    grammarFileName = "NdfGrammar.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.11.1")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


