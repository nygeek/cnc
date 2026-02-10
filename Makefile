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

.PHONY: help setup
help:
	cat Makefile
	echo "OS: " ${OS}
	echo "PYTHON: " ${PYTHON}
	echo "DATE: " ${DATE}
	echo "HERE: " ${HERE}

setup:
	@echo "=== SDL2 Setup Instructions for ${OS} ==="
	@echo ""
ifeq (Darwin, ${OS})
	@echo "On macOS, install SDL2 using Homebrew:"
	@echo ""
	@echo "  brew install sdl2 sdl2_gfx sdl2_ttf"
	@echo ""
	@echo "Then run 'make build' to create venv and install Python dependencies."
	@echo "PySDL2 will be installed automatically from requirements.txt."
	@echo ""
else ifeq (Linux, ${OS})
	@echo "On Linux (Ubuntu/Debian), install SDL2 using apt:"
	@echo ""
	@echo "  sudo apt-get update"
	@echo "  sudo apt-get install libsdl2-dev libsdl2-gfx-dev libsdl2-ttf-dev"
	@echo ""
	@echo "On Linux (Fedora/RHEL), install SDL2 using dnf/yum:"
	@echo ""
	@echo "  sudo dnf install SDL2-devel SDL2_gfx-devel SDL2_ttf-devel"
	@echo ""
	@echo "Then run 'make build' to create venv and install Python dependencies."
	@echo "PySDL2 will be installed automatically from requirements.txt."
	@echo ""
else
	@echo "Unsupported OS: ${OS}"
	@echo "Please install SDL2, SDL2_gfx, and SDL2_ttf manually for your system."
	@echo "Then run 'make build' to install Python dependencies."
endif
	@echo "After installation, you can run the GUI calculator with:"
	@echo ""
	@echo "  python3 cnc_gui.py"
	@echo ""

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

.PHONY: build install clean pylint listings test lint ci gui

FILES = \
	${SOURCE} \
	pylintrc

# Virtual environment setup and build
build:
	@if [ ! -d .venv ]; then \
		echo "Creating virtual environment..."; \
		${PYTHON} -m venv .venv; \
	fi
	@echo "Installing project dependencies..."
	.venv/bin/pip install --upgrade pip
	@if [ -f requirements.txt ]; then \
		echo "Installing from requirements.txt..."; \
		.venv/bin/pip install -r requirements.txt; \
	fi
	.venv/bin/pip install -e .

.PHONY: install
install: build 
	echo ${HERE}/.venv/bin/python ${HERE}/cli_cnc.py --binary '$$*' > cnc.sh
	echo ${HERE}/.venv/bin/python ${HERE}/cli_cnc.py --decimal '$$*' > cnc10.sh
	cp cnc.sh ${HOME}/bin/cnc
	cp cnc10.sh ${HOME}/bin/cnc10
	chmod +x ${HOME}/bin/cnc
	chmod +x ${HOME}/bin/cnc10
	- rm cnc.sh
	- rm cnc10.sh

clean:
	- rm -f *.ps *.pdf
	- rm -rf .venv
	- rm -f ${HOME}/bin/cnc ${HOME}/bin/cnc10

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

gui: build
	.venv/bin/python ./cnc_gui.py

screenshot: build
	@mkdir -p _build
	.venv/bin/python ./cnc_gui.py --screenshot _build/hp35_latest.png
	@echo "Screenshot saved to _build/hp35_latest.png"

compare: screenshot
	@mkdir -p _build
	.venv/bin/python ./tests/compare_renders.py images/hp35_reference_cropped.jpg _build/hp35_latest.png _build/hp35_diff_latest.png

test-gui: compare
	@echo "GUI screenshot comparison complete. Check _build/hp35_diff_latest.png for visual differences."

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
