from Tkinter import *
from tkinter import ttk
from app_modules import processSample, parserDataset, cuckooSearch, configuration
from scripts import functions
from windows import Preferences, modelTable, newDataset
from socket import gethostbyname, gaierror
import tkFileDialog, tkMessageBox, os, inspect, requests, time, csv, subprocess, thread

class Application(Frame):
    # Open Sample Pressed
    def btnGetSamplePressed(self):
        fileName = tkFileDialog.askopenfilename(initialdir = "C:\\", title = "Select Sample File", filetypes  = (("Binary Files", "*"), ("Executable Files", "*.exe"), ("DLL Files", "*.dll")))
        self.txtFilePath.delete(0, END)
        self.txtFilePath.insert(0, fileName)

    # Submit sample pressed
    def btnSubmitSamplePressed(self):
        self.commandWindowDisplay.insert(END, "== Process Sample ==\n")

        # Gets the FileName
        fileName = self.txtFilePath.get()
        if fileName != "":
            self.txtFilePath.config(state = "disabled")
            self.btnSubmitSample.config(state = "disabled")
            self.btnGetSample.config(state = "disabled")

            rLocation = os.path.isfile(configuration.R_LOCATION + r'\RScript.exe')
            fileExists = os.path.isfile(fileName)
            if not rLocation:
                self.installR()

            if fileExists:
                if self.checkCuckooStatus():
                    thread.start_new_thread(processSample.analyze,(fileName, self.commandWindowDisplay, self.status))
                else:
                    self.commandWindowDisplay.insert(END, "**Cuckoo Not Running, please check settings and try again**\n")
            else:
                self.commandWindowDisplay.insert(END, "**File Does Not Exist**\n")

            self.txtFilePath.delete(0, END)
            self.txtFilePath.config(state = "normal")
            self.btnSubmitSample.config(state = "normal")
            self.btnGetSample.config(state = "normal")

        else:
            self.commandWindowDisplay.insert(END, "**Please enter a file or use Open File to select one**\n")

    # Search Pressed
    def btnSearchSamplePressed(self):
        md5Hash = self.txtMD5Search.get()
        if md5Hash != "":
            if self.checkCuckooStatus():
                thread.start_new_thread(cuckooSearch.search, (md5Hash, self.commandWindowDisplay, self.status, ))
            else:
                self.commandWindowDisplay.insert(END, "**Cuckoo Not Running, please check settings and try again**\n")
        else:
            self.commandWindowDisplay.insert(END, "**Please Enter A Search Term**\n")

    # Model Stats
    def btnModelStatsPressed(self):
        modelTable.modelTable(self)

    # New Model
    def btnNewModelPressed(self):
        thread.start_new_thread(self.newModel, (self.commandWindowDisplay, ))

    # New Model Function
    def newModel(self, printer):
        self.commandWindowDisplay.insert(END, "== New Model ==\n")
        self.status.config(text = "Running Command: New Model")
        command = ["rscript", os.getcwd() + r"\mlcore\Model_Creation_Script.R", configuration.DATASET_DIRECTORY, configuration.MODEL_DIRECTORY, configuration.RUN_BORUTA, configuration.RUN_CROSSVALIDATION, configuration.NUMBER_OF_FOLDS]
        functions.runScript(command, printer)
        self.status.config(text = "Waiting for Command...")

    # DataSet Stats
    def btnDatasetStatsPressed(self):
        print("DataSet Stats Pressed")

    # New DataSet
    def btnNewDatasetPressed(self):
        self.sampleChecked = 0
        self.datasetChecked = 0
        self.retrieveChecked = 0

        datasetScreen = newDataset.newDataset(self)

    def newDataset(self):
        self.commandWindowDisplay.insert(END, "== New Dataset ==\n")
        if self.checkCuckooStatus():
            thread.start_new_thread(parserDataset.parser, (self.commandWindowDisplay, self.status, self.retrieveChecked, self.sampleChecked, self.datasetChecked ))
        else:
            self.commandWindowDisplay.insert(END, "**Cuckoo Not Running, please check settings and try again**\n")

    # Clear Console
    def btnClearConsolePressed(self):
        answer = tkMessageBox.askyesno("Clear Console","Are you sure you want to clear the console?")

        if answer:
            self.commandWindowDisplay.delete("1.0", END)

    # Cancel Task
    def btnCancelTaskPressed(self):
        answer = tkMessageBox.askyesno("Cancel Task","Are you sure you want to cancel the current task?")

        if answer:
            print("Cancel Task Pressed")

    # Show Preferences Pane
    def showPreferences(self):
        Preferences.Preferences(self)

    # Install R
    def installR(self):
        tkMessageBox.showwarning("R Dependancy Check", "R Is Not Installed, will now attempt to install.")
        location = os.getcwd() + r"\dependencies\R-3.5.3-win.exe"
        os.system(location)
        subprocess.call([r'setx /M PATH "%PATH%;C:\Program Files\R\R-3.5.3\bin\"'])

    # Checks cuckoo status
    def checkCuckooStatus(self):
        isCuckooOnline = functions.checkCuckooOnline(configuration.CUCKOO_SERVER, configuration.CUCKOO_SERVER_PORT)

        return isCuckooOnline

    # Attempts to launch cuckoo
    def attemptToLaunchCuckoo(self):
        subprocess.call(["python", os.getcwd() + r"\scripts\cuckoo_run.pyw"])

    # Dependancy check for r
    def dependancyCheckAndInstallR(self):
        R_Location = os.path.isfile(configuration.R_LOCATION + r'\RScript.exe')

        if R_Location:
            tkMessageBox.showinfo("R Dependancy Check", "R Is Already Installed, please check the permissions on the application install folder in Program Files.")
        else:
            self.installR()

    # Dependancy check for cuckoo
    def dependancyCheckAndLaunchCuckoo(self):
        cuckooOnline = self.checkCuckooStatus()

        # Now loaded display error message if cuckoo not online
        if not cuckooOnline:
            try:
                if gethostbyname(configuration.CUCKOO_SERVER) == "127.0.0.1":
                    answer = tkMessageBox.askyesno("Cuckoo Offline", "The configured Cuckoo Server didn't respond, as the server appears to be on this machine, do you want us to try and launch it?")

                    if answer:
                        # Try to launch using scripts cuckoo_run.pyw
                        self.attemptToLaunchCuckoo()
                else:
                    tkMessageBox.showinfo("Cuckoo Offline", "The configured Cuckoo Server didn't respond, please check it is online and preferences.")
            except gaierror:
                tkMessageBox.showinfo("Cuckoo Offline", "The configured Cuckoo Server could not be resolved and didn't respond, please check it is online and preferences.")

    # Creates the UI
    def createWidgets(self):
        # Sets up the SideBar
        self.sideBar = Frame(self, width=150)
        self.lblSideBarTitle = Label(self.sideBar, text = "Actions")
        titleFont = ("times", 16, "bold")
        self.lblSideBarTitle.config(font = titleFont)
        self.lblSideBarTitle.pack()

        # Sets up the Upload Pane
        self.uploadPane = LabelFrame(self.sideBar, text = "Sample Upload:", padx = 5, pady = 5)
        self.uploadPane.pack(padx = 10, pady = 10, fill = "both")
        self.txtFilePath = Entry(self.uploadPane)
        self.btnGetSample = Button(self.uploadPane, text = "Open File", command = self.btnGetSamplePressed)
        self.btnSubmitSample = Button(self.uploadPane, text = "Submit", command = self.btnSubmitSamplePressed)
        self.txtFilePath.grid(row = 1, column = 0, columnspan = 4, sticky = "nesw", padx = 5 , pady = 5)
        self.btnGetSample.grid(row = 1, column = 4, columnspan = 2, sticky = "nesw", padx = 5, pady = 5)
        self.btnSubmitSample.grid(row = 2, column = 0, columnspan = 6, sticky = "nesw", padx = 5, pady = 5)

        self.searchPane = LabelFrame(self.sideBar, text = "Cuckoo Search:", padx = 5, pady = 5)
        self.searchPane.pack(padx = 10, pady = 10, fill = "both")
        self.txtMD5Search = Entry(self.searchPane)
        self.btnSearchSample = Button(self.searchPane, text = "Search", command = self.btnSearchSamplePressed)
        self.txtMD5Search.grid(row = 1, column = 0, columnspan = 4, sticky = "nesw", padx = 5 , pady = 5)
        self.btnSearchSample.grid(row = 1, column = 4, columnspan = 2, sticky = "nesw", padx = 5, pady = 5)

        # Sets up the Dataset Model uploadPane
        self.dsmodelPane = LabelFrame(self.sideBar, text = "DataSet / Model", padx = 5, pady = 5)
        self.dsmodelPane.pack(padx = 10, pady = 10, fill = "both")
        self.btnNewDataset = Button(self.dsmodelPane, text = "New DataSet", command = self.btnNewDatasetPressed)
        self.btnNewModel = Button(self.dsmodelPane, text = "New Model", command = self.btnNewModelPressed)
        self.btnNewDataset.grid(row = 0, column = 0, columnspan = 3, sticky = "nesw", padx = 5, pady = 5)
        self.btnNewModel.grid(row = 0, column = 3, columnspan = 3, sticky = "nesw", padx = 5, pady = 5)
        self.btnDatasetStats = Button(self.dsmodelPane, text = "DataSet Stats", command = self.btnDatasetStatsPressed)
        self.btnModelStats = Button(self.dsmodelPane, text = "Model Stats", command = self.btnModelStatsPressed)
        self.btnDatasetStats.grid(row = 1, column = 0, columnspan = 3, sticky = "nesw", padx = 5, pady = 5)
        self.btnModelStats.grid(row = 1, column = 3, columnspan = 3, sticky = "nesw", padx = 5, pady = 5)

        self.utilitiesPane = LabelFrame(self.sideBar, text = "Utilities", padx = 5, pady = 5)
        self.utilitiesPane.pack(padx = 10, pady = 10, fill = "both")
        self.btnClearConsole = Button(self.utilitiesPane, text = "Clear Console", command = self.btnClearConsolePressed)
        self.btnCancelTask = Button(self.utilitiesPane, text = "Cancel Task", command = self.btnCancelTaskPressed)
        self.btnClearConsole.grid(row = 0, column = 0, columnspan = 3, sticky = "nesw", padx = 5, pady = 5)
        self.btnCancelTask.grid(row = 0, column = 3, columnspan = 3, sticky = "nesw", padx = 5, pady = 5)

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
        self.commandWindowDisplay.grid(row = 0, column = 0, sticky = "nesw")

        self.scrollbar = Scrollbar(self.mainContent, command = self.commandWindowDisplay.yview)
        self.scrollbar.grid(row = 0, column = 1, sticky = "nesw", padx = (0, 5))
        self.commandWindowDisplay['yscrollcommand'] = self.scrollbar.set

        # status bar
        self.statusFrame = Frame(self)
        self.status = Label(self.statusFrame, text="Waiting for Command...")
        self.status.pack(fill="both", expand=True)

        # Define Grid for different sections
        self.sideBar.grid(row=0, column=0, rowspan=2, sticky="nesw")
        self.titleFrame.grid(row=0, column=1, sticky="ew")
        self.mainContent.grid(row=1, column=1, sticky="nesw")
        self.statusFrame.grid(row=2, column=0, columnspan=2, sticky="ew")

        # Sets up Menu Bar
        self.menuBar = Menu(self)

        self.fileMenu = Menu(self.menuBar, tearoff = 0)
        self.fileMenu.add_command(label = "New Dataset", command = self.btnNewDatasetPressed)
        self.fileMenu.add_command(label = "New Model", command = self.btnNewModelPressed)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label = "Preferences", command = self.showPreferences)
        self.dependancyMenu = Menu(self.menuBar, tearoff = 0)
        self.dependancyMenu.add_command(label = "R 3.5.3", command = self.dependancyCheckAndInstallR)
        try:
            if gethostbyname(configuration.CUCKOO_SERVER) == "127.0.0.1":
                self.dependancyMenu.add_command(label = "Reload Cuckoo", command = self.dependancyCheckAndLaunchCuckoo)
        except gaierror:
            # No further processing needed as the hostname could not be resolved so we know its not local
            pass
        self.fileMenu.add_cascade(label = "Dependencies", menu = self.dependancyMenu)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label = "Quit", command = self.quit)
        self.menuBar.add_cascade(label = "File", menu = self.fileMenu)

        self.viewMenu = Menu(self.menuBar, tearoff = 0)
        self.viewMenu.add_command(label = "Model Statistics", command = self.btnModelStatsPressed)
        self.viewMenu.add_command(label = "Dataset Statistics", command = self.btnDatasetStatsPressed)
        self.menuBar.add_cascade(label = "View", menu = self.viewMenu)

    def __init__(self, master = None):
        # Next start setting up the UI
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

        # Check if cukoo is installed
        self.dependancyCheckAndLaunchCuckoo()

root = Tk()
app = Application(master = root)
root.config(menu = app.menuBar)
root.title("Malware Categorisation")
root.resizable(width = False, height = False)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(1, weight=1)
app.mainloop()
root.destroy()
