"""

main.py - root of GAE cnc calculator.

"""

# Started 2024-09-28 by Marc Donner
# Contact: marc.donner@gmail.com

# [START gae_python310_app]
# [START gae_python3_app]

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

from cnc import ComplexNumberCalculator
from trace_debug import DebugTrace

APPLICATION_NAME = 'CNC-GAE'
DEBUG = DebugTrace(False)

app = Flask(APPLICATION_NAME)
app.secret_key = '17ff751d08cf47eda51d8856f9e193ee73099b10944809728d4534c953fadd3b'

cnc_engine = ComplexNumberCalculator(stack_depth=8, clamp=1e-10)
cnc_engine.stack.push(complex(17))

@app.route("/")
def index():
    """ display the calculator framework """
    _tag = request.cookies.get('username')
    resp = make_response(render_template('cnc-35.html',
                           stack=cnc_engine.stack,
                           appname=APPLICATION_NAME,
                           tape=cnc_engine.log))
    resp.set_cookie('username', 'marc')
    flash("Cookie set.")
    return resp

@app.route("/", methods=["POST"])
def handle_post_form():
    """ handle typed input """
    text = request.form['command']
    (_rc, message) = cnc_engine.handle_string(text)
    if _rc == -1:
        # print(f"error: '{message}', text: {text}")
        flash('error: ' + message + ' text: ' + text)
    # render_template('cnc-35.html',
    #                        stack=cnc_engine.stack,
    #                        appname=APPLICATION_NAME,
    #                        tape=cnc_engine.log)
    return redirect(url_for('index'))

@app.route("/button/<bname>")
def button(bname):
    """ handle a button """
    cnc_engine.handle_button_by_name(bname)
    # render_template('cnc-35.html',
    #                        stack=cnc_engine.stack,
    #                        appname=APPLICATION_NAME,
    #                        tape=cnc_engine.log)
    return redirect(url_for('index'))


@app.route("/digit/<dig>")
def digit(dig):
    """ handle a digit button click """
    (_x, num) = cnc_engine.digit(dig)
    flash(f'dig: {dig}, num: {num}')
    # render_template('cnc-35.html',
    #                        stack=cnc_engine.stack,
    #                        appname=APPLICATION_NAME,
    #                        tape=cnc_engine.log)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)

# [END gae_python3_app]
# [END gae_python310_app]
