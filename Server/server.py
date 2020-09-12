from flask import Flask, request, send_file, send_from_directory, url_for, Response
from os import listdir, getcwd
from os.path import isdir, isfile, abspath
import jinja2 as jin
import base64
import os
from Engine.BillzOCR import process_file


root_folder = getcwd() + "/"
app = Flask(__name__, root_path=root_folder, static_url_path=root_folder)


@app.route("/")
def index():
    return "Welcome to Billz-OCR-Server!"


@app.route("/uploadFile", methods=['POST'])
def upload_file():
    file = request.files["billFile"]
    form = request.form.get("cycle_billing"), request.form.get("bill_type")
    file_name = "{}/{}".format(os.getcwd(), file.filename)
    file.save(file_name)
    process_file(file_name)
    return {"status": "ok"}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ["PORT"])
