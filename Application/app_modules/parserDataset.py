from Tkinter import *
import compileSamplelist, compileAPIResults, retrieveAPIResults
import os

def parser(printer, statusbar):
    statusbar.config(text = "Running Command: Parser DataSet")
    printer.insert(END, "~~ API Results Retrieval: Started ~~\n")
    retrieveAPIResults.retrieve(printer)
    printer.insert(END, "~~ Sample List Production: Started ~~\n")
    compileSamplelist.compile(printer)
    printer.insert(END, "~~ API Results Production: Started ~~\n")
    compileAPIResults.compile(printer)
    statusbar.config(text = "Waiting for Command...")
