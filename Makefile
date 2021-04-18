SHELL=/bin/bash

help:
	@echo Choose a target \[ help \| setup \| runFlask \| clean \]

setup:
	python3 -m venv packages
	source packages/bin/activate && \
	pip3 install -r requirements.txt


run:
	export FLASK_APP=test.py && \
	export FLASK_ENV=development && \
	source packages/bin/activate && \
	flask run

clean:
	py3clean .
	rm -rf packages
	rm -rf datadb.db
