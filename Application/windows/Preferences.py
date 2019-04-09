from Tkinter import *
from tkinter import ttk
from app_modules import configuration
import ConfigParser

class Preferences():
    def btnSaveLocationsPressed(self):
        cuckoo_server = self.txtCuckooServer.get()
        cuckoo_server_port = self.txtCuckooServerPort.get()
        sample_directory = self.txtSampleDirectory.get()
        dataset_directory = self.txtDataSetDirectory.get()
        model_directory = self.txtModelDirectory.get()
        cuckoo_export_directory = self.txtCuckooExportDirectory.get()
        reports_directory = self.txtReportsDirectory.get()

        config = ConfigParser.RawConfigParser()

        config.read('config.ini')

        config.set('locations', 'cuckoo_server', cuckoo_server)
        config.set('locations', 'cuckoo_server_port', cuckoo_server_port)
        config.set('locations', 'sample_directory', sample_directory)
        config.set('locations', 'dataset_directory', dataset_directory)
        config.set('locations', 'model_directory', model_directory)
        config.set('locations', 'cuckoo_export_directory', cuckoo_export_directory)
        config.set('locations', 'reports_directory', reports_directory)

        with open('config.ini', 'w') as config_file:
            config.write(config_file)

        reload(configuration)

        self.preferencesWindow.destroy()

    def btnCuckooConnectPressed(self):
        print("BTN CUCKOO CONNECT PRESSED")

    def verifyLocations(self):
        print(configuration.MODEL_DIRECTORY)

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
        self.btnSampleDirectoryOpenFolder = Button(self.locationsGroup, text = "Open")
        self.btnSampleDirectoryOpenFolder.grid(row = 1, column = 6, columnspan = 1, sticky = "nesw", pady = (0, 5), padx = 5)

        self.lblDataSetDirectory = Label(self.locationsGroup, text = "DataSet Directory", anchor = "w")
        self.lblDataSetDirectory.grid(row = 2, column = 0, columnspan = 1, sticky = "nesw", pady = 5, padx = 5)
        self.txtDataSetDirectory = Entry(self.locationsGroup)
        self.txtDataSetDirectory.grid(row = 2, column = 1, columnspan = 5, sticky = "nesw", pady = (0, 5), padx = 5)
        self.txtDataSetDirectory.insert(0, configuration.DATASET_DIRECTORY)
        self.btnDataSetDirectoryOpenFolder = Button(self.locationsGroup, text = "Open")
        self.btnDataSetDirectoryOpenFolder.grid(row = 2, column = 6, columnspan = 1, sticky = "nesw", pady = (0, 5), padx = 5)

        self.lblModelDirectory = Label(self.locationsGroup, text = "Model Directory", anchor = "w")
        self.lblModelDirectory.grid(row = 3, column = 0, columnspan = 1, sticky = "nesw", pady = 5, padx = 5)
        self.txtModelDirectory = Entry(self.locationsGroup)
        self.txtModelDirectory.grid(row = 3, column = 1, columnspan = 5, sticky = "nesw", pady = (0, 5), padx = 5)
        self.txtModelDirectory.insert(0, configuration.MODEL_DIRECTORY)
        self.btnModelDirectoryOpenFolder = Button(self.locationsGroup, text = "Open")
        self.btnModelDirectoryOpenFolder.grid(row = 3, column = 6, columnspan = 1, sticky = "nesw", pady = (0, 5), padx = 5)

        self.lblCuckooExportDirectory = Label(self.locationsGroup, text = "Cuckoo Exports", anchor = "w")
        self.lblCuckooExportDirectory.grid(row = 4, column = 0, columnspan = 1, sticky = "nesw", pady = 5, padx = 5)
        self.txtCuckooExportDirectory = Entry(self.locationsGroup)
        self.txtCuckooExportDirectory.grid(row = 4, column = 1, columnspan = 5, sticky = "nesw", pady = (0, 5), padx = 5)
        self.txtCuckooExportDirectory.insert(0, configuration.CUCKOO_EXPORT_DIRECTORY)
        self.btnCuckooExportDirectoryOpenFolder = Button(self.locationsGroup, text = "Open")
        self.btnCuckooExportDirectoryOpenFolder.grid(row = 4, column = 6, columnspan = 1, sticky = "nesw", pady = (0, 5), padx = 5)

        self.lblReportsDirectory = Label(self.locationsGroup, text = "Reports Directory", anchor = "w")
        self.lblReportsDirectory.grid(row = 5, column = 0, columnspan = 1, sticky = "nesw", pady = 5, padx = 5)
        self.txtReportsDirectory = Entry(self.locationsGroup)
        self.txtReportsDirectory.grid(row = 5, column = 1, columnspan = 5, sticky = "nesw", pady = (0, 5), padx = 5)
        self.txtReportsDirectory.insert(0, configuration.REPORTS_DIRECTORY)
        self.btnReportsOpenFolder = Button(self.locationsGroup, text = "Open", command = self.verifyLocations)
        self.btnReportsOpenFolder.grid(row = 5, column = 6, columnspan = 1, sticky = "nesw", pady = (0, 5), padx = 5)

        self.btnSaveLocations = Button(self.locationsGroup, text = "Save", command = self.btnSaveLocationsPressed)
        self.btnSaveLocations.grid(row = 10, column = 6, sticky = "nesw", columnspan = 1, pady = (0, 5), padx = 5)

    def __init__(self, master = None):
        self.preferencesWindow = Toplevel(master)
        self.createWidgets()
        self.preferencesWindow.title("Preferences")
        self.preferencesWindow.resizable(width = False, height = False)
        self.preferencesWindow.grid_rowconfigure(1, weight=1)
        self.preferencesWindow.grid_columnconfigure(1, weight=1)
        self.preferencesWindow.transient(master)
