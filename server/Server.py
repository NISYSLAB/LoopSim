from flask import render_template
from flask import Flask, request, send_file
from werkzeug.utils import secure_filename
import os
import logging
import glob
from flask import jsonify

logging.basicConfig(level=logging.INFO)

# Initialize the flask
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

SEPARATOR = "/"
WORKDIR = "userfiles/"

@app.route('/')
def hello_world():
    return render_template('home.html')

# ctl -> /ctl/test?return=u
# Check the init() is executed by confirming the existence of WORKDIR + test
# Check the content for binary data, executable, "invalid" text.

# pm -> /pm/test?return=ym
# Check the init() is executed by confirming the existence of workdir + test
# Check the content for binary data, executable, "invalid" text.

# cleanup()
# @app.route('/clean/<name>', methods=['DELETE'])


# Run from one of the clients as the initial step
@app.route('/init/<dirname>', methods=['POST']) # POST has u and ym
def init(dirname=None):
    initialized = False
    logging.info("Init Request received for: %s", dirname)
    # Get the file from the POST request
    f1 = request.files['file1']
    f2 = request.files['file2']
    if not (os.path.exists(WORKDIR + secure_filename(dirname))):
        os.makedirs(WORKDIR + secure_filename(dirname))
        initialized = True
    else:
        files = glob.glob(WORKDIR + secure_filename(dirname) + SEPARATOR + "*")
        for f in files:
            os.remove(f)
        initialized = True
    while not initialized:
        time.sleep(1)
    f1.save(WORKDIR + secure_filename(dirname) + SEPARATOR + secure_filename(f1.filename))
    f2.save(WORKDIR + secure_filename(dirname) + SEPARATOR + secure_filename(f2.filename))

    resp = jsonify(success=True)
    return resp

# Run when a POST is made to /ctl/<dirname>. For example, /ctl/test
@app.route('/ctl/<dirname>', methods=['POST'])
def ctl(dirname=None):
    logging.info("CTL Request received for: %s", dirname)
    # Get the file from the POST request
    f1 = request.files['file1']
    f1.save(WORKDIR + secure_filename(dirname) + SEPARATOR + secure_filename(f1.filename))
    return send_file(WORKDIR + secure_filename(dirname) + SEPARATOR + 'u', mimetype='text/plain')


# Run when a POST is made to /pm/<dirname>. For example, /pm/test
@app.route('/pm/<dirname>', methods=['POST'])
def pm(dirname=None):
    logging.info("PM request received for: %s", dirname)
    # Get the file from the POST request
    f1 = request.files['file1']
    f1.save(WORKDIR + secure_filename(dirname) + SEPARATOR + secure_filename(f1.filename))
    return send_file(WORKDIR + secure_filename(dirname) + SEPARATOR + 'ym', mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
