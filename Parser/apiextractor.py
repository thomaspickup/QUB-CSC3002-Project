import json, os

def getJSON(filepath):
    with open(filepath) as file:
        json_file = json.load(file)

    return json_file

def main():
    directory = '/Users/thomaspickup/Documents/University/CSC3002/Assignment/CSC3002-Project/Malware Reports'

    api_names = []

    for file in os.listdir(directory):
        if file.endswith('.json'):
            filepath = os.path.join(directory, file)

            data = getJSON(filepath)

            print(data['info']['id'])
            for processes in data['behavior']['processes']:
                for call in processes['calls']:
                    found = False

                    for name in api_names:
                        if call['api'] == name:
                            found = True

                    if found == False:
                        api_names.append(call['api'])

    for name in api_names:
        print(name)

if __name__ == "__main__":
    main()
