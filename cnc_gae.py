#!/usr/bin/python3

# [START gae_python310_app]
# [START gae_python3_app]

""" Implementation of the web UI for the CNC using:
    [1] ComplexNumberCalculator class in cnc.py,
    [2] HP35Stack class implemented in hp35stack.py
    [3] DebugTrace class implemented in trace_debug.py

Started 2024-08-22 by Marc Donner

Copyright (C) 2024 Marc Donner

"""

# ----- Python Libraries ----- #
from flask import Flask, redirect, render_template, request, url_for

# ----- Calculator libraries ----- #
from cnc import ComplexNumberCalculator
from trace_debug import DebugTrace

# ----- Variables ----- #

APPLICATION_NAME = 'CNC-WEB'
DEBUG = DebugTrace(False)

cnc = Flask(__name__)
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
    """ Handle commands submitted with POST operations """
    text = request.form['command']
    cnc_engine.handle_string(text)
    render_template('cnc-35.html',
                           stack=cnc_engine.stack,
                           appname=APPLICATION_NAME)
    return redirect(url_for('index'))

@cnc.route("/button/<bname>")
def button(bname):
    """ Handle a button from the templates/cnc-35.html page """
    cnc_engine.handle_button_by_name(bname)
    render_template('cnc-35.html',
                           stack=cnc_engine.stack,
                           appname=APPLICATION_NAME)
    return redirect(url_for('index'))

# [END gae_python3_app]
# [END gae_python310_app]
