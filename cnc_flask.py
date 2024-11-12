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
from flask import (
        Flask,
        flash,
        make_response,
        redirect,
        render_template,
        request,
        session,
        url_for
        )

# ----- Calculator libraries ----- #
from cnc import ComplexNumberCalculator
from trace_debug import DebugTrace

# ----- Variables ----- #

APPLICATION_NAME = 'CNC-WEB'
DEBUG = DebugTrace(False)

app = Flask(__name__)
app.secret_key = '17ff751d08cf47eda51d8856f9e193ee73099b10944809728d4534c953fadd3b'
cnc_engine = ComplexNumberCalculator(stack_depth=8, clamp=1e-10)
cnc_engine.stack.push(complex(17))

@app.route("/")
def index():
    """ display the calculator framework """
    _tag = request.cookies.get('username')
    resp = make_response(render_template('cnc-35.html',
                         stack=cnc_engine.stack,
                         username=_tag,
                         appname=APPLICATION_NAME))
    resp.set_cookie('username', 'marc')
    flash("Cookie set.")
    return resp


@app.route("/", methods=["POST"])
def handle_post_form():
    """ handle text input from the form """
    text = request.form['command']
    cnc_engine.handle_string(text)
    flash(f'text: {text}')
    render_template('cnc-35.html',
                           stack=cnc_engine.stack,
                           appname=APPLICATION_NAME)
    return redirect(url_for('index'))


@app.route("/digit/<dig>")
def digit(dig):
    """ handle a digit button click """
    (_x, num) = cnc_engine.digit(dig)
    flash(f'dig: {dig}, num: {num}')
    render_template('cnc-35.html',
                           stack=cnc_engine.stack,
                           appname=APPLICATION_NAME)
    return redirect(url_for('index'))


@app.route("/button/<bname>")
def button(bname):
    """ handle a button click """
    cnc_engine.handle_button_by_name(bname)
    flash(f'bname: {bname}')
    render_template('cnc-35.html',
                           stack=cnc_engine.stack,
                           appname=APPLICATION_NAME)
    return redirect(url_for('index'))
