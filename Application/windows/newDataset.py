from Tkinter import *
from tkinter import ttk
from app_modules import configuration, parserDataset
from scripts import functions
import ConfigParser, csv, decimal, os, tkMessageBox, thread

class newDataset():
    def passBack(self):
        self.master.sampleChecked = self.sampleChecked.get()
        self.master.datasetChecked = self.datasetChecked.get()
        self.master.retrieveChecked = self.retrieveChecked.get()

        self.master.newDataset()

        self.newDataset.destroy()

    def createWidgets(self):
        # Creates the title
        self.titleFrame = Frame(self.newDataset)
        self.titleFrame.grid(row=0, column=0, sticky="new", pady = 5, padx = 5)
        self.lblTitle = Label(self.titleFrame, text = "New Dataset")
        titleFont = ("times", 16, "bold")
        self.lblTitle.config(font = titleFont)
        self.lblTitle.pack()

        # Creates the main content frame
        self.mainContent = Frame(self.newDataset)
        self.mainContent.grid(row=1, column=0, sticky = "nesw", pady = (0, 5), padx = 5)

        self.mainFrame = LabelFrame(self.mainContent, text = " Run Options")
        self.mainFrame.grid(row = 0, column = 0, sticky = "nesw", pady = 5, padx = 5)

        self.retrieveChecked = IntVar()
        self.retrieveCheckBox = Checkbutton(self.mainFrame, text="Retrieve Reports From Cuckoo Export Directory", variable=self.retrieveChecked)
        self.retrieveCheckBox.grid(row = 0, column = 0, sticky = "nesw", pady = 5, padx = 5)
        self.sampleChecked = IntVar()
        self.sampleCheckBox = Checkbutton(self.mainFrame, text="Produce New Sample List From Sample Directory", variable=self.sampleChecked)
        self.sampleCheckBox.grid(row = 1, column = 0, sticky = "nesw", pady = 5, padx = 5)
        self.datasetChecked = IntVar()
        self.datasetCheckBox = Checkbutton(self.mainFrame, text="Produce API Call Dataset From Reports Directory", variable=self.datasetChecked)
        self.datasetCheckBox.grid(row = 2, column = 0, sticky = "nesw", pady = 5, padx = 5)

        self.runParserDataset = Button(self.mainContent, text = "Run New Dataset", command = self.passBack)
        self.runParserDataset.grid(row = 3, column = 0, sticky = "nesw", pady = 5, padx = 5)

    def __init__(self, master = None):
        self.master = master
        self.newDataset = Toplevel(master)
        self.createWidgets()
        self.newDataset.title("New Dataset")
        self.newDataset.resizable(width = False, height = False)
        self.newDataset.grid_rowconfigure(1, weight=1)
        self.newDataset.grid_columnconfigure(1, weight=1)
        self.newDataset.transient(master)
