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
        4,1,6,33,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,1,0,1,0,1,0,1,1,
        1,1,1,1,1,1,3,1,18,8,1,1,1,1,1,5,1,22,8,1,10,1,12,1,25,9,1,1,2,1,
        2,1,3,1,3,1,4,1,4,1,4,0,1,2,5,0,2,4,6,8,0,2,1,0,1,2,1,0,5,6,30,0,
        10,1,0,0,0,2,17,1,0,0,0,4,26,1,0,0,0,6,28,1,0,0,0,8,30,1,0,0,0,10,
        11,3,2,1,0,11,12,5,0,0,1,12,1,1,0,0,0,13,14,6,1,-1,0,14,18,3,4,2,
        0,15,18,3,8,4,0,16,18,3,6,3,0,17,13,1,0,0,0,17,15,1,0,0,0,17,16,
        1,0,0,0,18,23,1,0,0,0,19,20,10,1,0,0,20,22,3,2,1,2,21,19,1,0,0,0,
        22,25,1,0,0,0,23,21,1,0,0,0,23,24,1,0,0,0,24,3,1,0,0,0,25,23,1,0,
        0,0,26,27,7,0,0,0,27,5,1,0,0,0,28,29,5,4,0,0,29,7,1,0,0,0,30,31,
        7,1,0,0,31,9,1,0,0,0,2,17,23
    ]

class NdfGrammarParser ( Parser ):

    grammarFileName = "NdfGrammar.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [  ]

    symbolicNames = [ "<INVALID>", "K_TRUE", "K_FALSE", "WS", "STRING", 
                      "INT", "HEXNUMBER" ]

    RULE_ndf_file = 0
    RULE_builtin_type = 1
    RULE_boolean = 2
    RULE_string = 3
    RULE_integer = 4

    ruleNames =  [ "ndf_file", "builtin_type", "boolean", "string", "integer" ]

    EOF = Token.EOF
    K_TRUE=1
    K_FALSE=2
    WS=3
    STRING=4
    INT=5
    HEXNUMBER=6

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
            self.state = 10
            self.builtin_type(0)
            self.state = 11
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


        def integer(self):
            return self.getTypedRuleContext(NdfGrammarParser.IntegerContext,0)


        def string(self):
            return self.getTypedRuleContext(NdfGrammarParser.StringContext,0)


        def builtin_type(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(NdfGrammarParser.Builtin_typeContext)
            else:
                return self.getTypedRuleContext(NdfGrammarParser.Builtin_typeContext,i)


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
            self.state = 17
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1, 2]:
                self.state = 14
                self.boolean()
                pass
            elif token in [5, 6]:
                self.state = 15
                self.integer()
                pass
            elif token in [4]:
                self.state = 16
                self.string()
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 23
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,1,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = NdfGrammarParser.Builtin_typeContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_builtin_type)
                    self.state = 19
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 20
                    self.builtin_type(2) 
                self.state = 25
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,1,self._ctx)

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
            self.state = 26
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


    class StringContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(NdfGrammarParser.STRING, 0)

        def getRuleIndex(self):
            return NdfGrammarParser.RULE_string

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterString" ):
                listener.enterString(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitString" ):
                listener.exitString(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitString" ):
                return visitor.visitString(self)
            else:
                return visitor.visitChildren(self)




    def string(self):

        localctx = NdfGrammarParser.StringContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_string)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 28
            self.match(NdfGrammarParser.STRING)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IntegerContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT(self):
            return self.getToken(NdfGrammarParser.INT, 0)

        def HEXNUMBER(self):
            return self.getToken(NdfGrammarParser.HEXNUMBER, 0)

        def getRuleIndex(self):
            return NdfGrammarParser.RULE_integer

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInteger" ):
                listener.enterInteger(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInteger" ):
                listener.exitInteger(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInteger" ):
                return visitor.visitInteger(self)
            else:
                return visitor.visitChildren(self)




    def integer(self):

        localctx = NdfGrammarParser.IntegerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_integer)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 30
            _la = self._input.LA(1)
            if not(_la==5 or _la==6):
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
         




