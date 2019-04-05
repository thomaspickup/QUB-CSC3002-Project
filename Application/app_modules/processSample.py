from Tkinter import *
from scripts import functions
import os, time, requests, csv, subprocess


def analyze(sampleLocation, printer):
    server_url = "http://localhost:8090/"
    malware_file = sampleLocation
    request_headers = {"Authorization": "Bearer S4MPL3"}

    # self.commandWindowDisplay.insert(END, "- Submitting Test Item")
    #
    # with open(malware_file, "rb") as sample:
    #     files = {"file": ("product_submission", sample)}
    #     this_request = server_url + r"tasks/create/file"
    #     r = requests.post(this_request, headers=request_headers, files=files)

    task_id = 3171 #r.json()["task_id"]

    printer.insert(END, "- Testing of Test Item\n")

    this_request = server_url + r"tasks/view/" + str(task_id)
    r = requests.get(this_request)
    current_status = r.json()["task"]["status"]
    printer.insert(END, current_status)


    while current_status != "reported":
        time.sleep(5)
        r = requests.get(this_request)
        current_status = r.json()["task"]["status"]
        printer.insert(END, current_status)

        pass

    printer.insert(END, "- Completed Testing of Item\n")


    printer.insert(END, "- Downloading Report\n")


    this_request = server_url + r"tasks/report/" + str(task_id)
    r = requests.get(this_request)
    report = r.json()
    printer.insert(END, "- Finished Downloading Report\n")


    headers = ["SampleName"]
    dataset = []

    with open(r'C:\Users\thomaspickup\iCloudDrive\Documents\University\CSC3002\Assignment\CSC3002-Project\Experimental\Model\api_headers.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            api_names = row


    # Adds the API names as table headers
    for name in api_names:
        headers.append(name)


    # Appends headers to dataset
    dataset.append(headers)

    if 'md5' in report['target']['file']:
        row = []
        row.append(report['target']['file']['md5'])

        # Loops through all the api_names
        for api in api_names:
            count = 0
            # Counts how many times this api was called

            for processes in report['behavior']['processes']:
                for call in processes['calls']:
                    if call['api'] == api:
                        count += 1

            # Adds result to python list ['api_name', 'times_called']
            row.append(count)


        # Adds list row to table
        dataset.append(row)

    printer.insert(END, "- Exporting API Results Table\n")


    # Exports table to csv file
    dataset_csv =  r"C:\Users\thomaspickup\iCloudDrive\Documents\University\CSC3002\Assignment\CSC3002-Project\Experimental\Production\product_api.csv"
    with open(dataset_csv, "w") as dataset_file:
        writer = csv.writer(dataset_file, lineterminator='\n')
        writer.writerows(dataset)
    command = ["rscript", r"C:\Users\thomaspickup\iCloudDrive\Documents\University\CSC3002\Assignment\CSC3002-Project\Application\mlcore\Product_Script.R"]
    functions.runScript(command, printer)

    printer.insert(END, "- Finished\n")
