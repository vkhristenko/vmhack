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
        self.currentFunctionName = ""
        self.currentFunctionCalls = 0
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.outputStream.close()

    def setFileName(self, fileName):
        if fileName == self.currentInputFile:
            pass
        else:
            self.currentInputFile = fileName
            self._triggerNewFile()
    
    def _triggerNewFile(self):
        self.outputStream.write("\n// starting to parse a new input file: %s\n" % 
                                self.currentInputFile)

    def generateInit(self):
        self.outputStream.write("\n// bootstrap code\n")
        self.outputStream.write("\n")

    def genCommentLine(self):
        self.outputStream.write("\n// %s\n" % self.inputLine)

    def generateLabel(self, label):
        self.outputStream.write("(%s.%s$%s)\n" % (self.currentInputFile,
            self.currentFunctionName, label))

    def generateGoTo(self, label):
        cmd = """@{label}
0;JMP
""".format(label = label)
        self.outputStream.write(cmd)

    def generateIF(self, label):
        cmd = """@SP
A=M-1 // M = RAM[SP-1]
D=M // store the stack's top in D-register

@SP
M=M-1 // sp--

@{label}
D;JNE
""".format(label = label)
        self.outputStream.write(cmd)

    def generateFunction(self, fname, nlocal):
        self.currentFunctionName = fname 
        self.currentFunctionCalls = 0
        cmd = """
({fileName}.{funcName})
""".format(funcName=fname, fileName = self.currentInputFile)
        self.outputStream.write(cmd)
        # intialize local memory segement
        for i in range(nlocal):
            self.generatePushPop(defs.C_PUSH, "constant", 0)

    def generateCall(self, fname, nargs):
        # generate the return label 
        returnAddressLabel = "{fileName}.{funcName}$ret.{index}".format(
            fileName = self.currentFileName,
            funcName = self.currentFunctionName,
            index = self.currentFunctionCall)
        self.currentFunctionCall = self.currentFunctionCall + 1

        # push the return address to the stack
        self.generatePushPop(defs.C_PUSH, "constant", returnAddressLabel)

        # save the caller's frame!
        # LCL, ARG, THIS, THAT addresses of memory segments to reset them back to 
        def _quickGenCMD(reg):
            return """@{value}
D=M
@SP
A=M
M=D
@SP
M=M+1
""".format(value = reg)
        self.outputStream.write(_quickGenCMD("LCL"))
        self.outputStream.write(_quickGenCMD("ARG"))
        self.outputStream.write(_quickGenCMD("THIS"))
        self.outputStream.write(_quickGenCMD("THAT"))

        # reposition ARG and LCL
        cmd = """// ARG = SP - 5 - nARGs
@{nArgs}
D=A
@5
D=D+A
@SP
D=M-D
@ARG
M=D

// LCL = SP
@SP
D=M
@LCL
M=D
""".format(nArgs = nargs)
        self.oututStream.write(cmd)

        # goto the function that is called
        self.generateGoTo(fname)

        # need to declare a label for the called function to return to
        self.outputStream.write("({returnAddress})\n".format(
            returnAddress=returnAddressLabel))

    def generateReturn(self):
        cmd = """@LCL
D=M
@{TMP0}
M=D // endFrame = LCL

@5
D=A
@{TMP0}
D=M-D
A=D // *(endFrame - 5)
D=M // D = returnAddress
@{TMP1}
M=D

// pop the top value on the stack into *arg
""".format(TMP0=defs.segment2id["temp"], TMP1=(defs.segment2id["temp"]+1))
        self.outputStream.write(cmd)
        self.generatePushPop(defs.C_POP, "argument", 0)
        cmd = """// SP = ARG+1
@ARG
D=M+1
@SP
M=D

// THAT = *(endFrame - 1)
@{TMP0}
A=M-1
D=M
@THAT
M=D

// THIS = *(endFrame - 2)
@2
D=A
@{TMP0}
A=M-D
@THIS
M=D

// ARG = *(endFrame - 3)
@3
D=A
@{TMP0}
A=M-D
@ARG
M=D

// LCL = *(endFrame - 4)
@4
D=A
@{TMP0}
A=M-D
@LCL
M=D

// goto returnAddress
@{TMP1}
0;JMP
""".format(TMP0=defs.segment2id["temp"], TMP1=(defs.segment2id["temp"]+1))
        self.outputStream.write(cmd)

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
        return template % "D+M"

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
A=D+M
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
A=D+M
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
