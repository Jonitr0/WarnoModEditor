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
        4,1,13,86,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,
        1,30,8,1,1,1,1,1,5,1,34,8,1,10,1,12,1,37,9,1,1,2,1,2,1,3,1,3,1,4,
        1,4,1,5,1,5,1,6,1,6,1,6,1,6,1,6,1,6,1,7,1,7,1,7,1,7,5,7,57,8,7,10,
        7,12,7,60,9,7,1,7,3,7,63,8,7,3,7,65,8,7,1,7,1,7,1,8,1,8,1,8,1,8,
        1,8,5,8,74,8,8,10,8,12,8,77,9,8,1,8,3,8,80,8,8,3,8,82,8,8,1,8,1,
        8,1,8,0,1,2,9,0,2,4,6,8,10,12,14,16,0,2,1,0,6,7,2,0,10,10,12,12,
        89,0,18,1,0,0,0,2,29,1,0,0,0,4,38,1,0,0,0,6,40,1,0,0,0,8,42,1,0,
        0,0,10,44,1,0,0,0,12,46,1,0,0,0,14,52,1,0,0,0,16,68,1,0,0,0,18,19,
        3,2,1,0,19,20,5,0,0,1,20,1,1,0,0,0,21,22,6,1,-1,0,22,30,3,4,2,0,
        23,30,3,6,3,0,24,30,3,8,4,0,25,30,3,10,5,0,26,30,3,12,6,0,27,30,
        3,14,7,0,28,30,3,16,8,0,29,21,1,0,0,0,29,23,1,0,0,0,29,24,1,0,0,
        0,29,25,1,0,0,0,29,26,1,0,0,0,29,27,1,0,0,0,29,28,1,0,0,0,30,35,
        1,0,0,0,31,32,10,1,0,0,32,34,3,2,1,2,33,31,1,0,0,0,34,37,1,0,0,0,
        35,33,1,0,0,0,35,36,1,0,0,0,36,3,1,0,0,0,37,35,1,0,0,0,38,39,7,0,
        0,0,39,5,1,0,0,0,40,41,5,9,0,0,41,7,1,0,0,0,42,43,7,1,0,0,43,9,1,
        0,0,0,44,45,5,11,0,0,45,11,1,0,0,0,46,47,5,1,0,0,47,48,3,2,1,0,48,
        49,5,2,0,0,49,50,3,2,1,0,50,51,5,3,0,0,51,13,1,0,0,0,52,64,5,4,0,
        0,53,58,3,2,1,0,54,55,5,2,0,0,55,57,3,2,1,0,56,54,1,0,0,0,57,60,
        1,0,0,0,58,56,1,0,0,0,58,59,1,0,0,0,59,62,1,0,0,0,60,58,1,0,0,0,
        61,63,5,2,0,0,62,61,1,0,0,0,62,63,1,0,0,0,63,65,1,0,0,0,64,53,1,
        0,0,0,64,65,1,0,0,0,65,66,1,0,0,0,66,67,5,5,0,0,67,15,1,0,0,0,68,
        69,5,8,0,0,69,81,5,4,0,0,70,75,3,12,6,0,71,72,5,2,0,0,72,74,3,12,
        6,0,73,71,1,0,0,0,74,77,1,0,0,0,75,73,1,0,0,0,75,76,1,0,0,0,76,79,
        1,0,0,0,77,75,1,0,0,0,78,80,5,2,0,0,79,78,1,0,0,0,79,80,1,0,0,0,
        80,82,1,0,0,0,81,70,1,0,0,0,81,82,1,0,0,0,82,83,1,0,0,0,83,84,5,
        5,0,0,84,17,1,0,0,0,8,29,35,58,62,64,75,79,81
    ]

class NdfGrammarParser ( Parser ):

    grammarFileName = "NdfGrammar.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'('", "','", "')'", "'['", "']'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "K_TRUE", "K_FALSE", "K_MAP", 
                      "STRING", "INT", "FLOAT", "HEXNUMBER", "WS" ]

    RULE_ndf_file = 0
    RULE_builtin_type = 1
    RULE_boolean = 2
    RULE_string = 3
    RULE_integer = 4
    RULE_float = 5
    RULE_pair = 6
    RULE_vector = 7
    RULE_map = 8

    ruleNames =  [ "ndf_file", "builtin_type", "boolean", "string", "integer", 
                   "float", "pair", "vector", "map" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    K_TRUE=6
    K_FALSE=7
    K_MAP=8
    STRING=9
    INT=10
    FLOAT=11
    HEXNUMBER=12
    WS=13

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
            self.state = 18
            self.builtin_type(0)
            self.state = 19
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


        def string(self):
            return self.getTypedRuleContext(NdfGrammarParser.StringContext,0)


        def integer(self):
            return self.getTypedRuleContext(NdfGrammarParser.IntegerContext,0)


        def float_(self):
            return self.getTypedRuleContext(NdfGrammarParser.FloatContext,0)


        def pair(self):
            return self.getTypedRuleContext(NdfGrammarParser.PairContext,0)


        def vector(self):
            return self.getTypedRuleContext(NdfGrammarParser.VectorContext,0)


        def map_(self):
            return self.getTypedRuleContext(NdfGrammarParser.MapContext,0)


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
            self.state = 29
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [6, 7]:
                self.state = 22
                self.boolean()
                pass
            elif token in [9]:
                self.state = 23
                self.string()
                pass
            elif token in [10, 12]:
                self.state = 24
                self.integer()
                pass
            elif token in [11]:
                self.state = 25
                self.float_()
                pass
            elif token in [1]:
                self.state = 26
                self.pair()
                pass
            elif token in [4]:
                self.state = 27
                self.vector()
                pass
            elif token in [8]:
                self.state = 28
                self.map_()
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 35
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,1,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = NdfGrammarParser.Builtin_typeContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_builtin_type)
                    self.state = 31
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 32
                    self.builtin_type(2) 
                self.state = 37
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
            self.state = 38
            _la = self._input.LA(1)
            if not(_la==6 or _la==7):
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
            self.state = 40
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
            self.state = 42
            _la = self._input.LA(1)
            if not(_la==10 or _la==12):
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


    class FloatContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FLOAT(self):
            return self.getToken(NdfGrammarParser.FLOAT, 0)

        def getRuleIndex(self):
            return NdfGrammarParser.RULE_float

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFloat" ):
                listener.enterFloat(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFloat" ):
                listener.exitFloat(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFloat" ):
                return visitor.visitFloat(self)
            else:
                return visitor.visitChildren(self)




    def float_(self):

        localctx = NdfGrammarParser.FloatContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_float)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 44
            self.match(NdfGrammarParser.FLOAT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PairContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def builtin_type(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(NdfGrammarParser.Builtin_typeContext)
            else:
                return self.getTypedRuleContext(NdfGrammarParser.Builtin_typeContext,i)


        def getRuleIndex(self):
            return NdfGrammarParser.RULE_pair

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPair" ):
                listener.enterPair(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPair" ):
                listener.exitPair(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPair" ):
                return visitor.visitPair(self)
            else:
                return visitor.visitChildren(self)




    def pair(self):

        localctx = NdfGrammarParser.PairContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_pair)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 46
            self.match(NdfGrammarParser.T__0)
            self.state = 47
            self.builtin_type(0)
            self.state = 48
            self.match(NdfGrammarParser.T__1)
            self.state = 49
            self.builtin_type(0)
            self.state = 50
            self.match(NdfGrammarParser.T__2)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VectorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def builtin_type(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(NdfGrammarParser.Builtin_typeContext)
            else:
                return self.getTypedRuleContext(NdfGrammarParser.Builtin_typeContext,i)


        def getRuleIndex(self):
            return NdfGrammarParser.RULE_vector

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVector" ):
                listener.enterVector(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVector" ):
                listener.exitVector(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVector" ):
                return visitor.visitVector(self)
            else:
                return visitor.visitChildren(self)




    def vector(self):

        localctx = NdfGrammarParser.VectorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_vector)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 52
            self.match(NdfGrammarParser.T__3)
            self.state = 64
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if ((_la) & ~0x3f) == 0 and ((1 << _la) & 8146) != 0:
                self.state = 53
                self.builtin_type(0)
                self.state = 58
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 54
                        self.match(NdfGrammarParser.T__1)
                        self.state = 55
                        self.builtin_type(0) 
                    self.state = 60
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

                self.state = 62
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==2:
                    self.state = 61
                    self.match(NdfGrammarParser.T__1)




            self.state = 66
            self.match(NdfGrammarParser.T__4)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MapContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def K_MAP(self):
            return self.getToken(NdfGrammarParser.K_MAP, 0)

        def pair(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(NdfGrammarParser.PairContext)
            else:
                return self.getTypedRuleContext(NdfGrammarParser.PairContext,i)


        def getRuleIndex(self):
            return NdfGrammarParser.RULE_map

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMap" ):
                listener.enterMap(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMap" ):
                listener.exitMap(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMap" ):
                return visitor.visitMap(self)
            else:
                return visitor.visitChildren(self)




    def map_(self):

        localctx = NdfGrammarParser.MapContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_map)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 68
            self.match(NdfGrammarParser.K_MAP)
            self.state = 69
            self.match(NdfGrammarParser.T__3)
            self.state = 81
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==1:
                self.state = 70
                self.pair()
                self.state = 75
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,5,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 71
                        self.match(NdfGrammarParser.T__1)
                        self.state = 72
                        self.pair() 
                    self.state = 77
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,5,self._ctx)

                self.state = 79
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==2:
                    self.state = 78
                    self.match(NdfGrammarParser.T__1)




            self.state = 83
            self.match(NdfGrammarParser.T__4)
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
         




