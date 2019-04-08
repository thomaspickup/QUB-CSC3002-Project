from Tkinter import *
import subprocess, requests

# This functions purpose is to run a script using the subprocess command and return the output of the script to a printer (Tkinter output)
def runScript(command, printer):
    # Defines the process
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # This will write to the printer any output that is given.
    while True:
        # Gets the next line of the output
        nextline = process.stdout.readline()

        # Checks the next line isn't null
        if nextline == '' and process.poll() is not None:
            break

        # Prints out to the printer
        printer.insert(END, nextline)
        sys.stdout.flush()

    # If there is an error it will be raised
    output = process.communicate()[0]
    exitCode = process.returncode
    if (exitCode != 0):
        raise ProcessException(command, exitCode, output)

def printTextFile(fileLocation, printer):
    with open(fileLocation, 'r') as file:
        data = file.read()

    printer.insert(END, data)

def checkCuckooOnline(cuckoo_host, cuckoo_port):
    server_url = cuckoo_host
    server_port = cuckoo_port
    server =  r"http://" + server_url + r":" + server_port + r"/"

    cuckooOnline = True

    try:
        response = requests.get(server + "cuckoo/status");
        if response.status_code != requests.codes.ok:
            cuckooOnline = False
    except requests.exceptions.RequestException as e:
        cuckooOnline = False

    return cuckooOnline
