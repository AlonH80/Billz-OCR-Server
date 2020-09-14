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
    res = Response()
    res.data = "Welcome to Billz-OCR-Server!"
    res.headers.set('Access-Control-Allow-Origin', '*')
    return res


@app.route("/uploadFile", methods=['POST'])
def upload_file():
    file = request.files["billFile"]
    bill_type = request.form.get("bill_type")
    # form = request.form.get("cycle_billing"), request.form.get("bill_type")
    file_name = "{}/{}".format(os.getcwd(), file.filename)
    print("Save file: {}".format(file_name))
    file.save(file_name)
    print("Processing file {}".format(file_name))
    result = process_file(file_name)
    print("Processing file {} done, send back response".format(file_name))
    res = Response()
    res.data = result
    res.headers.set('Access-Control-Allow-Origin', '*')
    return res


if __name__ == '__main__':
    port = os.environ.get("PORT") or 5000
    app.run(host='0.0.0.0', port=port)
