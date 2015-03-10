PYTHON := python
PYFLAKES := pyflakes

default: test

test:
	$(PYTHON) setup.py test

check: test

publish:
	rm -rf dist/*
	$(PYTHON) setup.py sdist bdist_wheel
	gpg --detach-sign -a dist/*
	twine upload dist/*

setup-pypi-test:
	$(PYTHON) setup.py register -r pypitest
	$(PYTHON) setup.py sdist upload -r pypitest

setup-pypi-publish:
	$(PYTHON) setup.py register -r pypi
	$(PYTHON) setup.py sdist upload --sign -r pypi

lint:
	$(PYFLAKES) elv/*.py tests/*.py

clean:
	find . -name '*.pyc' -exec rm -f {} \;
	rm -rf elv.egg-info .eggs build dist
