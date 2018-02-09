"""
Code Generation Module
"""

import defs

#
# Template for the majoarity of arithmetic commands
#
template = "\n".join([
        "@SP",
        "AM=M-1",
        "D=M",
        "A=A-1",
        "M=%s"])

class CodeGen(object):
    def __init__(self, outputPath, shouldGenBootstrap):
        self.outputPath = outputPath
        self.shouldBootstrap = shouldGenBootstrap
        self.currentInputFile = ""

    def __enter__(self):
        self.outputStream = open(self.outputPath, "w")
        self.cmdindex = 0
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.outputStream.close()

    def setFileName(self, fileName):
        if fileName == self.currentInputFile:
            pass
        else:
            self.currentInputFile = fileName
            self.triggerNewFile()
    
    def _triggerNewFile(self):
        self.outputStream.write("\n// starting to parse a new input file: %s\n" % 
                                self.currentInputFile)

    def generateInit(self):
        self.outputStream.write("\n// bootstrap code\n")
        self.outputStream.write("")

    def genCommentLine(self):
        self.outputStream.write("\n// %s\n" % self.inputLine)

    def generateLabel(self, label):
        self.outputStream.write("(%s)\n" % label)

    def generateGoTo(self, label):
        cmd = """@({label})
JMP
""".format(label = label)
        self.outputStream.write(cmd)

    def generateIF(self, label):
        cmd = """@({label})
@SP
A=M-1 // M = RAM[SP-1]
D=M // store the stack's top in D-register

@SP
M=M-1 // sp--

@{label}
D;JNE
""".format(label = label)
        self.outputStream.write(cmd)

    def generateFunction(self, fname, nlocal):
        pass

    def generateCall(self, fname, nargs):
        pass

    def generateReturn(self):
        pass

    def generateArithmetic(self, acmd):
        if acmd == "add":
            asm = self.vm_add()
        elif acmd == "sub":
            asm = self.vm_sub()
        elif acmd == "neg":
            asm = self.vm_neg()
        elif acmd == "eq":
            asm = self.vm_eq()
        elif acmd == "gt":
            asm = self.vm_gt()
        elif acmd == "lt":
            asm = self.vm_lt()
        elif acmd == "and":
            asm = self.vm_and()
        elif acmd == "or":
            asm = self.vm_or()
        elif acmd == "not":
            asm = self.vm_not()
        else:
            raise NotImplementedError("unknown arithmetic command: %s" % acmd)

        #
        # write out the actual assembly instructions per given VM command
        #
        self.outputStream.write("%s\n" % asm)

    def vm_add(self):
        return template % "M+D"

    def vm_sub(self):
        return template % "M-D"

    def vm_neg(self):
        return "\n".join([
                "@SP",
                "A=M-1",
                "M=-M"])

    def vm_eq(self):
        gened = """@SP
AM=M-1
D=M
A=A-1
D=M-D

@EQ_TRUE_{index}
D;JEQ
@EQ_FALSE_{index}
D;JNE

(EQ_TRUE_{index})
@RETURN_ADDRESS_{index}
D=-1;JMP
(EQ_FALSE_{index})
@RETURN_ADDRESS_{index}
D=0;JMP

(RETURN_ADDRESS_{index})
@SP
A=M-1
M=D
""".format(index=self.cmdindex)
        self.cmdindex = self.cmdindex + 1 
        return gened

    def vm_gt(self):
        gened = """@SP
AM=M-1
D=M
A=A-1
D=M-D

@GT_TRUE_{index}
D;JGT
@GT_FALSE_{index}
D;JLE

(GT_TRUE_{index})
@RETURN_ADDRESS_{index}
D=-1;JMP
(GT_FALSE_{index})
@RETURN_ADDRESS_{index}
D=0;JMP                

(RETURN_ADDRESS_{index})
@SP
A=M-1
M=D
""".format(index=self.cmdindex)
        self.cmdindex = self.cmdindex + 1
        return gened

    def vm_lt(self):
        gened = """@SP
AM=M-1
D=M
A=A-1
D=M-D

@LT_TRUE_{index}
D;JLT
@LT_FALSE_{index}
D;JGE

(LT_TRUE_{index})
@RETURN_ADDRESS_{index}
D=-1;JMP
(LT_FALSE_{index})
@RETURN_ADDRESS_{index}
D=0;JMP                

(RETURN_ADDRESS_{index})
@SP
A=M-1
M=D
""".format(index = self.cmdindex)
        self.cmdindex = self.cmdindex + 1
        return gened

    def vm_and(self):
        return template % "D&M"

    def vm_or(self):
        return template % "D|M"

    def vm_not(self):
        return \
                """@SP
A=M-1
M=!M
"""

    def generatePushPop(self, memcmd, segment, address):
        if memcmd == defs.C_PUSH:
            asm = self.vm_push(segment, address)
        elif memcmd == defs.C_POP:
            asm = self.vm_pop(segment, address)
        else:
            raise NotImplementedError("unknown memory access command (%d, %s, %d)" % 
                    (memcmd, segment, address))

        self.outputStream.write("%s\n" % asm)

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
""".format(filename=self.outputFile.rstrip(".asm").split("/")[-1],
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
""".format(filename = self.outputFile.rstrip(".asm").split("/")[-1], 
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
                raise NotImplementedError("unknown address for the pointer memory segement %s" % str(address))
        else:
            raise NotImplementedError("unknown memory segment: (%s, %d)" % (
                segment, address))
