import json, os
def getJSON(filepath):
    with open(filepath) as file:
        json_file = json.load(file)

    return json_file

def main():
    directory = '/Users/thomaspickup/Documents/University/CSC3002/Assignment/CSC3002-Project/Malware Reports'

    for file in os.listdir(directory):
        if file.endswith('.json'):
            filepath = os.path.join(directory, file)

            data = getJSON(filepath)

            print(data['info']['id'])

if __name__ == "__main__":
    main()
