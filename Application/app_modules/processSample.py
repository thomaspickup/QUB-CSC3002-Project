from Tkinter import *
from scripts import functions
import os, time, requests, csv, subprocess, hashlib, configuration

def analyze(sampleLocation, printer, statusbar):
    statusbar.config(text = "Running Command: Process Sample")

    # Concat the server url from the host and port
    server_url = configuration.CUCKOO_SERVER
    server_port = configuration.CUCKOO_SERVER_PORT
    server =  r"http://" + server_url + r":" + server_port + r"/"

    malware_file = sampleLocation
    request_headers = {"Authorization": "Bearer S4MPL3"}

    # ####################################### #
    #                                         #
    #           Report Generation             #
    #                                         #
    # ####################################### #
    # First we get the MD5 Hash of the sample and see if it already exists on cuckoo
    printer.insert(END, "- Submitting Test Item\n")

    hash_md5 = hashlib.md5()
    with open(malware_file, "rb") as f:
      for chunk in iter(lambda: f.read(4096), b""):
        hash_md5.update(chunk)
    md5Hash = hash_md5.hexdigest()

    with open(malware_file, "rb") as sample:
        this_request = server + r"files/view/md5/" + md5Hash
        r = requests.get(this_request)
    result = r.json()

    if "sample" not in result:
        exists = False
    else:
        exists = True

    # If the file already exists then we continue straight into the model eval stage
    if exists:
        printer.insert(END, "** File Already Exists Skipping to Report Download **\n")
        task_id = result["sample"]["id"]
    else:
        # Else we submit the sample and then poll on the report being completed
        with open(malware_file, "rb") as sample:
            files = {"file": ("product_submission", sample)}
            this_request = server + r"tasks/create/file"
            r = requests.post(this_request, headers=request_headers, files=files)

        task_id = r.json()["task_id"]

        printer.insert(END, "- Testing of Test Item\n")
        this_request = server + r"tasks/view/" + str(task_id)
        r = requests.get(this_request)
        current_status = r.json()["task"]["status"]
        printer.insert(END, current_status + "\n")

        while current_status != "reported":
            time.sleep(5)
            r = requests.get(this_request)
            current_status = r.json()["task"]["status"]
            printer.insert(END, current_status + "\n")

            pass

        printer.insert(END, "- Completed Testing of Item\n")


    printer.insert(END, "- Downloading Report\n")
    this_request = server + r"tasks/report/" + str(task_id)
    r = requests.get(this_request)
    report = r.json()
    printer.insert(END, "- Finished Downloading Report\n")

    # ####################################### #
    #                                         #
    #         API Results Generation          #
    #                                         #
    # ####################################### #
    headers = ["SampleName"]
    dataset = []

    with open(configuration.MODEL_DIRECTORY + r'\api_headers.csv') as csv_file:
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

    # ####################################### #
    #                                         #
    #           Sample Evaluation             #
    #                                         #
    # ####################################### #
    # Exports table to csv file
    dataset_csv =  os.getcwd() + r"\tmp\product_api.csv"
    with open(dataset_csv, "w") as dataset_file:
        writer = csv.writer(dataset_file, lineterminator='\n')
        writer.writerows(dataset)
    command = ["rscript", os.getcwd() + r"\mlcore\Product_Script.R"]
    functions.runScript(command, printer)

    printer.insert(END, "- Finished\n")
    statusbar.config(text = "Waiting for Command...")
