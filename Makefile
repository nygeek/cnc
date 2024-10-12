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
	echo "DATE: " ${DATE}
	echo "HERE: " ${HERE}

PYTHON_SOURCE = \
	trace_debug.py \
	hp35stack.py \
	cnc_shell.py

SOURCE = \
	 ${PYTHON_SOURCE} \
	 cnc-35.html \
	 cnc.sh \
	 Makefile \
	 .gitignore \
	 README.md

.PHONY: clean pylint listings test lint ci

FILES = \
	${SOURCE} \
	pylintrc

.phony: install
install: 
	echo 'python3' ${HERE}/cnc_shell.py '$$*' > cnc.sh
	cp cnc.sh ${HOME}/bin/cnc
	chmod +x ${HOME}/bin/cnc

clean:
	- rm *.ps *.pdf

pylint:
	- ${PYLINT} trace_debug.py
	- ${PYLINT} hp35stack.py
	- ${PYLINT} cnc_shell.py

lint: pylint

test:
	${PYTHON} cnc_shell.py

listings:\
	listing-trace_debug.pdf \
	listing-hp35stack.pdf \
	listing-Makefile.pdf \
	listing-cnc_shell.pdf
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
