import os

print("~~ API Results Retrieval: Started ~~")
os.system("python retrieve_apiresults.py '/Users/thomaspickup/Documents/University/CSC3002/Assignment/Cuckoo-export' '/Users/thomaspickup/Documents/University/CSC3002/Assignment/Malware-Reports'")

print("~~ Sample List Production: Started ~~")
os.system("python compile_samplelist.py '/Users/thomaspickup/documents/university/csc3002/assignment/samples' '/Users/thomaspickup/documents/university/csc3002/assignment/csc3002-project/dataset'")

print("~~ API Results Production: Started ~~")
os.system("python compile_apiresults.py '/Users/thomaspickup/Documents/University/CSC3002/Assignment/Malware-Reports' '/Users/thomaspickup/Documents/University/CSC3002/Assignment/CSC3002-Project/dataset'")