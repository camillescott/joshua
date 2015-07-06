install:
	python setup.py install

test:
	python setup.py test

clean:
	rm -rf build/ *.pyc joshua/*.pyc joshua/*.egg-info joshua/intervaltree.c
