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

    sample_types = []
    excluded_files = [".DS_Store"]

    if os.path.isdir(sample_directory):
        for root, dirs, files in os.walk(sample_directory):
            for file in files:
                if not file in excluded_files:
                    sample_types.append([file, os.path.basename(root)])

    malware_types = []
    sample_list = []
    next_malware_id = 0
    next_sample_id = 0

    for st in sample_types:
        malware_id = ""
        id_found = False

        for type in malware_types:
            if type[1] == st[1]:
                malware_id = str(type[0])
                id_found = True

        if id_found == False:
            next_malware_id = next_malware_id + 1
            malware_id = str(next_malware_id)
            malware_types.append([malware_id, st[1]])

        next_sample_id = next_sample_id + 1
        sample_list.append([next_sample_id, malware_id, st[0]])

    if os.path.isdir(output_directory):
        type_name = file_names[0]
        type_csv = os.path.join(output_directory, type_name)

        sample_name = file_names[1]
        sample_csv = os.path.join(output_directory, sample_name)

        with open(type_csv, "w") as csv_file:
            writer = csv.writer(csv_file, lineterminator='\n')
            writer.writerows(malware_types)

        with open(sample_csv, "w") as csv_file:
            writer = csv.writer(csv_file, lineterminator='\n')
            writer.writerows(sample_list)

    print("~~ Sample List Production: Complete ~~")
if __name__ == "__main__":
    main()
