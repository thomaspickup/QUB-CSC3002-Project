import os

# Asks for what is needed to run - saves on having to run whole generation each time
API_retrieval_run = raw_input("API Results Retrieval (Y/N): ")
Sample_production_run = raw_input("Sample List Production (Y/N): ")
Dataset_production_run = raw_input("API Dataset Production (Y/N): ")

if (API_retrieval_run == 'Y' or API_retrieval_run == 'y'):
    print("~~ API Results Retrieval: Started ~~")
    os.system("python Parser\\retrieve_apiresults.py")
if (Sample_production_run == 'Y' or Sample_production_run == 'y'):
    print("~~ Sample List Production: Started ~~")
    os.system("python Parser\\compile_samplelist.py")
if (Dataset_production_run == 'Y' or Dataset_production_run == 'y'):
    print("~~ API Results Production: Started ~~")
    os.system("python Parser\\compile_apiresults.py")
