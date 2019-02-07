import sys, os, csv

def main():
    sample_directory = ""
    output_directory = ""

    if len(sys.argv) == 3:
        sample_directory = sys.argv[1]
        output_directory = sys.argv[2]
    else:
        sample_directory = "/samples"
        output_directory = "/output"

    file_names = ['malware_types.csv', 'sample_list.csv']
    print(sample_directory)
    if os.path.isdir(sample_directory):
        for root, dirs, files in os.walk(sample_directory):
            for file in files:
                print(file)
                print(os.path.basename(root))

if __name__ == "__main__":
    main()
