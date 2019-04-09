from Tkinter import *
import compileSamplelist, compileAPIResults, retrieveAPIResults
import os

def parser(printer, statusbar, retrieve, sample, dataset):
    statusbar.config(text = "Running Command: Parser DataSet")
    
    if retrieve == 1:
        printer.insert(END, "~~ API Results Retrieval: Started ~~\n")
        retrieveAPIResults.retrieve(printer)
    if sample == 1:
        printer.insert(END, "~~ Sample List Production: Started ~~\n")
        compileSamplelist.compile(printer)
    if dataset == 1:
        printer.insert(END, "~~ API Results Production: Started ~~\n")
        compileAPIResults.compile(printer)

    statusbar.config(text = "Waiting for Command...")
