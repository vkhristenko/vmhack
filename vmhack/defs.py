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
RE_INLINECOMMENT = " +//.*"
RE_LINECOMMENT = "^" + RE_INLINECOMMENT + "$"
RE_EMPTYLINE = "^ *$"
RE_PUSHORPOP = "^(push|pop) +(constant|local|argument|static|this|that|pointer|temp) +([1-9][0-9]*)( *|%s)$" % RE_INLINECOMMENT
RE_ARITHMETIC = "^(add|sub|neg|eq|gt|lt|and|or|not)( *|%s)$" % RE_INLINECOMMENT
