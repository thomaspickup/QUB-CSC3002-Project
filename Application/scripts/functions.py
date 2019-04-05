from Tkinter import *
import subprocess

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
