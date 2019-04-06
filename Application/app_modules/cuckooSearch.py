from Tkinter import *
from scripts import functions
import os, time, requests, csv, subprocess, hashlib

def search(input, printer, statusbar):
    statusbar.config(text = "Running Command: Cuckoo Search")
    server_url = "http://localhost:8090/"
    request_headers = {"Authorization": "Bearer S4MPL3"}
    error = False

    isInputDigit = input.isdigit()

    printer.insert(END, "== Cuckoo Search ==\n")

    if isInputDigit:
        printer.insert(END, "- Searching For Sample with Task ID: " + input + "\n\n")
    else:
        printer.insert(END, "- Searching For Sample with MD5Hash: " + input + "\n\n")

    printer.insert(END, "== Results ==\n")

    if isInputDigit:
        this_request = server_url + r"tasks/view/" + input
        md5Check = requests.get(this_request)

        if "task" in md5Check.json():
            if "sample" in md5Check.json()['task']:
                if "md5" in md5Check.json()['task']['sample']:
                    md5Hash = md5Check.json()['task']['sample']['md5']

                    printer.insert(END, "MD5 Hash: " + md5Hash + "\n")
                else:
                    error = True
            else:
                error = True
        else:
            error = True
    else:
        this_request = server_url + r"files/view/md5/" + input
        idCheck = requests.get(this_request)

        if "sample" in idCheck.json():
            id = idCheck.json()['sample']['id']

            printer.insert(END, "Task ID: " + str(id) + "\n")
        else:
            error = True

    if not error:
        print("Continue on with report run")

    if error:
        printer.insert(END, "**Sample Not Found**\n")
    statusbar.config(text = "Waiting for Command...")
