from Tkinter import *
import tkFileDialog
from tkinter import ttk

class Application(Frame):
    # Functions
    def getSample(self):
        fileName = tkFileDialog.askopenfilename(initialdir = "C:\\", title = "Select Sample File", filetypes  = (("Binary Files", "*"), ("Executable Files", "*.exe"), ("DLL Files", "*.dll")))
        self.txtFilePath.delete(0, END)
        self.txtFilePath.insert(0, fileName)

    def submitSample(self):
        fileName = tkFileDialog.askopenfilename(initialdir = "C:\\", title = "Select Sample File", filetypes  = (("Binary Files", "*"), ("Executable Files", "*.exe"), ("DLL Files", "*.dll")))
        self.txtFilePath.delete(0, END)
        self.txtFilePath.insert(0, fileName)

    # Creates the UI
    def createWidgets(self):
        # Sets up Title Bar
        self.lblTitle = Label(self, text = "Malware Categorisation Using Machine Learning")
        titleFont = ("times", 16, "bold")
        self.lblTitle.config(font = titleFont)
        self.lblTitle.grid(row = 1, column = 0, columnspan = 5)

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

        # Sets up input box
        self.lblFilePath = Label(self, text = "Sample File: ")
        self.txtFilePath = Entry(self)
        self.btnGetSample = Button(self, text = "Open File", command = self.getSample)
        self.btnSubmitSample = Button(self, text = "Submit", command = self.submitSample)
        self.txtFilePath.grid(row = 2, column = 1, columnspan = 2, sticky = "nesw", pady = 5)
        self.lblFilePath.grid(row = 2, column = 0, columnspan = 1, pady = 5)
        self.btnGetSample.grid(row = 2, column = 3, columnspan = 1, pady = 5)
        self.btnSubmitSample.grid(row = 2, column = 4, columnspan = 1, pady = 5)

        self.commandWindowDisplay = Text(self)
        self.commandWindowDisplay.grid(row = 4, column = 0, columnspan = 5, rowspan = 3, sticky = "nesw")

    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
app = Application(master = root)
root.config(menu = app.menuBar)
root.title("Malware Categorisation")
root.resizable(width = False, height = False)
app.mainloop()
root.destroy()
