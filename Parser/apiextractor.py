import json, os

def main():
    directory = '/Users/thomaspickup/Documents/University/CSC3002/Assignment/CSC3002-Project/Malware Reports'

    for file in os.listdir(directory):
        if file.endswith('.json'):
            filepath = os.path.join(directory, file)

            with open(filepath) as f:
                data = json.load(f)

            print(data['info']['id'])

if __name__ == "__main__":
    main()
