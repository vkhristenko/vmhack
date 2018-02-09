"""
various constants / definitions / declarations
"""

#
# list of Hack VM commands
#
C_ARITHMETIC = 0
C_PUSH = 1
C_POP = 2
C_LABEL = 3
C_GOTO = 4
C_IF = 5
C_FUNCTION = 6
C_RETURN = 7
C_CALL = 8

#
# Memory Segments Base Addresses
#
SP = 0
LCL = 1
ARG = 2
THIS = 3
THAT = 4
POINTER = 3
TEMP = 5
STACK_BASE = 256
HEAP_BASE = 2048

segment2id = {"constant" : None, "local" : LCL, "argument" : ARG,
        "pointer" : POINTER, "temp" : TEMP, "this" : THIS, "that" : THAT}

#
# Regular Expressions to specify the Hack VM Language
#
RE_INLINECOMMENT = "[ \t]*//.*"
RE_LINECOMMENT = "^" + RE_INLINECOMMENT + "$"
RE_EMPTYLINE = "^$"
RE_PUSHORPOP = "^(push|pop) +(constant|local|argument|static|this|that|pointer|temp) +([0-9]+)([ \t]*|[ \t]%s)$" % RE_INLINECOMMENT
RE_ARITHMETIC = "^(add|sub|neg|eq|gt|lt|and|or|not)([ \t]*|[ \t]%s)$" % RE_INLINECOMMENT
RE_LABEL = "^(label) +([a-zA-Z_.:][a-zA-Z_0-9$_:.]*)([ \t]*|[ \t]%s)$" % RE_INLINECOMMENT
RE_GOTO = "^(goto) +([a-zA-Z][a-zA-Z_0-9$.]*)([ \t]*|[ \t]%s)$"% RE_INLINECOMMENT
RE_IF = "^(if-goto) +([a-zA-Z][a-zA-Z_0-9$.]*)([ \t]*|[ \t]%s)$" % RE_INLINECOMMENT
RE_FUNCTION = "^(function) +([a-zA-Z][a-zA-Z_0-9$.]*) +([0-9]+)([ \t]*|[ \t]%s)$" % RE_INLINECOMMENT
RE_CALL = "^(call) +([a-zA-Z][a-zA-Z_0-9$.]*) +([0-9]+)([ \t]*|[ \t]%s)$" % RE_INLINECOMMENT
RE_RETURN = "^(return)([ \t]*|[ \t]%s)$" % RE_INLINECOMMENT
