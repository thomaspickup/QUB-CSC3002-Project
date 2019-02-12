import os

print("~~ Sample List Production: Started ~~")
os.system("python compile_samplelist.py '/Users/thomaspickup/documents/university/csc3002/assignment/samples' '/Users/thomaspickup/documents/university/csc3002/assignment/csc3002-project/dataset'")

print("~~ API Results Production: Started ~~")
os.system("python compile_apiresults.py")
