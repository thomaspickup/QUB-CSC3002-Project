from Tkinter import *
from tkinter import ttk
from app_modules import configuration
from scripts import functions
import ConfigParser, csv, decimal, os, tkMessageBox

class modelTable():
    def p(self, input):
        # Sets decimal accuracy to 3 places
        decimal.getcontext().prec = 3

        # Gets the passed data and converts to decimal
        percent = decimal.Decimal(input)

        # Returns a percentage as a string
        return str((percent * decimal.Decimal(100.00))) + "%"

    def populateTable(self):
        malware_types = []
        malware_csv = functions.getCSV(configuration.DATASET_DIRECTORY + r'\malware_types.csv', True)
        if "Error" not in malware_csv[0]:
            for row in malware_csv:
                malware_types.append(row[1])
        else:
            tkMessageBox.showwarning("Malware Types", "The Malware Types CSV could not be found, please check the Dataset directory to verify it exists.")
        
        confusionMatrix = functions.getCSV(configuration.MODEL_DIRECTORY + r'\confusionMatrix.csv', True)
        if "Error" not in confusionMatrix[0]:
            for row in confusionMatrix:
                self.confusionMatrix.insert('', 'end', text=malware_types[int(row[0].replace("Class: ", "")) - 1], values = (self.p(row[1]), self.p(row[2]), self.p(row[3]), self.p(row[4]), self.p(row[5]), self.p(row[6]), self.p(row[7]), self.p(row[8]), self.p(row[9]), self.p(row[10]), self.p(row[11])))
        else:
            tkMessageBox.showwarning("confusion Matrix", "The Confusion Matrix could not be found, please check the model directory to verify it exists.")

    def populateAccuracy(self):
        # Assume initaly there is no error
        hasError = False

        # Check if the file exists
        fileExists = os.path.isfile(configuration.MODEL_DIRECTORY + r"\accuracies.json")
        if fileExists:
            # Try catch to get any errors with the Json file itself
            try:
                # Get the JSON file if it exists
                accuracyJson = functions.getJSON(configuration.MODEL_DIRECTORY + r"\accuracies.json")

                # Check if the key 'dataset_accuracy' is present in the root of json object
                if 'dataset_accuracy' in accuracyJson:
                    # Itterates through the expected keys to see if any are missing
                    expected_keys = ['accuracy', 'total_items', 'correct', 'incorrect']
                    for key in expected_keys:
                        # If the key isn't in the main keys json object then throw an error
                        if key not in accuracyJson['dataset_accuracy']:
                            hasError = True
                else:
                    # Main key isn't in the json file so it isn't valid
                    hasError = True
            except ValueError:
                print(ValueError)
                hasError = True
        else:
            # File doesn't exist
            hasError = True

        if not hasError:
            # Import the data if all there
            self.txtAccuracy.insert(0, accuracyJson['dataset_accuracy']['accuracy'])
            self.txtTotalItems.insert(0, accuracyJson['dataset_accuracy']['total_items'])
            self.txtCorrect.insert(0, accuracyJson['dataset_accuracy']['correct'])
            self.txtIncorrect.insert(0, accuracyJson['dataset_accuracy']['incorrect'])
        else:
            # Show an error message if error has occured
            tkMessageBox.showwarning("JSON Error", "The JSON file provided either doesn't exist or isn't valid, please check the model directory to verify this file.")

        # Set the fields to read only regardless so user can't edit fields
        self.txtAccuracy.config(state = "readonly")
        self.txtTotalItems.config(state = "readonly")
        self.txtCorrect.config(state = "readonly")
        self.txtIncorrect.config(state = "readonly")

    def createWidgets(self):
        # Sets up column data
        column_ref = ["#0", "#1", "#2", "#3", "#4", "#5", "#6", "#7", "#8", "#9", "#10", "#11"]
        heading_text = ["Family", "Sensitivity", "Specifity", "Pos Pred Value", "Neg Pred Value", "Precision", "Recall", "F1", "Prevalance", "Detection Rate", "Detection Prevalance", "Balanced Accuracy"]
        table_headers = [column_ref, heading_text]
        standard_width = 60

        # Creates the title
        self.titleFrame = Frame(self.modelTable, height = 50)
        self.titleFrame.grid(row=0, column=0, sticky="new", pady = 5, padx = 5)
        self.lblTitle = Label(self.titleFrame, text = "Model Stats")
        titleFont = ("times", 16, "bold")
        self.lblTitle.config(font = titleFont)
        self.lblTitle.pack()

        # Creates the main content frame
        self.mainContent = Frame(self.modelTable, height = 200)
        self.mainContent.grid(row=1, column=0, sticky = "nesw", pady = (0, 5), padx = 5)

        # Creates the accuracies frame and data boxes for displaying accuracies.json
        self.accuraciesFrame = LabelFrame(self.mainContent, text = "Overall Accuracy")
        self.accuraciesFrame.grid(row = 0, column = 0, columnspan = 4, sticky = "nesw", pady = (0, 5), padx = 5)
        self.lblAccuracy = Label(self.accuraciesFrame, text = "Accuracy")
        self.lblAccuracy.grid(row = 0, column = 0, sticky = "nesw", pady = 5, padx = 5)
        self.lblTotalItems = Label(self.accuraciesFrame, text = "Total Test Items")
        self.lblTotalItems.grid(row = 1, column = 0, sticky = "nesw", pady = (0, 5), padx = 5)
        self.lblCorrect = Label(self.accuraciesFrame, text = "Correct Test Examples")
        self.lblCorrect.grid(row = 0, column = 3, sticky = "nesw", pady = (0, 5), padx = 5)
        self.lblIncorrect = Label(self.accuraciesFrame, text = "Incorrect Test Examples")
        self.lblIncorrect.grid(row = 1, column = 3, sticky = "nesw", pady = (0, 5), padx = 5)
        self.txtAccuracy = Entry(self.accuraciesFrame)
        self.txtAccuracy.grid(row = 0, column = 1, columnspan = 2, sticky = "nesw", pady = (0, 5), padx = 5)
        self.txtTotalItems = Entry(self.accuraciesFrame)
        self.txtTotalItems.grid(row = 1, column = 1, columnspan = 2, sticky = "nesw", pady = (0, 5), padx = 5)
        self.txtCorrect = Entry(self.accuraciesFrame)
        self.txtCorrect.grid(row = 0, column = 4, columnspan = 2, sticky = "nesw", pady = (0, 5), padx = 5)
        self.txtIncorrect = Entry(self.accuraciesFrame)
        self.txtIncorrect.grid(row = 1, column = 4, columnspan = 2, sticky = "nesw", pady = (0, 5), padx = 5)

        # Sets up the confusionMatrix tree view
        self.confusionMatrix = ttk.Treeview(self.mainContent, columns = table_headers[0][1:len(table_headers[0])])
        self.confusionMatrix.grid(row = 1, column = 0, columnspan = 4, sticky = "nesw", pady = (0, 5), padx = 5)

        # Itterates through all the table headers and sets them to the right text and size
        for i in range(len(table_headers[0])):
            self.confusionMatrix.heading(table_headers[0][i], text = table_headers[1][i])
            if i == 0:
                self.confusionMatrix.column(table_headers[0][i], width = standard_width * 2, anchor = 'center')
            else:
                self.confusionMatrix.column(table_headers[0][i], width = standard_width, anchor = 'center')

        # Calls population functions
        self.populateTable()
        self.populateAccuracy()

    def __init__(self, master = None):
        self.modelTable = Toplevel(master)
        self.createWidgets()
        self.modelTable.title("Model Stats")
        self.modelTable.resizable(width = False, height = False)
        self.modelTable.grid_rowconfigure(1, weight=1)
        self.modelTable.grid_columnconfigure(1, weight=1)
        self.modelTable.transient(master)
