#
# Stibitz project Makefile
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

DIRS = "."
DIRPATH = "~/projects/p/python/stibitz/"

.PHONY: help
help:
	cat Makefile
	echo "OS: " ${OS}
	echo "DATE: " ${DATE}

PYTHON_SOURCE = \
	cnc.py \
	debug.py \
	hp35stack.py \
	new_shell.py

SOURCE = \
	 ${PYTHON_SOURCE} \
	 Makefile \
	 .gitignore \
	 README.md

.PHONY: clean pylint listings test lint ci

FILES = \
	${SOURCE} \
	pylintrc

clean:
	- rm *.ps *.pdf

ci:
	ci -l ${FILES}

pylint:
	- pylint cnc.py
	- pylint debug.py
	- pylint hp35stack.py
	- pylint new_shell.py

lint: pylint

test:
	${PYTHON} new_shell.py

listings:\
	listing-cnc.pdf \
	listing-debug.pdf \
	listing-hp35stack.pdf \
	listing-Makefile.pdf \
	listing-new_shell.pdf
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
	git describe --abbrev=4 --dirty --always --tags > version.txt

# This brings the local copy into sync with the remote (main)
pull: .gitattributes
	git pull origin main

version.txt: ${FORCE}
	git describe --abbrev=4 --dirty --always --tags > version.txt

log: .gitattributes
	git log --pretty=oneline
