from Tkinter import *
from tkinter import ttk

class Preferences():
    def verifyLocations(self):
        print("verify")

    def createWidgets(self):
        self.titleFrame = Frame(self.preferencesWindow)
        self.titleFrame.grid(row=0, column=0, sticky="new", pady = 5, padx = 5)
        self.lblTitle = Label(self.titleFrame, text = "Preferences")
        titleFont = ("times", 16, "bold")
        self.lblTitle.config(font = titleFont)
        self.lblTitle.pack()

        self.mainContent = Frame(self.preferencesWindow)
        self.mainContent.grid(row=1, column=0, sticky = "nesw", pady = (0, 5), padx = 5)
        self.locationsGroup = LabelFrame(self.mainContent, text = "Locations")
        self.locationsGroup.grid(row = 0, column = 0, sticky = "nesw", pady = (0, 5), padx = 5)

        self.lblCuckoo = Label(self.locationsGroup, text = "Cuckoo Server", anchor = "w")
        self.lblCuckoo.grid(row = 0, column = 0, columnspan = 1, sticky = "nesw", pady = 5, padx = 5)
        self.txtCuckoo = Entry(self.locationsGroup)
        self.txtCuckoo.grid(row = 0, column = 1, columnspan = 5, sticky = "nesw", pady = (0, 5), padx = 5)
        self.btnCuckooOpenFolder = Button(self.locationsGroup, text = "Connect")
        self.btnCuckooOpenFolder.grid(row = 0, column = 6, columnspan = 1, sticky = "nesw", pady = (0, 5), padx = 5)

        self.lblSampleDirectory = Label(self.locationsGroup, text = "Sample Directory", anchor = "w")
        self.lblSampleDirectory.grid(row = 1, column = 0, columnspan = 1, sticky = "nesw", pady = 5, padx = 5)
        self.txtSampleDirectory = Entry(self.locationsGroup)
        self.txtSampleDirectory.grid(row = 1, column = 1, columnspan = 5, sticky = "nesw", pady = (0, 5), padx = 5)
        self.btnSampleDirectoryOpenFolder = Button(self.locationsGroup, text = "Open")
        self.btnSampleDirectoryOpenFolder.grid(row = 1, column = 6, columnspan = 1, sticky = "nesw", pady = (0, 5), padx = 5)

        self.lblDataSetDirectory = Label(self.locationsGroup, text = "DataSet Directory", anchor = "w")
        self.lblDataSetDirectory.grid(row = 2, column = 0, columnspan = 1, sticky = "nesw", pady = 5, padx = 5)
        self.txtDataSetDirectory = Entry(self.locationsGroup)
        self.txtDataSetDirectory.grid(row = 2, column = 1, columnspan = 5, sticky = "nesw", pady = (0, 5), padx = 5)
        self.btnDataSetDirectoryOpenFolder = Button(self.locationsGroup, text = "Open")
        self.btnDataSetDirectoryOpenFolder.grid(row = 2, column = 6, columnspan = 1, sticky = "nesw", pady = (0, 5), padx = 5)

        self.lblModelDirectory = Label(self.locationsGroup, text = "Model Directory", anchor = "w")
        self.lblModelDirectory.grid(row = 3, column = 0, columnspan = 1, sticky = "nesw", pady = 5, padx = 5)
        self.txtModelDirectory = Entry(self.locationsGroup)
        self.txtModelDirectory.grid(row = 3, column = 1, columnspan = 5, sticky = "nesw", pady = (0, 5), padx = 5)
        self.btnModelDirectoryOpenFolder = Button(self.locationsGroup, text = "Open")
        self.btnModelDirectoryOpenFolder.grid(row = 3, column = 6, columnspan = 1, sticky = "nesw", pady = (0, 5), padx = 5)

        self.lblCuckooExportDirectory = Label(self.locationsGroup, text = "Cuckoo Exports", anchor = "w")
        self.lblCuckooExportDirectory.grid(row = 4, column = 0, columnspan = 1, sticky = "nesw", pady = 5, padx = 5)
        self.txtCuckooExportDirectory = Entry(self.locationsGroup)
        self.txtCuckooExportDirectory.grid(row = 4, column = 1, columnspan = 5, sticky = "nesw", pady = (0, 5), padx = 5)
        self.btnCuckooExportDirectoryOpenFolder = Button(self.locationsGroup, text = "Open")
        self.btnCuckooExportDirectoryOpenFolder.grid(row = 4, column = 6, columnspan = 1, sticky = "nesw", pady = (0, 5), padx = 5)

        self.lblReportsDirectory = Label(self.locationsGroup, text = "Reports Directory", anchor = "w")
        self.lblReportsDirectory.grid(row = 5, column = 0, columnspan = 1, sticky = "nesw", pady = 5, padx = 5)
        self.txtReportsDirectory = Entry(self.locationsGroup)
        self.txtReportsDirectory.grid(row = 5, column = 1, columnspan = 5, sticky = "nesw", pady = (0, 5), padx = 5)
        self.btnReportsOpenFolder = Button(self.locationsGroup, text = "Open")
        self.btnReportsOpenFolder.grid(row = 5, column = 6, columnspan = 1, sticky = "nesw", pady = (0, 5), padx = 5)

        self.btnVerify = Button(self.locationsGroup, text = "Save", command = self.verifyLocations)
        self.btnVerify.grid(row = 10, column = 6, sticky = "nesw", columnspan = 1, pady = (0, 5), padx = 5)

    def __init__(self, master = None):
        self.preferencesWindow = Toplevel(master)
        self.createWidgets()
        self.preferencesWindow.title("Preferences")
        self.preferencesWindow.resizable(width = False, height = False)
        self.preferencesWindow.grid_rowconfigure(1, weight=1)
        self.preferencesWindow.grid_columnconfigure(1, weight=1)
