""" 

cnc_flask.py - root of flask cnc calculator.

Implementation of the web UI for the CNC using:
    [1] ComplexNumberCalculator class in cnc.py,
    [2] HP35Stack class implemented in hp35stack.py
    [3] DebugTrace class implemented in trace_debug.py

Started 2024-08-22 by Marc Donner

Copyright (C) 2024 Marc Donner

$Id$

"""

# Started 2024-09-28 by Marc Donner
# Contact: marc.donner@gmail.com

# [START gae_python310_app]
# [START gae_python3_app]

# ----- Python Libraries ----- #

import os

from flask import (
        Flask,
        flash,
        make_response,
        redirect,
        render_template,
        request,
#       session,
        url_for
        )

# ----- Calculator libraries ----- #
from cnc import ComplexNumberCalculator
from trace_debug import DebugTrace
from secret_stash import SecretStash

# ----- Variables ----- #
APPLICATION_NAME = 'CNC-Flask'
DEBUG = DebugTrace(False)

stash = SecretStash()
app = Flask(APPLICATION_NAME)

app.secret_key = stash.get_secret()

cnc_engine = ComplexNumberCalculator(stack_depth=8, clamp=1e-10)

@app.route("/")
def index():
    """ display the calculator framework """
    cnc_stack_json = request.cookies.get('cnc_stack')
    if cnc_stack_json is None:
        resp.set_cookie('cnc_stack', cnc_engine.stack.stack_to_json())
    else:
        cnc_engine.stack.load_stack_from_json(cnc_stack_json)
    resp = make_response(render_template('cnc-35.html',
            stack=cnc_engine.stack,
            appname=APPLICATION_NAME,
            tape=cnc_engine.log))
    return resp

@app.route("/", methods=["POST"])
def handle_post_form():
    """ handle text input from the form """
    text = request.form['command']
    (_rc, message) = cnc_engine.handle_string(text)
    if _rc == -1:
        flash('error: ' + message)
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('cnc_stack', cnc_engine.stack.stack_to_json())
    return resp

@app.route("/button/<bname>")
def button(bname):
    """ handle a button click """
    cnc_engine.handle_button_by_name(bname)
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('cnc_stack', cnc_engine.stack.stack_to_json())
    return resp

@app.route("/digit/<dig>")
def digit(dig):
    """ handle a digit button click """
    (_x, _num) = cnc_engine.digit(dig)
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('cnc_stack', cnc_engine.stack.stack_to_json())
    return resp

@app.route("/status")
def status():
    """ report the status of the appengine system """
    cnc_stack_json = request.cookies.get('cnc_stack')
    # print(f"cookie_value: {cnc_stack_json}")
    return render_template('status.html',
                           environ=os.environ,
                           cookie=cnc_stack_json)