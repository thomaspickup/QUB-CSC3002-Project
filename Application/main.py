from Tkinter import *
from tkinter import ttk
from app_modules import processSample, parserDataset
from scripts import functions
import tkFileDialog, tkMessageBox, os, inspect, requests, time, csv, subprocess, thread

class Application(Frame):
    # UnKnown Sample Related Functions
    def btnGetSamplePressed(self):
        fileName = tkFileDialog.askopenfilename(initialdir = "C:\\", title = "Select Sample File", filetypes  = (("Binary Files", "*"), ("Executable Files", "*.exe"), ("DLL Files", "*.dll")))
        self.txtFilePath.delete(0, END)
        self.txtFilePath.insert(0, fileName)

    def btnSubmitSamplePressed(self):
        # Gets the FileName
        fileName = self.txtFilePath.get()
        self.txtFilePath.config(state = "disabled")
        self.btnSubmitSample.config(state = "disabled")
        self.btnGetSample.config(state = "disabled")

        # TODO: Check Cuckoo is running
        # TODO: Check for an actual file
        R_Location = os.path.isfile(r'C:\Program Files\R\R-3.5.3\bin\RScript.exe')

        if R_Location:
            thread.start_new_thread(processSample.analyze,(fileName, self.commandWindowDisplay, ))

        self.txtFilePath.delete(0, END)
        self.txtFilePath.config(state = "normal")
        self.btnSubmitSample.config(state = "normal")
        self.btnGetSample.config(state = "normal")

    # Model Stats

    # New Model
    def btnNewModelPressed(self):
        thread.start_new_thread(self.newModel, (self.commandWindowDisplay, ))

    def newModel(self, printer):
        command = ["rscript", r"C:\Users\thomaspickup\iCloudDrive\Documents\University\CSC3002\Assignment\CSC3002-Project\Application\mlcore\Model_Creation_Script.R"]
        functions.runScript(command, printer)

    # DataSet Stats
    
    # New DataSet
    def btnNewDatasetPressed(self):
        thread.start_new_thread(parserDataset.parser, (self.commandWindowDisplay, ))

    # General Purpose Functions
    def dependancyCheckAndInstallR(self):
        R_Location = os.path.isfile(r'C:\Program Files\R\R-3.5.3\bin\RScript.exe')

        if R_Location:
            tkMessageBox.showinfo("R Dependancy Check", "R Is Already Installed, please check the permissions on the application install folder in Program Files.")
        else:
            tkMessageBox.showwarning("R Dependancy Check", "R Is Not Installed, will now attempt to install.")
            location = os.getcwd() + r"\Application\dependencies\R-3.5.3-win.exe"
            print(location)
            os.system(location)
            subprocess.call(['runas', '/user:Administrator', r'setx /M PATH "%PATH%;C:\Program Files\R\R-3.5.3\bin\"'])

    # Creates the UI
    def createWidgets(self):
        # Sets up the SideBar
        self.sideBar = Frame(self, width=150)
        self.sideBarUpper = Frame(self.sideBar, width=150)
        self.sideBarLower = Frame(self.sideBar, width=150)
        self.sideBarUpper.pack(side="top", fill="both", expand=True)
        self.sideBarLower.pack(side="top", fill="both", expand=True)

        # Sets up the Upload Pane
        self.uploadPane = LabelFrame(self.sideBarUpper, text = "Sample Upload:", padx = 5, pady = 5)
        self.uploadPane.pack(padx = 10, pady = 10, fill = "both")
        self.txtFilePath = Entry(self.uploadPane)
        self.btnGetSample = Button(self.uploadPane, text = "Open File", command = self.btnGetSamplePressed)
        self.btnSubmitSample = Button(self.uploadPane, text = "Submit", command = self.btnSubmitSamplePressed)
        self.txtFilePath.grid(row = 1, column = 0, columnspan = 4, sticky = "ew", padx = 5 , pady = 5)
        self.btnGetSample.grid(row = 2, column = 0, columnspan = 2, sticky = "w", padx = 5, pady = 5)
        self.btnSubmitSample.grid(row = 2, column = 2, columnspan = 2, sticky = "e", padx = 5, pady = 5)

        # Sets up the Dataset Model uploadPane
        self.dsmodelPane = LabelFrame(self.sideBarUpper, text = "DataSet / Model", padx = 5, pady = 5)
        self.dsmodelPane.pack(padx = 10, pady = 10, fill = "both")
        self.btnNewDataset = Button(self.dsmodelPane, text = "New DataSet", command = self.btnNewDatasetPressed)
        self.btnNewModel = Button(self.dsmodelPane, text = "New Model", command = self.btnNewModelPressed)
        self.btnNewDataset.grid(row = 0, column = 0, columnspan = 2, sticky = "w", padx = 5, pady = 5)
        self.btnNewModel.grid(row = 0, column = 2, columnspan = 2, sticky = "e", padx = 5, pady = 5)
        self.btnDatasetStats = Button(self.dsmodelPane, text = "DataSet Stats", command = self.btnSubmitSamplePressed)
        self.btnModelStats = Button(self.dsmodelPane, text = "Model Stats", command = self.btnSubmitSamplePressed)
        self.btnDatasetStats.grid(row = 1, column = 0, columnspan = 2, sticky = "w", padx = 5, pady = 5)
        self.btnModelStats.grid(row = 1, column = 2, columnspan = 2, sticky = "e", padx = 5, pady = 5)

        # Sets up the Title Bar
        self.titleFrame = Frame(self)
        self.lblTitle = Label(self.titleFrame, text = "Malware Categorisation Using Machine Learning")
        titleFont = ("times", 16, "bold")
        self.lblTitle.config(font = titleFont)
        self.lblTitle.pack()

        # Set up the Main Content
        self.mainContent = Frame(self)
        self.mainContent.grid(row=1, column=1)
        self.commandWindowDisplay = Text(self.mainContent)
        self.commandWindowDisplay.grid(row = 4, column = 0, columnspan = 5, rowspan = 3, sticky = "nesw")

        # status bar
        self.statusFrame = Frame(self)
        self.status = Label(self.statusFrame, text="Waiting...")
        self.status.pack(fill="both", expand=True)

        # Define Grid for different sections
        self.sideBar.grid(row=0, column=0, rowspan=2, sticky="nesw")
        self.titleFrame.grid(row=0, column=1, sticky="ew")
        self.mainContent.grid(row=1, column=1, sticky="nesw")
        self.statusFrame.grid(row=2, column=0, columnspan=2, sticky="ew")

        # Sets up Menu Bar
        self.menuBar = Menu(self)

        self.fileMenu = Menu(self.menuBar, tearoff = 0)
        self.fileMenu.add_command(label = "Create New Dataset", command = self.quit)
        self.fileMenu.add_command(label = "Create New Model", command = self.quit)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label = "Preferences", command = self.quit)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label = "Quit", command = self.quit)
        self.menuBar.add_cascade(label = "File", menu = self.fileMenu)

        self.dependancyMenu = Menu(self.menuBar, tearoff = 0)
        self.dependancyMenu.add_command(label = "R 3.5.3", command = self.dependancyCheckAndInstallR)
        self.menuBar.add_cascade(label = "Dependancies", menu = self.dependancyMenu)

    def __init__(self, master = None):
        # TODO: Check if Cuckoo is running

        # Next start setting up the UI
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
app = Application(master = root)
root.config(menu = app.menuBar)
root.title("Malware Categorisation")
root.resizable(width = False, height = False)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(1, weight=1)
app.mainloop()
root.destroy()
