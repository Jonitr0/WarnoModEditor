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
        4,1,13,9,2,0,7,0,2,1,7,1,1,0,1,0,1,1,1,1,1,1,0,0,2,0,2,0,0,6,0,4,
        1,0,0,0,2,6,1,0,0,0,4,5,3,2,1,0,5,1,1,0,0,0,6,7,5,13,0,0,7,3,1,0,
        0,0,0
    ]

class NdfGrammarParser ( Parser ):

    grammarFileName = "NdfGrammar.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [  ]

    symbolicNames = [ "<INVALID>", "K_EXPORT", "K_IS", "K_TEMPLATE", "K_UNNAMED", 
                      "K_NIL", "K_PRIVATE", "K_INT", "K_STRING", "K_TRUE", 
                      "K_FALSE", "K_DIV", "K_MAP", "T_BOOLEAN" ]

    RULE_builtin_type = 0
    RULE_boolean = 1

    ruleNames =  [ "builtin_type", "boolean" ]

    EOF = Token.EOF
    K_EXPORT=1
    K_IS=2
    K_TEMPLATE=3
    K_UNNAMED=4
    K_NIL=5
    K_PRIVATE=6
    K_INT=7
    K_STRING=8
    K_TRUE=9
    K_FALSE=10
    K_DIV=11
    K_MAP=12
    T_BOOLEAN=13

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.11.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class Builtin_typeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def boolean(self):
            return self.getTypedRuleContext(NdfGrammarParser.BooleanContext,0)


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
        self.enterRule(localctx, 0, self.RULE_builtin_type)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 4
            self.boolean()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BooleanContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def T_BOOLEAN(self):
            return self.getToken(NdfGrammarParser.T_BOOLEAN, 0)

        def getRuleIndex(self):
            return NdfGrammarParser.RULE_boolean

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBoolean" ):
                listener.enterBoolean(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBoolean" ):
                listener.exitBoolean(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBoolean" ):
                return visitor.visitBoolean(self)
            else:
                return visitor.visitChildren(self)




    def boolean(self):

        localctx = NdfGrammarParser.BooleanContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_boolean)
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





