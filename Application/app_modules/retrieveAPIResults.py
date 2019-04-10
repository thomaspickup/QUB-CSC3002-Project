from Tkinter import *
from shutil import copyfile
import configuration
import os, sys

def retrieve(printer):
    # The directory that the exports from the cuckoo environment are stored
    raw_directory = configuration.CUCKOO_EXPORT_DIRECTORY
    report_directory = configuration.REPORTS_DIRECTORY
    isRawDirectory = os.path.isdir(raw_directory)
    isReportDirectory = os.path.isdir(report_directory)

    if isRawDirectory and isReportDirectory:
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
    else:
        printer.insert(END, "** ERROR: Reports or Cuckoo Export Directory are Invalid, please check preferences **\n")
        
    printer.insert(END, "~~ API Results Retrieval: Complete ~~\n")
