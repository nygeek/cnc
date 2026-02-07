#
# CNC project Makefile
#
# SPDX-License-Identifier: MIT
# Copyright (C) 2026 NYGeek LLC
#

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
	cli_cnc.py \
	cnc.py \
	cnc10.py \
	hp35stack.py \
	logcnc.py \

SOURCE = \
	${PYTHON_SOURCE} \
	.gitignore \
	LICENSE \
	Makefile \
	README.md

.PHONY: clean pylint listings test lint ci

FILES = \
	${SOURCE} \
	pylintrc

.PHONY: install
install: 
	echo ${HERE}/.venv/bin/python ${HERE}/cli_cnc.py --binary '$$*' > cnc.sh
	echo ${HERE}/.venv/bin/python ${HERE}/cli_cnc.py --decimal '$$*' > cnc10.sh
	cp cnc.sh ${HOME}/bin/cnc
	cp cnc10.sh ${HOME}/bin/cnc10
	chmod +x ${HOME}/bin/cnc
	chmod +x ${HOME}/bin/cnc10
	- rm cnc.sh
	- rm cnc10.sh

clean:
	- rm *.ps *.pdf

pylint:
	- ${PYLINT} cli_cnc.py
	- ${PYLINT} cnc.py
	- ${PYLINT} cnc10.py
	- ${PYLINT} logcnc.py

lint: pylint

.PHONY: test decimal binary
test:
	${PYTHON} ./cli_cnc.py

decimal:
	${PYTHON} ./cli_cnc.py --decimal

binary:
	${PYTHON} ./cli_cnc.py --binary

LISTINGS = cnc.pdf cnc10.pdf hp35stack.pdf Makefile.pdf cli_cnc.pdf

listings: ${LISTINGS}
	mv ${LISTINGS} ~/tmp

%.ps: %.py
	enscript -G $< -p $@

Makefile.ps: Makefile
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
