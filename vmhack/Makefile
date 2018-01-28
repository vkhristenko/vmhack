.PHONY: all clean

all: VMTranslator

VMTranslator:
	echo "#!/bin/bash\n\npython VMTranslator.py --inputFile="\$$"1\n\n" >> VMTranslator
	chmod 755 VMTranslator

clean:
	rm VMTranslator
