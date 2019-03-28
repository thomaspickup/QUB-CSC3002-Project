import os

ans = raw_input("API Results Retrieval (Y/N): ")
if (ans == 'Y' or ans == 'y'):
    print("~~ API Results Retrieval: Started ~~")
    os.system("python Parser\\retrieve_apiresults.py")

ans = raw_input("Sample List Production (Y/N): ")
if (ans == 'Y' or ans == 'y'):
    print("~~ Sample List Production: Started ~~")
    os.system("python Parser\\compile_samplelist.py")

ans = raw_input("API Dataset Production (Y/N): ")
if (ans == 'Y' or ans == 'y'):
    print("~~ API Results Production: Started ~~")
    os.system("python Parser\\compile_apiresults.py")
