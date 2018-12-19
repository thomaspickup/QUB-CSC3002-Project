import json, os, csv

def getJSON(filepath):
    with open(filepath) as file:
        json_file = json.load(file)

    return json_file

def main():
    # The directory that the malware reports are stored in
    directory = '/Users/thomaspickup/Documents/University/CSC3002/Assignment/CSC3002-Project/Malware-Reports'

    # Sets up the python lists
    dataset = []
    headers = ["FamilyID", "SampleID"]
    api_names = []
    json_filepaths = []

    for file in os.listdir(directory):
        if file.endswith('.json'):
            # Stores the filepaths that end with .json in a list
            filepath = os.path.join(directory, file)
            json_filepaths.append(filepath)

            # Opens the JSON file and decodes the JSON
            data = getJSON(filepath)

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

    # Adds the API names as table headers
    for name in api_names:
        headers.append(name)

    # Appends headers to dataset
    dataset.append(headers)

    # Loops through all the files again
        # Adds malware type and ID to pythong list
        # Loops through all the api_names
            # Counts how many times this api was called
            # Adds result to python list ['api_name', 'times_called']
        # Adds list row to table

    # Exports table to csv file
    dataset_csv = directory + "/dataset.csv"
    with open(dataset_csv, "w") as dataset_file:
        writer = csv.writer(dataset_file, lineterminator='\n')
        writer.writerows(dataset)

if __name__ == "__main__":
    main()
