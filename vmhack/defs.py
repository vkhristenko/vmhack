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
STACK_BASE = 256
HEAP_BASE = 2048
