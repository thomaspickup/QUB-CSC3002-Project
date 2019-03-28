import json, os, csv, sys

def getJSON(filepath):
    with open(filepath) as file:
        json_file = json.load(file)

    return json_file

def main():
    # The directory that the malware reports are stored in
    report_directory = ''
    dataset_directory = ''
    threshold_score = 1.8

    if len(sys.argv) == 3:
        report_directory = sys.argv[1]
        dataset_directory = sys.argv[2]
    else:
        report_directory = r"R:\\"
        dataset_directory = r'C:\\Users\\thomaspickup\\iCloudDrive\\Documents\\University\\CSC3002\\Assignment\\csc3002-project\\dataset'

    # Sets up the python lists
    dataset = []
    headers = ["SampleName"]
    api_names = []
    json_filepaths = []

    print("- Gathering API Headers")
    for file in os.listdir(report_directory):
        if file.endswith('.json'):
            # Stores the filepaths that end with .json in a list
            filepath = os.path.join(report_directory, file)


            # Opens the JSON file and decodes the JSON
            data = getJSON(filepath)
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
            print(filepath)
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
        data = getJSON(file)



        row.append(data['target']['file']['md5'])

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
        print(file)
        dataset.append(row)

    print("- Exporting API Results Table")
    # Exports table to csv file
    dataset_csv = dataset_directory + "\\api_results.csv"
    with open(dataset_csv, "w") as dataset_file:
        writer = csv.writer(dataset_file, lineterminator='\n')
        writer.writerows(dataset)

    print("~~ API Results Production: Complete ~~")

if __name__ == "__main__":
    main()
