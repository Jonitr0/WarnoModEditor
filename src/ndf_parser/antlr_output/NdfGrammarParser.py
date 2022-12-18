# Generated from NdfGrammar.g4 by ANTLR 4.11.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,1,9,2,0,7,0,2,1,7,1,1,0,1,0,1,1,1,1,1,1,0,0,2,0,2,0,0,6,0,4,
        1,0,0,0,2,6,1,0,0,0,4,5,3,2,1,0,5,1,1,0,0,0,6,7,5,1,0,0,7,3,1,0,
        0,0,0
    ]

class NdfGrammarParser ( Parser ):

    grammarFileName = "NdfGrammar.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [  ]

    symbolicNames = [ "<INVALID>", "T_BOOLEAN" ]

    RULE_ndf_file = 0
    RULE_builtin_type = 1

    ruleNames =  [ "ndf_file", "builtin_type" ]

    EOF = Token.EOF
    T_BOOLEAN=1

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.11.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class Ndf_fileContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def builtin_type(self):
            return self.getTypedRuleContext(NdfGrammarParser.Builtin_typeContext,0)


        def getRuleIndex(self):
            return NdfGrammarParser.RULE_ndf_file

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNdf_file" ):
                listener.enterNdf_file(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNdf_file" ):
                listener.exitNdf_file(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNdf_file" ):
                return visitor.visitNdf_file(self)
            else:
                return visitor.visitChildren(self)




    def ndf_file(self):

        localctx = NdfGrammarParser.Ndf_fileContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_ndf_file)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 4
            self.builtin_type()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Builtin_typeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def T_BOOLEAN(self):
            return self.getToken(NdfGrammarParser.T_BOOLEAN, 0)

        def getRuleIndex(self):
            return NdfGrammarParser.RULE_builtin_type

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBuiltin_type" ):
                listener.enterBuiltin_type(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBuiltin_type" ):
                listener.exitBuiltin_type(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBuiltin_type" ):
                return visitor.visitBuiltin_type(self)
            else:
                return visitor.visitChildren(self)




    def builtin_type(self):

        localctx = NdfGrammarParser.Builtin_typeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_builtin_type)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 6
            self.match(NdfGrammarParser.T_BOOLEAN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





