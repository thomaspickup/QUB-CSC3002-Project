import os

print("~~ API Results Retrieval: Started ~~")
<<<<<<< HEAD
os.system("python retrieve_apiresults.py '/Users/thomaspickup/Documents/University/CSC3002/Assignment/Cuckoo-export' '/Users/thomaspickup/Documents/University/CSC3002/Assignment/Malware-Reports'")
=======
os.system("python retrieve_apiresults.py '/Users/thomaspickup/Documents/University/CSC3002/Assignment/Cuckoo-export' '/Users/thomaspickup/Documents/University/CSC3002/Assignment/CSC3002-Project/Malware-Reports'")
>>>>>>> Added test set for testing entire process, made tweeks to scripts

print("~~ Sample List Production: Started ~~")
os.system("python compile_samplelist.py '/Users/thomaspickup/documents/university/csc3002/assignment/samples' '/Users/thomaspickup/documents/university/csc3002/assignment/csc3002-project/dataset'")

print("~~ API Results Production: Started ~~")
os.system("python compile_apiresults.py '/Users/thomaspickup/Documents/University/CSC3002/Assignment/Malware-Reports' '/Users/thomaspickup/Documents/University/CSC3002/Assignment/CSC3002-Project/dataset'")
