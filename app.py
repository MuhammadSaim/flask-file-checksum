from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import hashlib
import os


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def create_checksum():
    checksum = None
    if request.method == 'POST':
        file = request.files['file']
        new_name = secure_filename(file.filename)
        file.save('static/uploads/'+new_name)
        checksum = sha256(new_name)
        os.remove('static/uploads/'+new_name)
    return render_template('pages/create.html', checksum=checksum)


@app.route('/verify-checksum', methods=['GET', 'POST'])
def verify_checksum():
    status = None
    if request.method == 'POST':
        file = request.files['file']
        checksum = request.form.get('checksum')
        new_name = secure_filename(file.filename)
        file.save('static/uploads/' + new_name)
        new_checksum = sha256(new_name)
        status = checksum == new_checksum
        os.remove('static/uploads/' + new_name)
    return render_template('pages/verify.html', status=status)


def sha256(file_name):
    hash_sha256 = hashlib.sha256()
    with open('static/uploads/'+file_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()


if __name__ == '__main__':
    app.run(debug=True)
