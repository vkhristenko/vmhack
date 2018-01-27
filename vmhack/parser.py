"""
Parser module
"""
import logging, re
import defs

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
        """
        keep reading lines from the input stream until the line is not a white space
        """
        logging.debug("hasMoreCommands start")
        while True:
            line = self.inputStream.readline()
            logging.debug("line = \"%s\"" % line)
            
            # check if this is a comment or or just an empty string of spaces
            m_comment = re.match(defs.RE_LINECOMMENT, line)
            m_empty = re.match(defs.RE_EMPTYLINE, line)

            # if both are not matched -> valid string -> save the string and exit
            if not m_comment and not m_empty:
                self.inputLine = line
                return True


    def advance(self):
        """
        pass the input line
        """
        # log
        logging.debug("advane start")
        logging.debug("parse the input line: %s" % self.inputLine)

        # match to determine the type of the command
        m_pushpop = re.match(defs.RE_PUSHORPOP, self.inputLine)
        m_arithmetic = re.match(defs.RE_ARITHMETIC, self.inputLine)

        if m_pushpop is not None:
            pass
        elif m_arithmetic is not None:
            pass
        else:
            raise NotImplementedError("Unsupported VM command type: %s" % self.inputLine)

    def commandType(self):
        return None

    def arg1(self):
        return None

    def arg2(self):
        return None
