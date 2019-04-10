from Tkinter import *
from tkinter import ttk
from app_modules import configuration
from scripts import functions
import ConfigParser, tkMessageBox, tkFileDialog, os

class Preferences():
    def btnSaveLocationsPressed(self):
        errorString = self.verifyLocations()
        if errorString == "":
            cuckoo_server = self.txtCuckooServer.get()
            cuckoo_server_port = self.txtCuckooServerPort.get()
            sample_directory = self.txtSampleDirectory.get()
            dataset_directory = self.txtDataSetDirectory.get()
            model_directory = self.txtModelDirectory.get()
            cuckoo_export_directory = self.txtCuckooExportDirectory.get()
            reports_directory = self.txtReportsDirectory.get()

            r_location = self.txtRLocationDirectory.get()

            run_boruta = self.borutaChecked.get()
            run_crossvalidation = self.crossvalidationChecked.get()
            number_of_folds = self.numFoldsSlider.get()

            config = ConfigParser.RawConfigParser()

            config.read('config.ini')

            config.set('locations', 'cuckoo_server', cuckoo_server)
            config.set('locations', 'cuckoo_server_port', cuckoo_server_port)
            config.set('locations', 'sample_directory', sample_directory)
            config.set('locations', 'dataset_directory', dataset_directory)
            config.set('locations', 'model_directory', model_directory)
            config.set('locations', 'cuckoo_export_directory', cuckoo_export_directory)
            config.set('locations', 'reports_directory', reports_directory)

            config.set('program', 'r_location', r_location)
            config.set('machinelearning', 'run_boruta', run_boruta)
            config.set('machinelearning', 'run_crossvalidation', run_crossvalidation)
            config.set('machinelearning', 'number_of_folds', number_of_folds)

            with open('config.ini', 'w') as config_file:
                config.write(config_file)

            reload(configuration)

            self.preferencesWindow.destroy()
        else:
            tkMessageBox.showwarning("Error Saving Settings", "The following errors were identified: \n" + errorString)

    def btnCuckooConnectPressed(self):
        isActive = functions.checkCuckooOnline(self.txtCuckooServer.get(), self.txtCuckooServerPort.get())

        if isActive:
            tkMessageBox.showinfo("Cuckoo Server Check", "Cuckoo Server: Connected")
        else:
            tkMessageBox.showwarning("Cuckoo Server Check", "Cuckoo Server: Connection Failed, please check the details provided.")

    def verifyLocations(self):
        errorString = ""
        cuckooOnline = functions.checkCuckooOnline(self.txtCuckooServer.get(), self.txtCuckooServerPort.get())

        if not cuckooOnline: errorString = errorString + "Cuckoo Server cannot be contacted\n"
        if not os.path.isdir(self.txtSampleDirectory.get()): errorString = errorString + "Sample Directory not valid\n"
        if not os.path.isdir(self.txtDataSetDirectory.get()): errorString = errorString + "DataSet Directory not valid\n"
        if not os.path.isdir(self.txtModelDirectory.get()): errorString = errorString + "Model Directory not valid\n"
        if not os.path.isdir(self.txtCuckooExportDirectory.get()): errorString = errorString + "Cuckoo Export Directory not valid\n"
        if not os.path.isdir(self.txtReportsDirectory.get()): errorString = errorString + "Reports Directory not valid\n"

        return errorString

    def openFileDialog(self, textbox):
        directory = tkFileDialog.askdirectory()

        if os.path.isdir(directory):
            textbox.delete(0, END)
            textbox.insert(0, directory)

    def populateLocations(self):
        self.lblCuckoo = Label(self.locationsGroup, text = "Cuckoo Server", anchor = "w")
        self.lblCuckoo.grid(row = 0, column = 0, columnspan = 1, sticky = "nesw", pady = 5, padx = 5)
        self.txtCuckooServer = Entry(self.locationsGroup)
        self.txtCuckooServer.insert(0, configuration.CUCKOO_SERVER)
        self.txtCuckooServer.grid(row = 0, column = 1, columnspan = 1, sticky = "nesw", pady = (0, 5), padx = 5)
        self.txtCuckooServerPort = Entry(self.locationsGroup)
        self.txtCuckooServerPort.insert(0, configuration.CUCKOO_SERVER_PORT)
        self.txtCuckooServerPort.grid(row = 0, column = 2, columnspan = 1, sticky = "nesw", pady = (0, 5), padx = 5)
        self.btnCuckooConnect = Button(self.locationsGroup, text = "Connect", command = self.btnCuckooConnectPressed)
        self.btnCuckooConnect.grid(row = 0, column = 6, columnspan = 1, sticky = "nesw", pady = (0, 5), padx = 5)

        self.lblSampleDirectory = Label(self.locationsGroup, text = "Sample Directory", anchor = "w")
        self.lblSampleDirectory.grid(row = 1, column = 0, columnspan = 1, sticky = "nesw", pady = 5, padx = 5)
        self.txtSampleDirectory = Entry(self.locationsGroup)
        self.txtSampleDirectory.grid(row = 1, column = 1, columnspan = 5, sticky = "nesw", pady = (0, 5), padx = 5)
        self.txtSampleDirectory.insert(0, configuration.SAMPLE_DIRECTORY)
        self.btnSampleDirectoryOpenFolder = Button(self.locationsGroup, text = "Open", command =  lambda: self.openFileDialog(self.txtSampleDirectory))
        self.btnSampleDirectoryOpenFolder.grid(row = 1, column = 6, columnspan = 1, sticky = "nesw", pady = (0, 5), padx = 5)

        self.lblDataSetDirectory = Label(self.locationsGroup, text = "DataSet Directory", anchor = "w")
        self.lblDataSetDirectory.grid(row = 2, column = 0, columnspan = 1, sticky = "nesw", pady = 5, padx = 5)
        self.txtDataSetDirectory = Entry(self.locationsGroup)
        self.txtDataSetDirectory.grid(row = 2, column = 1, columnspan = 5, sticky = "nesw", pady = (0, 5), padx = 5)
        self.txtDataSetDirectory.insert(0, configuration.DATASET_DIRECTORY)
        self.btnDataSetDirectoryOpenFolder = Button(self.locationsGroup, text = "Open", command = lambda: self.openFileDialog(self.txtDataSetDirectory))
        self.btnDataSetDirectoryOpenFolder.grid(row = 2, column = 6, columnspan = 1, sticky = "nesw", pady = (0, 5), padx = 5)

        self.lblModelDirectory = Label(self.locationsGroup, text = "Model Directory", anchor = "w")
        self.lblModelDirectory.grid(row = 3, column = 0, columnspan = 1, sticky = "nesw", pady = 5, padx = 5)
        self.txtModelDirectory = Entry(self.locationsGroup)
        self.txtModelDirectory.grid(row = 3, column = 1, columnspan = 5, sticky = "nesw", pady = (0, 5), padx = 5)
        self.txtModelDirectory.insert(0, configuration.MODEL_DIRECTORY)
        self.btnModelDirectoryOpenFolder = Button(self.locationsGroup, text = "Open", command =  lambda: self.openFileDialog(self.txtModelDirectory))
        self.btnModelDirectoryOpenFolder.grid(row = 3, column = 6, columnspan = 1, sticky = "nesw", pady = (0, 5), padx = 5)

        self.lblCuckooExportDirectory = Label(self.locationsGroup, text = "Cuckoo Exports", anchor = "w")
        self.lblCuckooExportDirectory.grid(row = 4, column = 0, columnspan = 1, sticky = "nesw", pady = 5, padx = 5)
        self.txtCuckooExportDirectory = Entry(self.locationsGroup)
        self.txtCuckooExportDirectory.grid(row = 4, column = 1, columnspan = 5, sticky = "nesw", pady = (0, 5), padx = 5)
        self.txtCuckooExportDirectory.insert(0, configuration.CUCKOO_EXPORT_DIRECTORY)
        self.btnCuckooExportDirectoryOpenFolder = Button(self.locationsGroup, text = "Open", command =  lambda: self.openFileDialog(self.txtCuckooExportDirectory))
        self.btnCuckooExportDirectoryOpenFolder.grid(row = 4, column = 6, columnspan = 1, sticky = "nesw", pady = (0, 5), padx = 5)

        self.lblReportsDirectory = Label(self.locationsGroup, text = "Reports Directory", anchor = "w")
        self.lblReportsDirectory.grid(row = 5, column = 0, columnspan = 1, sticky = "nesw", pady = 5, padx = 5)
        self.txtReportsDirectory = Entry(self.locationsGroup)
        self.txtReportsDirectory.grid(row = 5, column = 1, columnspan = 5, sticky = "nesw", pady = (0, 5), padx = 5)
        self.txtReportsDirectory.insert(0, configuration.REPORTS_DIRECTORY)
        self.btnReportsOpenFolder = Button(self.locationsGroup, text = "Open", command =  lambda: self.openFileDialog(self.txtReportsDirectory))
        self.btnReportsOpenFolder.grid(row = 5, column = 6, columnspan = 1, sticky = "nesw", pady = (0, 5), padx = 5)

    def populateProgram(self):
        self.lblRLocationDirectory = Label(self.programGroup, text = "R Install Location", anchor = "w")
        self.lblRLocationDirectory.grid(row = 0, column = 0, columnspan = 1, sticky = "nesw", pady = 5, padx = 5)
        self.txtRLocationDirectory = Entry(self.programGroup)
        self.txtRLocationDirectory.grid(row = 0, column = 1, columnspan = 5, sticky = "nesw", pady = (0, 5), padx = 5)
        self.txtRLocationDirectory.insert(0, configuration.R_LOCATION)
        self.btnROpenFolder = Button(self.programGroup, text = "Open", command =  lambda: self.openFileDialog(self.txtRLocationDirectory))
        self.btnROpenFolder.grid(row = 0, column = 6, columnspan = 1, sticky = "nesw", pady = (0, 5), padx = 5)

    def populateMachineLearning(self):
        self.borutaChecked = IntVar()
        self.borutaCheckBox = Checkbutton(self.machineLearningGroup, text="Run Automatic Feature Selection", anchor = "w", variable = self.borutaChecked)
        self.borutaCheckBox.grid(row = 0, column = 0, sticky = "nesw", pady = 5, padx = 5)
        self.borutaChecked.set(int(configuration.RUN_BORUTA))

        self.crossvalidationChecked = IntVar()
        self.crossvalidationCheckBox = Checkbutton(self.machineLearningGroup, text="Run Cross-Validation in Model Creation", anchor = "w", variable = self.crossvalidationChecked)
        self.crossvalidationCheckBox.grid(row = 1, column = 0, sticky = "nesw", pady = (0, 5), padx = 5)
        self.crossvalidationChecked.set(int(configuration.RUN_CROSSVALIDATION))

        self.lblNumFolds = Label(self.machineLearningGroup, text = "Number of Folds")
        self.lblNumFolds.grid(row = 2, column = 0, sticky = "nesw", pady = (0, 5), padx = 5)
        self.numFoldsSlider = Scale(self.machineLearningGroup, from_= 2, to = 50, orient = HORIZONTAL)
        self.numFoldsSlider.set(int(configuration.NUMBER_OF_FOLDS))
        self.numFoldsSlider.grid(row = 2, column = 1, sticky = "nesw", pady = (0, 5), padx = 5)
        if self.crossvalidationChecked.get() == 0:
            self.numFoldsSlider.config(state = 'disabled')

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
        self.programGroup = LabelFrame(self.mainContent, text = "Program Settings")
        self.programGroup.grid(row = 1, column = 0, sticky = "nesw", pady = (0, 5), padx = 5)
        self.machineLearningGroup = LabelFrame(self.mainContent, text = "Machine Learning")
        self.machineLearningGroup.grid(row = 2, column = 0, sticky = "nesw", pady = (0, 5), padx = 5)

        self.populateLocations()
        self.populateProgram()
        self.populateMachineLearning()

        self.btnSaveLocations = Button(self.mainContent, text = "Save", command = self.btnSaveLocationsPressed)
        self.btnSaveLocations.grid(row = 4, column = 0, sticky = "nesw", columnspan = 1, pady = (0, 5), padx = 5)

    def __init__(self, master = None):
        self.preferencesWindow = Toplevel(master)
        self.createWidgets()
        self.preferencesWindow.title("Preferences")
        self.preferencesWindow.resizable(width = False, height = False)
        self.preferencesWindow.grid_rowconfigure(1, weight=1)
        self.preferencesWindow.grid_columnconfigure(1, weight=1)
        self.preferencesWindow.transient(master)
