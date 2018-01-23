"""
Driver: VM Translator
"""

import sys, os
from parser import Parser
from codegen import CodeGen
import logging

def translate(inputFile):
    """
    Main Driver: translate the Hack VM code into the Hack Assembly Instructions
    """
    logger.info("Compiling hack vm file: %s" % inputFile)
    with Parser(inputFile) as p:
        outputFile = inputFile.replace(".vm", ".asm")
        with CodeGen(outputFile) as cg:

if __name__ == "__main__":
    #
    # get the option parser set up
    # 
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("--inputFile", dest="inputFile", default=None,
        help="File to translate")

    #
    # parse the input arguments
    # 
    opts, args = parser.parse_args()
    if not opts.inputFile: parser.error("Missing input file to translate")

    #
    # Start the translation
    #
    translate(inputFile=opts.inputFile)
