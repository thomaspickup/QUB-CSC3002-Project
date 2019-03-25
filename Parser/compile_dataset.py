import os

print("~~ API Results Retrieval: Started ~~")
os.system("python Parser\\retrieve_apiresults.py")

print("~~ Sample List Production: Started ~~")
os.system("python Parser\\compile_samplelist.py")

print("~~ API Results Production: Started ~~")
os.system("python Parser\\compile_apiresults.py")
