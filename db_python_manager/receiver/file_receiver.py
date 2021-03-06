import logging
import os

import requests
from flask import Flask, request, url_for, send_from_directory, redirect

from db import process
from receiver import settings

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['RECEIVED_FOLDER'] = settings.RECEIVED_FOLDER


def send_reload_command_to_dashboard():
    logging.info("Sending a command to reload the dashboard...")
    url = "http://corona_dashboard:8050/reload_data"

    response = requests.get(url)
    logging.info("Command to reload the dashboard was sent. Response:")
    logging.info(response.text)


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
            path = os.path.join(app.config['RECEIVED_FOLDER'], filename)
            file.save(path)
            logging.info(f"Received file - path: {path}")
            return redirect(url_for('start_db_process', filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


@app.route('/start_db_process/<filename>')
def start_db_process(filename):
    logging.info(f"DB process Process started with file: {filename}")
    process.run(filename)
    send_reload_command_to_dashboard()
    return f"""
    DB process Process finished with file: {filename}
    """


if __name__ == '__main__':
    app.run("0.0.0.0", port="5000", debug=True)
