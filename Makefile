#
# CNC project Makefile
#
# $Id$

# Make us OS-independent ... at least for MacOS and Linux
OS := $(shell uname -s)
ifeq (Linux, ${OS})
    DATE := $(shell date --iso-8601)
else
    DATE := $(shell date "+%Y-%m-%d")
endif

# Python version
PYTHON := python3
# PYTHON := python2
# PYLINT := ${PYTHON} -m pylint
PYLINT := pylint

HERE := $(shell pwd)

.PHONY: help
help:
	cat Makefile
	echo "OS: " ${OS}
	echo "PYTHON: " ${PYTHON}
	echo "DATE: " ${DATE}
	echo "HERE: " ${HERE}

PYTHON_SOURCE = \
	cnc.py \
	cnc_flask.py \
	cnc_gae.py \
	cnc_shell.py \
	logcnc.py \
	main.py

SOURCE = \
	${PYTHON_SOURCE} \
	app.yaml \
	.gitignore \
	Makefile \
	README.md \
	requirements.txt \
	static/keyboard.css \
	static/cnc-favicon.png \
	templates/cnc-35.html \
	templates/layout.html \
	templates/info.html 

.PHONY: clean pylint listings test lint ci

FILES = \
	${SOURCE} \
	pylintrc

.PHONY: install
install: 
	echo 'python3' ${HERE}/cnc_shell.py '$$*' > cnc.sh
	cp cnc.sh ${HOME}/bin/cnc
	chmod +x ${HOME}/bin/cnc
	- rm cnc.sh

.PHONY: gae_deploy
gae_deploy:
	gcloud storage rsync ./static gs://complex-35.appspot.com/static
	gcloud storage rsync ./templates gs://complex-35.appspot.com/templates
	gcloud app deploy

clean:
	- rm *.ps *.pdf

pylint:
	- ${PYLINT} cnc_shell.py
	- ${PYLINT} cnc.py
	- ${PYLINT} cnc_flask.py
	- ${PYLINT} cnc_gae.py
	- ${PYLINT} logcnc.py
	- ${PYLINT} main.py

lint: pylint

.PHONY: test
test:
	${PYTHON} ./cnc_shell.py

.PHONY: flask
flask:
	flask --app cnc_flask run

listings:\
	listing-cnc_shell.pdf \
	listing-cnc.pdf
	mv $^ ~/tmp

listing-%.ps: %.py
	enscript -G $< -p $@

listing-Makefile.ps: Makefile
	enscript -G $< -p $@

%.pdf: %.ps
	ps2pdf $< $@
	rm $<

# GIT operations

diff: .gitattributes
	git diff

status: ${FORCE}
	git status

# this brings the remote copy into sync with the local one
commit: .gitattributes
	git commit ${FILES}
	git push -u origin main

# This brings the local copy into sync with the remote (main)
pull: .gitattributes
	git pull origin main

log: .gitattributes
	git log --pretty=oneline
