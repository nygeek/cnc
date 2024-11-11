"""

main.py - root of GAE cnc calculator.

"""

# Started 2024-09-28 by Marc Donner
# Contact: marc.donner@gmail.com

# [START gae_python310_app]
# [START gae_python3_app]

from flask import Flask, render_template, redirect, url_for, request

from cnc import ComplexNumberCalculator
# from trace_debug import DebugTrace

# from flaskr.db import get_db

# from werkzeug.security import check_password_hash, generate_password_hash

# bp = Blueprint('auth', __name__, url_prefix='/auth')

# import functools

app = Flask(__name__)
app.secret_key = 'do5XKxpBdY_JyqOYpnSLvA'
cnc_engine = ComplexNumberCalculator(stack_depth=8, clamp=1e-10)
# cnc_engine.stack.push(complex(17))
APPLICATION_NAME = "CNC_GAE"

@app.route("/")
def index():
    """ display the calculator framework """
    return render_template('cnc-35.html',
                           stack=cnc_engine.stack,
                           appname=APPLICATION_NAME)

@app.route("/", methods=["POST"])
def handle_post_form():
    """ handle typed input """
    text = request.form['command']
    cnc_engine.handle_string(text)
    render_template('cnc-35.html',
                           stack=cnc_engine.stack,
                           appname=APPLICATION_NAME)
    return redirect(url_for('index'))

@app.route("/button/<bname>")
def button(bname):
    """ handle a button """
    cnc_engine.handle_button_by_name(bname)
    render_template('cnc-35.html',
                           stack=cnc_engine.stack,
                           appname=APPLICATION_NAME)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)

# [END gae_python3_app]
# [END gae_python310_app]
