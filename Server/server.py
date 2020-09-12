from flask import Flask, request, send_file, send_from_directory, url_for, Response
from os import listdir, getcwd
from os.path import isdir, isfile, abspath
import jinja2 as jin
import base64
import os
from Engine.BillzOCR import process_file


root_folder = getcwd() + "/"
app = Flask(__name__, root_path=root_folder, static_url_path=root_folder)

def generate_html(html_template_path: str, input_values: dict):
    html_temp = read_file(html_template_path)
    jin_temp = jin.Template(html_temp)
    html_rend = jin_temp.render(input_values)
    return html_rend


def get_json_from_request():
    req = request
    # return json.loads(req.get_data().decode())


def read_file(file_path: str):
    with open(file_path, "rb") as file:
        return file.read()


@app.route("/uploadFile", methods=['POST'])
def upload_file():
    file = request.files["billFile"]
    form = request.form.get("cycle_billing"), request.form.get("bill_type")
    file_name = "{}/{}".format(os.getcwd(), file.filename)
    file.save(file_name)
    process_file(file_name)
    return {"status": "ok"}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8055)
