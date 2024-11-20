"""

main.py - root of GAE cnc calculator.

Implementation of the web UI for the CNC using:
    [1] ComplexNumberCalculator class in cnc.py,
    [2] HP35Stack class implemented in hp35stack.py
    [3] DebugTrace class implemented in trace_debug.py

Started 2024-08-22 by Marc Donner

Copyright (C) 2024 Marc Donner

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

# ----- Variables ----- #
APPLICATION_NAME = 'CNC-AppEngine'
DEBUG = DebugTrace(False)

app = Flask(APPLICATION_NAME)

cnc_engine = ComplexNumberCalculator(stack_depth=8, clamp=1e-10)
# cnc_engine.stack.push(complex(17))

@app.route("/")
def index():
    """ display the calculator framework """
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
    return redirect(url_for('index'))

@app.route("/button/<bname>")
def button(bname):
    """ handle a button click """
    cnc_engine.handle_button_by_name(bname)
    return redirect(url_for('index'))

@app.route("/digit/<dig>")
def digit(dig):
    """ handle a digit button click """
    (_x, _num) = cnc_engine.digit(dig)
    return redirect(url_for('index'))


@app.route("/status")
def status():
    """ report the status of the appengine system """
    return render_template('status.html', environ=os.environ)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)

# [END gae_python3_app]
# [END gae_python310_app]
