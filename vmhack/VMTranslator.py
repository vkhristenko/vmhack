"""
Driver: VM Translator
"""

import sys, os
from parser import Parser
from codegen import CodeGen
import defs
import logging

def isdir(path):
    """
    return true if the provided path is a directory, otherwise false on a file
    """
    return os.path.isdir(path)

def basename(path):
    return os.path.basename(path[:-1]) if path[-1] == "/" else os.path.basename(path)

def dirname(path):
    pass

def translate(inputPath):
    """
    Main Driver: translate the Hack VM code into the Hack Assembly Instructions
    """
    logging.info("Compiling hack vm file: %s" % inputPath)
    with Parser(inputPath) as p:
        # build the output path
        if isdir(inputPath):
            outputPath = os.path.join(inputPath, basename(inputPath) + ".asm")
            shouldGenBootstrap = True
        else:
            outputPath = inputPath.replace(".vm", ".asm")
            shouldGenBootstrap = False
        with CodeGen(outputPath, shouldGenBootstrap) as cg:
            while p.hasMoreCommands():
                # fetch the command
                p.advance()
                logging.debug("next vm command: %s" % p.inputLine)

                # dispatch depending on the comamnd that we are dealing with
                cType = p.commandType()
                cg.inputLine = p.inputLine # ...
                # inform the code gen that we changed the input file
                if p.newInputFile(): cg.setFileName(p.inputFile())
                # generate a line that contains the cmd that is going to be translated
                cg.genCommentLine()
                if cType == defs.C_ARITHMETIC:
                    cg.generateArithmetic(p.arg1())
                elif cType == defs.C_PUSH or cType == defs.C_POP:
                    cg.generatePushPop(cType, p.arg1(), int(p.arg2()))
                elif cType == defs.C_LABEL:
                    cg.generateLabel(p.arg1())
                elif cType == defs.C_GOTO:
                    cg.generateGoTo(p.arg1())
                elif cType == defs.C_IF:
                    cg.generateIF(p.arg1())
                elif cType == defs.C_FUNCTION:
                    cg.generateFunction(p.arg1(), int(p.arg2()))
                elif cType == defs.C_CALL:
                    cg.generateCall(p.arg1(), int(p.arg2()))
                elif cType == defs.C_RETURN:
                    cg.generateReturn()
                else:
                    raise NotImplementedError("Unsupported command type: %d" % cType)

    logging.info("Finished compiling hack inputPath: %s" % inputPath)

if __name__ == "__main__":
    #
    # get the option parser set up
    # 
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("--inputPath", dest="inputPath", default=None,
        help="File to translate")
    parser.add_option("--logLevel", dest="logLevel", default=logging.INFO,
        help="Level of the logging facility")

    #
    # parse the input arguments
    # 
    opts, args = parser.parse_args()
    if not opts.inputPath: parser.error("Missing input file to translate")
    
    #
    # set up the logging facility
    #
    logging.basicConfig(level = int(opts.logLevel))

    #
    # Start the translation
    #
    translate(inputPath=opts.inputPath)
