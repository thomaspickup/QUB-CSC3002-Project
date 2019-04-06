from Tkinter import *
from tkinter import ttk
from app_modules import processSample, parserDataset, cuckooSearch
from scripts import functions
from windows import Preferences
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
        if fileName != "":
            self.txtFilePath.config(state = "disabled")
            self.btnSubmitSample.config(state = "disabled")
            self.btnGetSample.config(state = "disabled")

            rLocation = os.path.isfile(r'C:\Program Files\R\R-3.5.3\bin\RScript.exe')
            fileExists = os.path.isfile(fileName)
            if not rLocation:
                self.installR()

            if fileExists:
                thread.start_new_thread(processSample.analyze,(fileName, self.commandWindowDisplay, self.status))
            else:
                self.commandWindowDisplay.insert(END, "**File Does Not Exist**\n")

            self.txtFilePath.delete(0, END)
            self.txtFilePath.config(state = "normal")
            self.btnSubmitSample.config(state = "normal")
            self.btnGetSample.config(state = "normal")

        else:
            self.commandWindowDisplay.insert(END, "**Please enter a file or use Open File to select one**\n")

    def btnSearchSamplePressed(self):
        md5Hash = self.txtMD5Search.get()
        if md5Hash != "":
            thread.start_new_thread(cuckooSearch.search, (md5Hash, self.commandWindowDisplay, self.status, ))
        else:
            self.commandWindowDisplay.insert(END, "**Please Enter A Search Term**\n")

    # Model Stats
    def btnModelStatsPressed(self):
        fileExists = os.path.isfile(r"model\accuracies.txt")
        if fileExists:
            functions.printTextFile(r"model\accuracies.txt", self.commandWindowDisplay)
        else:
            self.commandWindowDisplay.insert(END, "**Model Stats Doesn't Exist**\n")

    # New Model
    def btnNewModelPressed(self):
        thread.start_new_thread(self.newModel, (self.commandWindowDisplay, ))

    def newModel(self, printer):
        command = ["rscript", r"C:\Users\thomaspickup\iCloudDrive\Documents\University\CSC3002\Assignment\CSC3002-Project\Application\mlcore\Model_Creation_Script.R"]
        functions.runScript(command, printer)

    # DataSet Stats
    def btnDatasetStatsPressed(self):
        print("DataSet Stats Pressed")

    # New DataSet
    def btnNewDatasetPressed(self):
        thread.start_new_thread(parserDataset.parser, (self.commandWindowDisplay, self.status, ))

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

    def showPreferences(self):
        Preferences.Preferences(self)

    # General Purpose Functions
    def installR(self):
        tkMessageBox.showwarning("R Dependancy Check", "R Is Not Installed, will now attempt to install.")
        location = os.getcwd() + r"\dependencies\R-3.5.3-win.exe"
        os.system(location)
        subprocess.call([r'setx /M PATH "%PATH%;C:\Program Files\R\R-3.5.3\bin\"'])

    def dependancyCheckAndInstallR(self):
        R_Location = os.path.isfile(r'C:\Program Files\R\R-3.5.3\bin\RScript.exe')

        if R_Location:
            tkMessageBox.showinfo("R Dependancy Check", "R Is Already Installed, please check the permissions on the application install folder in Program Files.")
        else:
            self.installR()

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
        self.txtFilePath.grid(row = 1, column = 0, columnspan = 6, sticky = "ew", padx = 5 , pady = 5)
        self.btnGetSample.grid(row = 2, column = 0, columnspan = 2, sticky = "w", padx = 5, pady = 5)
        self.btnSubmitSample.grid(row = 2, column = 4, columnspan = 2, sticky = "e", padx = 5, pady = 5)

        self.searchPane = LabelFrame(self.sideBar, text = "Cuckoo Search:", padx = 5, pady = 5)
        self.searchPane.pack(padx = 10, pady = 10, fill = "both")
        self.txtMD5Search = Entry(self.searchPane)
        self.btnSearchSample = Button(self.searchPane, text = "Search", command = self.btnSearchSamplePressed)
        self.txtMD5Search.grid(row = 1, column = 0, columnspan = 4, sticky = "we", padx = 5 , pady = 5)
        self.btnSearchSample.grid(row = 1, column = 4, columnspan = 2, sticky = "e", padx = 5, pady = 5)

        # Sets up the Dataset Model uploadPane
        self.dsmodelPane = LabelFrame(self.sideBar, text = "DataSet / Model", padx = 5, pady = 5)
        self.dsmodelPane.pack(padx = 10, pady = 10, fill = "both")
        self.btnNewDataset = Button(self.dsmodelPane, text = "New DataSet", command = self.btnNewDatasetPressed)
        self.btnNewModel = Button(self.dsmodelPane, text = "New Model", command = self.btnNewModelPressed)
        self.btnNewDataset.grid(row = 0, column = 0, columnspan = 2, sticky = "w", padx = 5, pady = 5)
        self.btnNewModel.grid(row = 0, column = 2, columnspan = 2, sticky = "e", padx = 5, pady = 5)
        self.btnDatasetStats = Button(self.dsmodelPane, text = "DataSet Stats", command = self.btnDatasetStatsPressed)
        self.btnModelStats = Button(self.dsmodelPane, text = "Model Stats", command = self.btnModelStatsPressed)
        self.btnDatasetStats.grid(row = 1, column = 0, columnspan = 2, sticky = "w", padx = 5, pady = 5)
        self.btnModelStats.grid(row = 1, column = 2, columnspan = 2, sticky = "e", padx = 5, pady = 5)

        self.utilitiesPane = LabelFrame(self.sideBar, text = "Utilities", padx = 5, pady = 5)
        self.utilitiesPane.pack(padx = 10, pady = 10, fill = "both")
        self.btnClearConsole = Button(self.utilitiesPane, text = "Clear Console", command = self.btnClearConsolePressed)
        self.btnCancelTask = Button(self.utilitiesPane, text = "Cancel Task", command = self.btnCancelTaskPressed)
        self.btnClearConsole.grid(row = 0, column = 0, columnspan = 2, sticky = "w", padx = 5, pady = 5)
        self.btnCancelTask.grid(row = 0, column = 2, columnspan = 2, sticky = "e", padx = 5, pady = 5)

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
        self.fileMenu.add_command(label = "Create New Dataset", command = self.btnNewDatasetPressed)
        self.fileMenu.add_command(label = "Create New Model", command = self.btnNewModelPressed)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label = "Preferences", command = self.showPreferences)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label = "Quit", command = self.quit)
        self.menuBar.add_cascade(label = "File", menu = self.fileMenu)

        self.dependancyMenu = Menu(self.menuBar, tearoff = 0)
        self.dependancyMenu.add_command(label = "R 3.5.3", command = self.dependancyCheckAndInstallR)
        self.menuBar.add_cascade(label = "Dependancies", menu = self.dependancyMenu)

    def __init__(self, master = None):
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
