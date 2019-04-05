import os, requests, time, csv

server_url = "http://localhost:8090/"
malware_file = raw_input("Please provide the location of the malware sample: ")# r"C:\Users\thomaspickup\iCloudDrive\Documents\University\CSC3002\Assignment\Samples\CryptoRansom\VirusShare_0d86ac1b7d00520bd18eb859f23fa490"
request_headers = {"Authorization": "Bearer S4MPL3"}

print("- Submitting Test Item")
with open(malware_file, "rb") as sample:
    files = {"file": ("product_submission", sample)}
    this_request = server_url + r"tasks/create/file"
    r = requests.post(this_request, headers=request_headers, files=files)

task_id = r.json()["task_id"]

print("- Testing of Test Item")
this_request = server_url + r"tasks/view/" + str(task_id)
r = requests.get(this_request)
current_status = r.json()["task"]["status"]
print(current_status)

while current_status != "reported":
    time.sleep(5)
    r = requests.get(this_request)
    current_status = r.json()["task"]["status"]
    print(current_status)
    pass

print("- Completed Testing of Item")

print("- Downloading Report")
this_request = server_url + r"tasks/report/" + str(task_id)
r = requests.get(this_request)
report = r.json()
print("- Finished Downloading Report")

headers = ["SampleName"]
dataset = []

with open(r'Model\api_headers.csv') as csv_file:
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

print("- Exporting API Results Table")

# Exports table to csv file
dataset_csv =  r"Production\product_api.csv"
with open(dataset_csv, "w") as dataset_file:
    writer = csv.writer(dataset_file, lineterminator='\n')
    writer.writerows(dataset)

os.system(r"rscript C:\Users\thomaspickup\iCloudDrive\Documents\University\CSC3002\Assignment\CSC3002-Project\MachineLearning\Product_Script.R")
