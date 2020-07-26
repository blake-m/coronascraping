import logging
import os

from flask import Flask, request, url_for, send_from_directory

from receiver import settings

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['RECEIVED_FOLDER'] = settings.RECEIVED_FOLDER


def allowed_file(filename: str) -> bool:
    is_allowed = any([filename.endswith(file_extention)
                      for file_extention in settings.ALLOWED_EXTENSIONS])
    return is_allowed


@app.route('/', methods=["GET", "POST"])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['RECEIVED_FOLDER'], filename))
            return url_for('uploaded_file',
                           filename=filename)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['RECEIVED_FOLDER'],
                               filename)


if __name__ == '__main__':
    app.run("0.0.0.0", port="5000", debug=True)
