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


# Run when a POST is made to /ctl/<name>. For example, /ctl/test
@app.route('/ctl/<name>', methods=['POST'])
def ctl(name=None):
    logging.info("CTL Request received for: %s", name)
    # Get the file from the POST request
    f1 = request.files['file1']
    f1.save(secure_filename(name) + "/" + f1.filename)
    return send_file(name + "/" + 'u', mimetype='text/plain')


# Run when a POST is made to /pm/<name>. For example, /pm/test
@app.route('/pm/<name>', methods=['POST'])
def pm(name=None):
    logging.info("PM Request received for: %s", name)
    # Get the file from the POST request
    f1 = request.files['file1']
    f1.save(secure_filename(name) + "/" + f1.filename)
    return send_file(name + "/" + 'ym', mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
