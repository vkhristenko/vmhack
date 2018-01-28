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
        self.outputStream = open(self.outputFile, "w")
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
                    """@{value}
                    D=A
                    @SP
                    A=M
                    M=D
                    @SP
                    M=M+1
                    """.format(value = address)
        elif segment in ["local", "argument", "this", "that"]:
            return \
                    """@{value}
                    D=A
                    @{segment}
                    A=M+D
                    D=M
                    @SP
                    A=M
                    M=D
                    @SP
                    M=M+1
                    """.format(value = address, segment = defs.segment2id[segment])
        elif segment == "static":
            return \
                    """@{filename}.{index}
                    D=M
                    @SP
                    A=M
                    M=D
                    @SP
                    M=M+1
                    """.format(filename=self.outputFile.rstrip(".asm"),
                               index = address)
        elif segment == "temp":
            return \
                    """@{index}
                    D=A
                    @{temp}
                    A=D+A
                    D=M
                    @SP
                    A=M
                    M=D
                    @SP
                    M=M+1
                    """.format(index=address, temp=defs.TEMP)
        elif segment == "pointer":
            if address == 0:
                return \
                        """@{this}
                        D=M
                        @SP
                        A=M
                        M=D
                        @SP
                        M=M+1
                        """.format(this=defs.THIS)
            elif address == 1:
                return \
                        """@{that}
                        D=M
                        @SP
                        A=M
                        M=D
                        @SP
                        M=M+1
                        """.format(that = defs.THAT)
            else:
                raise NotImplementedError("unknown address for the pointer memory segment %d" %
                        address)
        else:
            raise NotImplementedError("unknown memory segement: (%s, %d)" % (
                segment, address))

    def vm_pop(self, segment, address):
        if segment == "constant":
            raise NotImplementedError("can not do pop into constant memory segment")
        elif segment in ["local", "argument", "this", "that"]:
            return \
                    """@{index}
                    D=A
                    @{segment}
                    A=M+D
                    D=A
                    @SP
                    AM=M-1
                    D=D+M
                    A=D-M
                    D=D-A
                    M=D
                    """.format(index = address, segment = defs.segment2id[segment])
        elif segment == "static":
            return \
                    """@SP
                    AM=M-1
                    D=M
                    @{filename}.{index}
                    M=D
                    """.format(filename = self.outputFile.rstrip(".asm"), 
                               index = address)
        elif segment == "temp":
            return \
                    """@{index}
                    D=A
                    @{temp}
                    A=A+D
                    D=A
                    @SP
                    AM=M-1
                    D=D+M
                    A=D-M
                    D=D-A
                    M=D
                    """.format(index = address, temp=defs.TEMP)
        elif segment == "pointer":
            if address == 0:
                return \
                        """@SP
                        AM=M-1
                        D=M
                        @{this}
                        M=D
                        """.format(this = defs.THIS)
            elif address == 1:
                return \
                        """@SP
                        AM=M-1
                        D=M
                        @{that}
                        M=D
                        """.format(that = defs.THAT)
            else:
                raise NotImplementedError("unknown address for the pointer memory segement %d" %
                        address)
        else:
            raise NotImplementedError("unknown memory segment: (%s, %d)" % (
                segment, address))
