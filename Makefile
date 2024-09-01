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
				cnc_shell.py

SOURCE = \
		 ${PYTHON_SOURCE} \
		 Makefile \
		 README.md

.PHONY: clean pylint listing test lint ci

FILES = \
		${SOURCE} \
		pylintrc \
		version.txt

clean:

ci:
	ci -l ${FILES}

pylint:
	- pylint cnc.py

lint: pylint

test:
	${PYTHON} cnc.py

listing:
	enscript -G cnc.py -p listing-cnc.ps
	ps2pdf listing-cnc.ps listing-cnc.pdf

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
