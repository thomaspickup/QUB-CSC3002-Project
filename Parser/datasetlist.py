import sys, os, csv

def main():
    sample_directory = ""
    output_directory = ""

    if len(sys.argv) == 3:
        sample_directory = sys.argv[1]
        output_directory = sys.argv[2]

    file_names = ['malware_types.csv', 'sample_list.csv']

if __name__ == "__main__":
    main()
