from Tkinter import *
import sys, os, csv, hashlib, configuration

def compile(printer):
    sample_directory = configuration.SAMPLE_DIRECTORY
    output_directory = configuration.DATASET_DIRECTORY
    isSampleDir = os.path.isdir(sample_directory)
    isOutputDir = os.path.isdir(output_directory)

    if isSampleDir and isOutputDir:
        file_names = ['malware_types.csv', 'sample_list.csv']

        sample_types = []
        excluded_files = [".DS_Store"]

        printer.insert(END, "- Gathering MD5 Hashes and Malware Types\n")
        for root, dirs, files in os.walk(sample_directory):
            for file in files:
                if not file in excluded_files:
                    file_name = root + '\\' + file
                    hash_md5 = hashlib.md5()
                    with open(file_name, "rb") as f:
                      for chunk in iter(lambda: f.read(4096), b""):
                        hash_md5.update(chunk)

                    sample_types.append([hash_md5.hexdigest(), os.path.basename(root)])
        malware_types = []
        sample_list = []
        next_malware_id = 0
        next_sample_id = 0

        printer.insert(END, '- Creating Sample List Table\n')
        printer.insert(END, '- Creating Malware Types Table\n')

        malware_headers = ['MalwareID', 'MalwareName']
        sample_headers = ['SampleID', 'MalwareID', 'MD5hash']

        malware_types.append(malware_headers)
        sample_list.append(sample_headers)

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
            sample_list.append([next_sample_id, malware_id, st[0].replace("VirusShare_", "")])

        type_name = file_names[0]
        type_csv = os.path.join(output_directory, type_name)

        sample_name = file_names[1]
        sample_csv = os.path.join(output_directory, sample_name)

        printer.insert(END, "- Saving Malware Types Table\n")
        with open(type_csv, "w") as csv_file:
            writer = csv.writer(csv_file, lineterminator='\n')
            writer.writerows(malware_types)

        printer.insert(END, "- Saving Sample List Table\n")
        with open(sample_csv, "w") as csv_file:
            writer = csv.writer(csv_file, lineterminator='\n')
            writer.writerows(sample_list)
    else:
        printer.insert(END, "** ERROR: Sample or Dataset Directory are Invalid, please check preferences **\n")
    printer.insert(END, "~~ Sample List Production: Complete ~~\n")
