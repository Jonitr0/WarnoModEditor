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
        4,1,3,22,2,0,7,0,2,1,7,1,2,2,7,2,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,
        5,1,15,8,1,10,1,12,1,18,9,1,1,2,1,2,1,2,0,1,2,3,0,2,4,0,1,1,0,1,
        2,19,0,6,1,0,0,0,2,9,1,0,0,0,4,19,1,0,0,0,6,7,3,2,1,0,7,8,5,0,0,
        1,8,1,1,0,0,0,9,10,6,1,-1,0,10,11,3,4,2,0,11,16,1,0,0,0,12,13,10,
        1,0,0,13,15,3,4,2,0,14,12,1,0,0,0,15,18,1,0,0,0,16,14,1,0,0,0,16,
        17,1,0,0,0,17,3,1,0,0,0,18,16,1,0,0,0,19,20,7,0,0,0,20,5,1,0,0,0,
        1,16
    ]

class NdfGrammarParser ( Parser ):

    grammarFileName = "NdfGrammar.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [  ]

    symbolicNames = [ "<INVALID>", "K_TRUE", "K_FALSE", "WS" ]

    RULE_ndf_file = 0
    RULE_builtin_type = 1
    RULE_boolean = 2

    ruleNames =  [ "ndf_file", "builtin_type", "boolean" ]

    EOF = Token.EOF
    K_TRUE=1
    K_FALSE=2
    WS=3

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


        def EOF(self):
            return self.getToken(NdfGrammarParser.EOF, 0)

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
            self.state = 6
            self.builtin_type(0)
            self.state = 7
            self.match(NdfGrammarParser.EOF)
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

        def boolean(self):
            return self.getTypedRuleContext(NdfGrammarParser.BooleanContext,0)


        def builtin_type(self):
            return self.getTypedRuleContext(NdfGrammarParser.Builtin_typeContext,0)


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



    def builtin_type(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = NdfGrammarParser.Builtin_typeContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 2
        self.enterRecursionRule(localctx, 2, self.RULE_builtin_type, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 10
            self.boolean()
            self._ctx.stop = self._input.LT(-1)
            self.state = 16
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,0,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = NdfGrammarParser.Builtin_typeContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_builtin_type)
                    self.state = 12
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 13
                    self.boolean() 
                self.state = 18
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,0,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class BooleanContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def K_TRUE(self):
            return self.getToken(NdfGrammarParser.K_TRUE, 0)

        def K_FALSE(self):
            return self.getToken(NdfGrammarParser.K_FALSE, 0)

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
        self.enterRule(localctx, 4, self.RULE_boolean)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 19
            _la = self._input.LA(1)
            if not(_la==1 or _la==2):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[1] = self.builtin_type_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def builtin_type_sempred(self, localctx:Builtin_typeContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 1)
         




