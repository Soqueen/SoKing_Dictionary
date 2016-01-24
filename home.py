# -*- coding: utf-8 -*-

import os
import pprint
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug import secure_filename
from tools.tags import foods, get_tag_images, get_tags, get_probs, textToSpeech

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
def send_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename=filename)

@app.route('/show/<filename>')
def uploaded_file(filename):
    result = get_tag_images(filename)
    tags = get_tags(result)
    probs = get_probs(result)

    d = dict(zip(tags, probs))
    pprint.pprint(d)
    r1 = max(d.iterkeys(), key=(lambda k: d[k]))
    r2 = ""
    text = ""
    for tag in tags:
        if tag in foods:
            r2 = tag
            text += r2 + ", "
            # textToSpeech(r2)
    if r1 != r2:
        if r2 not in foods:
            # textToSpeech(r1)
            text += r1 
    # textToSpeech(r)
    return render_template("success.html", filename=filename, text=text)

if __name__ == '__main__':
    app.jinja_env.globals.update(textToSpeech=textToSpeech)
    app.debug = True
    app.run()