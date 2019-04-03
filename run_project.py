import os, datetime

# Prints debugging and start time
print("==== Running Project ====")
startDateTime = datetime.datetime.now()
print("Started Project at " + str(startDateTime) + "\n")

# Asks the runner what parts of the project they want to run
dataset_production_run = raw_input("Produce new dataset (Y/N): ")
model_production_run = raw_input("Produce new model (Y/N): ")
model_evaluation_run = raw_input("Run Product (Y/N): ")

if (dataset_production_run == 'Y' or dataset_production_run == 'y'):
    # Runs dataset compilation script
    print("\n%% Starting Dataset Production %%")
    os.system("python Parser/compile_dataset.py")
    print("%% Finished Dataset Production %%\n")

if (model_production_run == 'Y' or model_production_run == 'y'):
    # Runs Model Creation Script
    print("\n%% Starting Model Production %%")
    os.system("python Tools/check_R_variables.py")
    os.system(r"rscript C:\Users\thomaspickup\iCloudDrive\Documents\University\CSC3002\Assignment\CSC3002-Project\MachineLearning\Model_Creation_Script.R")
    os.system("python Parser/print_accuracy.py")
    print("%% Finished Model Production %%\n")

if (model_evaluation_run == 'Y' or model_evaluation_run == 'y'):
    os.system("python Production/product.py")

# Prints debugging to say finished time and completed project
endDateTime = datetime.datetime.now()
deltaDateTime = endDateTime - startDateTime
print("Finished Project at " + str(endDateTime))
print("Total Time Taken: " + str(deltaDateTime))
print("==== Completed Project ====")
