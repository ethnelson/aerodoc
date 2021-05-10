SHELL=/bin/bash

help:
	@echo Choose a target \[ help \| setup \| run \| clean \]

setup:
	python3 -m venv packages
	source packages/bin/activate && \
	pip3 install -r requirements.txt && \
	python3 scripts/setup.py


run:
	export FLASK_APP=test.py && \
	export FLASK_ENV=development && \
	source packages/bin/activate && \
	python3 appflask.py

clean:
	pyclean .
	pyclean scripts/
	rm -rf packages
	rm -rf datadb.db
	rm -rf monitor.p
	rm -rf dbBuffer.p
	rm -rf noteBuffer.p
	rm -rf datadb.db
