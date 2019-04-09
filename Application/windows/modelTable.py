from Tkinter import *
from tkinter import ttk
from app_modules import configuration
import ConfigParser, csv, decimal

class modelTable():
    def p(self, input):
        decimal.getcontext().prec = 3
        percent = decimal.Decimal(input)

        return str((percent * decimal.Decimal(100.00))) + "%"
    def populateTable(self):
        malware_types = []

        with open(configuration.DATASET_DIRECTORY + r'\malware_types.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            # Skips the Headers
            next(csv_reader, None)

            for row in csv_reader:
                malware_types.append(row[1])

        with open(configuration.MODEL_DIRECTORY + r'\confusionMatrix.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            # Skips the Headers
            next(csv_reader, None)

            for row in csv_reader:
                self.confusionMatrix.insert('', 'end', text=malware_types[int(row[0].replace("Class: ", "")) - 1], values = (self.p(row[1]), self.p(row[2]), self.p(row[3]), self.p(row[4]), self.p(row[5]), self.p(row[6]), self.p(row[7]), self.p(row[8]), self.p(row[9]), self.p(row[10]), self.p(row[11])))

    def createWidgets(self):
        column_ref = ["#0", "#1", "#2", "#3", "#4", "#5", "#6", "#7", "#8", "#9", "#10", "#11"]
        heading_text = ["Family", "Sensitivity", "Specifity", "Pos Pred Value", "Neg Pred Value", "Precision", "Recall", "F1", "Prevalance", "Detection Rate", "Detection Prevalance", "Balanced Accuracy"]
        table_headers = [column_ref, heading_text]
        standard_width = 60

        self.titleFrame = Frame(self.modelTable, height = 50)
        self.titleFrame.grid(row=0, column=0, sticky="new", pady = 5, padx = 5)
        self.lblTitle = Label(self.titleFrame, text = "Model Stats")
        titleFont = ("times", 16, "bold")
        self.lblTitle.config(font = titleFont)
        self.lblTitle.pack()

        self.mainContent = Frame(self.modelTable, height = 200)
        self.mainContent.grid(row=1, column=0, sticky = "nesw", pady = (0, 5), padx = 5)
        self.confusionMatrix = ttk.Treeview(self.mainContent, columns = table_headers[0][1:len(table_headers[0])])
        self.confusionMatrix.grid(row = 0, column = 0, sticky = "nesw", pady = (0, 5), padx = 5)

        # Inserted at the root, program chooses id:
        for i in range(len(table_headers[0])):
            self.confusionMatrix.heading(table_headers[0][i], text = table_headers[1][i])
            if i == 0:
                self.confusionMatrix.column(table_headers[0][i], width = standard_width * 2, anchor = 'center')
            else:
                self.confusionMatrix.column(table_headers[0][i], width = standard_width, anchor = 'center')

        self.populateTable()

    def __init__(self, master = None):
        self.modelTable = Toplevel(master)
        self.createWidgets()
        self.modelTable.title("Model Stats")
        self.modelTable.resizable(width = False, height = False)
        self.modelTable.grid_rowconfigure(1, weight=1)
        self.modelTable.grid_columnconfigure(1, weight=1)
        self.modelTable.transient(master)
