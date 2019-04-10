from Tkinter import *
from scripts import functions
import json, os, csv, sys, configuration

def compile(printer):
    # The directory that the malware reports are stored in
    report_directory = configuration.REPORTS_DIRECTORY
    dataset_directory = configuration.DATASET_DIRECTORY
    isReportDirectory = os.path.isdir(report_directory)
    isDatasetDirectory = os.path.isdir(dataset_directory)

    if isReportDirectory and isDatasetDirectory:
        threshold_score = 0.2

        # Sets up the python lists
        dataset = []
        headers = ["SampleName", "Score"]
        api_names = []
        json_filepaths = []

        printer.insert(END, "- Gathering API Headers\n")
        for file in os.listdir(report_directory):
            if file.endswith('.json'):
                # Stores the filepaths that end with .json in a list
                filepath = os.path.join(report_directory, file)


                # Opens the JSON file and decodes the JSON
                data = functions.getJSON(filepath)
                if data['info']['score'] <= threshold_score:
                    continue

                if 'behavior' not in data:
                    continue

                # Loops through all the processes
                for processes in data['behavior']['processes']:
                    # Loops through all the calls
                    for call in processes['calls']:
                        # Checks to see if the API Name is already in api_names
                        found = False
                        for name in api_names:
                            if call['api'] == name:
                                found = True

                        # If the api name isn't in the list - append it to it
                        if found == False:
                            api_names.append(call['api'])
                printer.insert(END, filepath + "\n")
                json_filepaths.append(filepath)

        # Adds the API names as table headers
        for name in api_names:
            headers.append(name)

        # Appends headers to dataset
        dataset.append(headers)

        print("- Counting API Interances")
        for file in json_filepaths:
            # Creates empty array to store results
            row = []

            # Gets json file
            data = functions.getJSON(file)

            if 'md5' in data['target']['file']:
                row.append(data['target']['file']['md5'])
                row.append(data['info']['score'])

                # Loops through all the api_names
                for api in api_names:
                    count = 0
                    # Counts how many times this api was called

                    for processes in data['behavior']['processes']:
                        for call in processes['calls']:
                            if call['api'] == api:
                                count += 1

                    # Adds result to python list ['api_name', 'times_called']
                    row.append(count)

                # Adds list row to table
                printer.insert(END, file + "\n")
                dataset.append(row)

        printer.insert(END, "- Exporting API Results Table\n")
        # Exports table to csv file
        dataset_csv = dataset_directory + "\\api_results.csv"
        with open(dataset_csv, "w") as dataset_file:
            writer = csv.writer(dataset_file, lineterminator='\n')
            writer.writerows(dataset)
    else:
        printer.insert(END, "** ERROR: Reports or Dataset Directory are Invalid, please check preferences **\n")

    printer.insert(END, "~~ API Results Production: Complete ~~\n")
