from flask import render_template
from flask import Flask, request, send_file
from werkzeug.utils import secure_filename
import os
import logging
logging.basicConfig(level=logging.INFO)

# Initialize the flask
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('home.html')


# Run when a POST is made to /ctl
@app.route('/ctl', methods=['POST'])
def pw():
    # Get the file from the POST request
    f1 = request.files['file1']
    f1.save(secure_filename(f1.filename))
    return send_file('u', mimetype='text/plain')


# Run when a POST is made to /pm
@app.route('/pm', methods=['POST'])
def cw():
    # Get the file from the POST request
    f1 = request.files['file1']
    f1.save(secure_filename(f1.filename))
    return send_file('ym', mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
