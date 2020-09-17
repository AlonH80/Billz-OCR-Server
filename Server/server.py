from flask import Flask, request, send_file, send_from_directory, url_for, Response
from os import listdir, getcwd
from os.path import isdir, isfile, abspath
import jinja2 as jin
import base64
import os
from Engine.BillzOCR import process_file, pending_queue
import random
from threading import Thread
import json


root_folder = getcwd() + "/"
app = Flask(__name__, root_path=root_folder, static_url_path=root_folder)
running_threads = dict()  # type: dict

@app.route("/")
def index():
    res = Response()
    res.data = "Welcome to Billz-OCR-Server!"
    res.headers.set('Access-Control-Allow-Origin', '*')
    return res


@app.route("/<pending_id>")
def check_status(pending_id):
    print("{} status: {}".format(pending_id, pending_queue[pending_id]))
    print("tid #{} alive: {}".format(pending_id, running_threads[pending_id].is_alive()))
    res = Response()
    res.data = ""
    res.headers.set('Access-Control-Allow-Origin', '*')
    if pending_id in pending_queue.keys():
        res.data = pending_queue[pending_id]
        if res.data == "" and not running_threads[pending_id].is_alive():
            res = json.dumps({"status": "fail"})
            pending_queue.pop(pending_id)
            running_threads.pop(pending_id)
        elif res.data != "":
            pending_queue.pop(pending_id)
            running_threads.pop(pending_id)
    else:
        res = json.dumps({"status": "fail"})
    return res


@app.route("/uploadFile", methods=['POST'])
def upload_file():
    file = request.files["billFile"]
    bill_type = request.form.get("bill_type")
    # form = request.form.get("cycle_billing"), request.form.get("bill_type")
    file_name = "{}/{}".format(os.getcwd(), file.filename)
    print("Save file: {}".format(file_name))
    file.save(file_name)
    #request_id = generate_random_ids()
    print("Processing file {}".format(file_name))
    proc_id = start_process_file_thread(file_name)
    #result = process_file(file_name)
    #print("Processing file {} done, send back response".format(file_name))
    print("send back response..")
    res = Response()
    res.data = json.dumps({"pendingId": proc_id})
    res.headers.set('Access-Control-Allow-Origin', '*')
    return res


def start_process_file_thread(file_name):
    global running_threads
    proc_thread = Thread(target=process_file, args=[file_name])
    proc_thread.start()
    running_threads.__setitem__(proc_thread.ident, proc_thread)
    return proc_thread.ident

def generate_random_ids():
    rand_num = "%06d" % random.randint(0, 1000000)
    while rand_num in pending_queue.keys():
        rand_num = "%06d" % random.randint(0, 1000000)
    return rand_num


if __name__ == '__main__':
    port = os.environ.get("PORT") or 5000
    app.run(host='0.0.0.0', port=port)
