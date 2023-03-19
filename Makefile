MOVIEPY_INSTALL=$(HOME)/.local/lib/python3.9/site-packages/moviepy/__init__.py


gestalt-test.mp4: test.mp4 preconditions
	./gestalt.py -i test.mp4 -g -v 

preconditions: /usr/bin/python $(MOVIEPY_INSTALL)

$(MOVIEPY_INSTALL): /usr/bin/pip
	pip install moviepy

/usr/bin/pip:
	sudo apt-get install pip


/usr/bin/python3:
	sudo apt-get install python3

im:
	sudo apt-get install imagemagick
