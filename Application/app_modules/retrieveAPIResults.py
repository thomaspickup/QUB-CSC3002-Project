from Tkinter import *
from shutil import copyfile
import os, sys

def retrieve(printer):
    # The directory that the exports from the cuckoo environment are stored
    raw_directory = ''
    report_directory = ''

    if len(sys.argv) == 3:
        raw_directory = sys.argv[1]
        report_directory = sys.argv[2]
    else:
        raw_directory = r"m:\\"
        report_directory = r"r:\\"

    printer.insert(END, "- Starting Copying of Reports\n")
    count = 0

    exclude = ["$RECYCLE.BIN", "System Volume Information"]
    for name in os.listdir(raw_directory):
        if name not in exclude:
            results_file = raw_directory + "/" + name + "\\reports\\report.json"
            new_file = report_directory + "\\" + name + ".json"
            if os.path.isfile(new_file) == False:
                print(new_file)
                copyfile(results_file, new_file)
                count = count + 1
    printer.insert(END, "- Finished Copying " + str(count) + " report(s).\n")
    printer.insert(END, "~~ API Results Retrieval: Complete ~~\n")
