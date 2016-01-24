# -*- coding: utf-8 -*-

import os
import pprint
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug import secure_filename
from tools.testing import get_tag_images, get_tags, get_probs, textToSpeech

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        # If file exists and
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Move file from temp folder to UPLOAD_FOLDER
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))

    return render_template("home.html")

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    result = get_tag_images("http://www.characters.ca/wp-content/uploads/2015/05/steak.jpg")
    tags = get_tags(result)
    probs = get_probs(result)

    d = dict(zip(tags, probs))
    pprint.pprint(d)
    r = max(d.iterkeys(), key=(lambda k: d[k]))
    textToSpeech(r)
    return render_template("success.html")

if __name__ == '__main__':
    app.debug = True
    app.run()