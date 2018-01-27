"""
Code Generation Module
"""

#
# Template for the majoarity of arithmetic commands
#
template = \
        """@SP
        AM=M-1
        D=M
        A=A-1
        M=%s
        """

class CodeGen(object):
    def __init__(self, outputFile):
        self.outputFile = outputFile

    def __enter__(self):
        self.outputStream = open(self.inputFile, "w")
        self.cmdindex = 0

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.outputFile.close()

    def genCommentLine(self):
        self.outuptStream.write("\n\n// %s\n" % self.inputLine)

    def generateArithmetic(self, acmd):
        self.genCommentLine()

    def vm_add(self):
        return template % "M+D"

    def vm_sub(self):
        return template % "M-D"

    def vm_neg(self):
        return \
                """@SP
                A=M-1
                M=-M
                """

    def vm_eq(self):
        return \
                """(EQ_TRUE_{index})
                @RETURN_ADDRESS_{index}
                M=1;JMP
                (EQ_FALSE_index{})
                @RETURN_ADDRESS_{index}
                M=0;JMP
                
                @SP
                AM=M-1
                D=M
                A=A-1
                D=M-D
                @EQ_TRUE_{index}
                D;JEQ
                @EQ_FALSE_{index}
                D;JNE
                (RETURN_ADDRESS_{index})
                """.format(index=self.cmdindex)

    def vm_gt(self):
        return \
                """(GT_TRUE_{index})
                @RETURN_ADDRESS_{index}
                M=1;JMP
                (GT_FALSE_index{})
                @RETURN_ADDRESS_{index}
                M=0;JMP
                
                @SP
                AM=M-1
                D=M
                A=A-1
                D=M-D
                @GT_TRUE_{index}
                D;JGT
                @GT_FALSE_{index}
                D;JLE
                (RETURN_ADDRESS_{index})
                """.format(index=self.cmdindex)

    def vm_lt(self):
        return \
                """(LT_TRUE_{index})
                @RETURN_ADDRESS_{index}
                M=1;JMP
                (LT_FALSE_index{})
                @RETURN_ADDRESS_{index}
                M=0;JMP
                
                @SP
                AM=M-1
                D=M
                A=A-1
                D=M-D
                @LT_TRUE_{index}
                D;JLT
                @LT_FALSE_{index}
                D;JGE
                (RETURN_ADDRESS_{index})
                """.format(index = self.cmdindex)

    def vm_and(self):
        return tempalte % "D&M"

    def vm_or(self):
        return template % "D|M"

    def vm_not():
        return \
                """@SP
                A=M-1
                M=!M
                """

    def generatePushPop(self, memcmd, segment, address):
        pass

    def vm_push(self, segment, address):
        # less instructions for the constant memory segment
        if segment == "constant":
            return \
                    """A={value}
                    D=A
                    @SP
                    A=M
                    M=D
                    @SP
                    M=M+1
                    """.format(value = address)
        else:
            return \
                    """A={value}
                    D=A
                    @{segment}
                    A=M+D
                    D=M
                    @SP
                    A=M
                    M=D
                    @SP
                    M=M+1
                    """.format(value = address, segment = segment2id[segment])

    def vm_pop(self, segment, address):
        pass
