2048Playground:
	echo "#!/bin/bash" > 2048Playground
	echo "python3 test.py \"\$$@\"" >> 2048Playground
	chmod u+x 2048Playground
	echo "run ./2048Playground for results!"