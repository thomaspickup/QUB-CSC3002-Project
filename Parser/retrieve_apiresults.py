import os, sys
from shutil import copyfile

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

    print("- Starting Copying of Reports")
    count = 0

    for name in os.listdir(raw_directory):
        if name != ".DS_Store":
            results_file = raw_directory + "/" + name + "/reports/report.json"
            new_file = report_directory + "/" + name + ".json"

            print(new_file)
            copyfile(results_file, new_file)
            count = count + 1
    print("- Finished Copying " + str(count) + " report(s).")
    print("~~ API Results Retrieval: Complete ~~")

if __name__ == "__main__":
    main()
