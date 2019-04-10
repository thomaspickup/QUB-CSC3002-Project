from Tkinter import *
from tkinter import ttk
from app_modules import configuration
from scripts import functions
import decimal, os, tkMessageBox

class datasetStats():
    def loadData(self):
        malware_types = []
        malware_csv = functions.getCSV(configuration.DATASET_DIRECTORY + r'\malware_types.csv', True)
        if "Error" not in malware_csv[0]:
            for row in malware_csv:
                malware_types.append([row[0], row[1], 0, 0])
        else:
            tkMessageBox.showwarning("Malware Types", "The Malware Types CSV could not be found, please check the Dataset directory to verify it exists.")

        api_results = []
        api_csv = functions.getCSV(configuration.DATASET_DIRECTORY + r'\api_results.csv', True)
        if "Error" not in api_csv[0]:
            for row in api_csv:
                api_results.append(row)
        else:
            tkMessageBox.showwarning("API CSV", "The API CSV could not be found, please check the dataset directory to verify it exists.")

        sample_list = []
        sample_csv = functions.getCSV(configuration.DATASET_DIRECTORY + r'\sample_list.csv', True)
        if "Error" not in sample_csv[0]:
            for row in sample_csv:
                sample_list.append(row)
        else:
            tkMessageBox.showwarning("Sample List CSV", "The Sample List CSV could not be found, please check the dataset directory to verify it exists.")

        for api in api_results:
            for sample in sample_list:
                if api[0] == sample[2]:
                    malware_id = sample[1]
                    malware_score = api[1]

                    for malware in malware_types:
                        if malware[0] == malware_id:
                            malware[2] += decimal.Decimal(malware_score)
                            malware[3] += 1

        decimal.getcontext().prec = 3
        for malware in malware_types:
            malware[2] = malware[2] / malware[3]
            self.statsTable.insert('', 'end', text=malware[1], values = (malware[2], malware[3]))

        print(malware_types)
    def createWidgets(self):
        # Sets up column data
        column_ref = ["#0", "#1", "#2"]
        heading_text = ["Family", "Average Cuckoo Score", "Total Items"]
        table_headers = [column_ref, heading_text]
        standard_width = 130

        # Creates the title
        self.titleFrame = Frame(self.datasetStats, height = 50)
        self.titleFrame.grid(row=0, column=0, sticky="new", pady = 5, padx = 5)
        self.lblTitle = Label(self.titleFrame, text = "Dataset Stats")
        titleFont = ("times", 16, "bold")
        self.lblTitle.config(font = titleFont)
        self.lblTitle.pack()

        # Creates the main content frame
        self.mainContent = Frame(self.datasetStats)
        self.mainContent.grid(row=1, column=0, sticky = "nesw", pady = (0, 5), padx = 5)

        # Sets up the dataset Stats tree view
        self.statsTable = ttk.Treeview(self.mainContent, columns = table_headers[0][1:len(table_headers[0])])
        self.statsTable.grid(row = 1, column = 0, columnspan = 4, sticky = "nesw", pady = (0, 5), padx = 5)

        # Itterates through all the table headers and sets them to the right text and size
        for i in range(len(table_headers[0])):
            self.statsTable.heading(table_headers[0][i], text = table_headers[1][i])
            self.statsTable.column(table_headers[0][i], width = standard_width, anchor = 'center')

        self.loadData()

    def __init__(self, master = None):
        self.datasetStats = Toplevel(master)
        self.createWidgets()
        self.datasetStats.title("Dataset Stats")
        self.datasetStats.resizable(width = False, height = False)
        self.datasetStats.grid_rowconfigure(1, weight=1)
        self.datasetStats.grid_columnconfigure(1, weight=1)
        self.datasetStats.transient(master)
