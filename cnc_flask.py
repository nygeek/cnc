#!/usr/bin/python3

""" Implementation of the web UI for the CNC using:
    [1] ComplexNumberCalculator class in cnc.py,
    [2] HP35Stack class implemented in hp35stack.py
    [3] DebugTrace class implemented in trace_debug.py

Started 2024-08-22 by Marc Donner

Copyright (C) 2024 Marc Donner

$Id$

"""

# ----- Python Libraries ----- #
from flask import Flask, flash, redirect, render_template, request, url_for

# ----- Calculator libraries ----- #
from cnc import ComplexNumberCalculator
from trace_debug import DebugTrace

# ----- Variables ----- #

APPLICATION_NAME = 'CNC-WEB'
DEBUG = DebugTrace(False)

cnc = Flask(__name__)
cnc.secret_key = 'do5XKxpBdY_JyqOYpnSLvA'
cnc_engine = ComplexNumberCalculator(stack_depth=8, clamp=1e-10)
cnc_engine.stack.push(complex(17))

@cnc.route("/")
def index():
    """ display the calculator framework """
    return render_template('cnc-35.html',
                           stack=cnc_engine.stack,
                           appname=APPLICATION_NAME)

@cnc.route("/", methods=["POST"])
def handle_post_form():
    text = request.form['command']
    cnc_engine.handle_string(text)
    render_template('cnc-35.html',
                           stack=cnc_engine.stack,
                           appname=APPLICATION_NAME)
    return redirect(url_for('index'))

@cnc.route("/button/<bname>")
def button(bname):
    cnc_engine.handle_button_by_name(bname)
    render_template('cnc-35.html',
                           stack=cnc_engine.stack,
                           appname=APPLICATION_NAME)
    return redirect(url_for('index'))

