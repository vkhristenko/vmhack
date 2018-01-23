"""
Code Generation Module
"""

class CodeGen(object):
    def __init__(self, outputFile):
        self.outputFile = outputFile

    def __enter__(self):
        self.outputStream = open(self.inputFile, "w")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.outputFile.close()
