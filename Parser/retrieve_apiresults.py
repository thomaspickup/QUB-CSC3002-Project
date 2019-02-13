import json, os, csv, sys

def getJSON(filepath):
    with open(filepath) as file:
        json_file = json.load(file)

    return json_file

def main():
    # The directory that the exports from the cuckoo environment are stored
    raw_directory = ''
    report_directory = ''

    if len(sys.argv) == 3:
        raw_directory = sys.argv[1]
        report_directory = sys.argv[2]
    else:
        raw_directory = "/reports"
        report_directory = "/output"

    print(raw_directory)
    print(report_directory)

    print("~~ API Results Retrieval: Complete ~~")

if __name__ == "__main__":
    main()
