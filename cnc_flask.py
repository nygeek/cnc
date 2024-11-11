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
        redirect,
        render_template,
        request,
        url_for,
        session
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
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('cnc-35.html',
                           stack=cnc_engine.stack,
                           username=session["username"],
                           appname=APPLICATION_NAME)

@app.route("/login", methods=['GET', 'POST'])
def login():
    """ log the user in """
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''


@app.route("/", methods=["POST"])
def handle_post_form():
    """ handle text input from the form """
    text = request.form['command']
    cnc_engine.handle_string(text)
    render_template('cnc-35.html',
                           stack=cnc_engine.stack,
                           appname=APPLICATION_NAME)
    return redirect(url_for('index'))

@app.route("/button/<bname>")
def button(bname):
    """ handle a button click """
    if bname == "logout":
        session.pop('username', None)
        return redirect(url_for('index'))
    cnc_engine.handle_button_by_name(bname)
    render_template('cnc-35.html',
                           stack=cnc_engine.stack,
                           appname=APPLICATION_NAME)
    return redirect(url_for('index'))
