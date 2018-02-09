.PHONY: all clean

all: VMTranslator

VMTranslator:
	echo "#!/bin/bash" >> VMTranslator
	echo "python VMTranslator.py --inputPath="\$$"1" >> VMTranslator
	chmod 755 VMTranslator

clean:
	rm VMTranslator
