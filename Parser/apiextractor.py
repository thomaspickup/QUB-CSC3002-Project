import json

def main():
    with open("/Users/thomaspickup/Documents/University/CSC3002/Assignment/CSC3002-Project/Malware Reports/report.json") as f:
        data = json.load(f)

    print(data['info']['id'])

if __name__ == "__main__":
    main()
