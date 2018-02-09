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
        self.inputStream = open(self.inputFile, "r")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.inputStream.close()

    def hasMoreCommands(self):
        """
        keep reading lines from the input stream until the line is not a white space
        """
        logging.debug("hasMoreCommands start")
        while True:
            line = self.inputStream.readline()
            if line == "": return False

            # to simplify things a bit -> right strip the line content
            line = line.rstrip()
            logging.debug("next input line = \"%s\"" % line)
            if line == "":
                continue
            
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
        m_label = re.match(defs.RE_LABEL, self.inputLine)
        m_goto = re.match(defs.RE_GOTO, self.inputLine)
        m_if = re.match(defs.RE_IF, self.inputLine)
        m_function = re.match(defs.RE_FUNCTION, self.inputLine)
        m_call = re.match(defs.RE_CALL, self.inputLine)
        m_return = re.match(defs.RE_RETURN, self.inputLine)

        if m_pushpop is not None:
            self.action = m_pushpop.group(1)
            self.segment = m_pushpop.group(2)
            self.value = m_pushpop.group(3)
            if self.action == "push":
                self.ctype = defs.C_PUSH
            elif self.action == "pop":
                self.ctype = defs.C_POP
            else:
                raise NotImplementedError("Matched command (%s) is neither push nor pop" %
                    self.action)
        elif m_arithmetic is not None:
            self.action = m_arithmetic.group(1)
            self.ctype = defs.C_ARITHMETIC
        elif m_label is not None:
            self.ctype = defs.C_LABEL
            self.label = m_label.group(2)
        elif m_goto is not None:
            self.ctype = defs.C_GOTO
            self.label = m_goto.group(2)
        elif m_if is not None:
            self.ctype = defs.C_IF
            self.label = m_if.group(2)
        elif m_function is not None:
            self.ctype = defs.C_FUNCTION
            self.fname = m_function.group(2)
            self.nlocal = m_function.group(3)
        elif m_call is not None:
            self.ctype = defs.C_CALL
            self.fname = m_call.group(2)
            self.nargs = m_call.group(2)
        elif m_return is not None:
            self.ctype = defs.C_RETURN
        else:
            raise NotImplementedError("Unsupported VM command type: %s" % self.inputLine)

    def commandType(self):
        return self.ctype

    def arg1(self):
        if self.ctype == defs.C_PUSH or self.ctype == defs.C_POP:
            return self.segment
        elif self.ctype == defs.C_ARITHMETIC:
            return self.action
        elif (self.ctype == defs.C_LABEL or self.ctype == defs.C_GOTO or
              self.ctype == defs.C_IF):
            return self.label
        elif self.ctype == defs.C_FUNCTION or self.ctype == defs.C_CALL:
            return self.fname
        elif self.ctype == defs.C_RETURN:
            raise NotImplementedError("Parser::arg1 should not be called for C_RETURN command")
        else:
            raise NotImplementedError("Parser::arg1 unknown ctype: " + str(self.ctype))


    def arg2(self):
        if self.ctype == defs.C_PUSH or self.ctype == defs.C_POP:
            return self.value
        elif self.ctype == defs.C_FUNCTION:
            return self.nlocal
        elif self.ctype == defs.C_CALL:
            return self.nargs
        else:
            raise NotImplementedError("Parser::arg2 unknown ctype:" + str(self.ctype))
