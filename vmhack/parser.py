"""
Parser module
"""

class Parser(object):
    """
    - Handles the parsing of a single vm file
    - reads a vm cmd, parses the cmd into its lexical components, and provides convenient
        access to these components
    """
    def __init__(self, inputFile):
        self.inputFile = inputFile

    def __enter__(self):
        self.inputStream = open(inputFile, "r")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.inputStream.close()

    def hasMoreCommands(self):
        return False

    def advance(self):
        pass

    def commandType(self):
        return None

    def arg1(self):
        return None

    def arg2(self):
        return None
