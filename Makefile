SHELL=/bin/bash

help:
	@echo Choose a target \[ help \| setup \| runFlask \| clean \]

setup:
	python3 -m venv packages
	source packages/bin/activate && \
	pip3 install -r requirements.txt

clean:
	py3clean .
	rm -rf packages
