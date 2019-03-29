import os, subprocess

dataset_production_run = raw_input("Produce new dataset (Y/N):")
model_production_run = raw_input("Produce new model (Y/N):")

if (dataset_production_run == 'Y' or dataset_production_run == 'y'):
    print("%% Starting Dataset Production %%")
    os.system("python Parser/compile_dataset.py")

if (model_production_run == 'Y' or model_production_run == 'y'):
    print("%% Starting Model Production %%")
    subprocess.Popen([r"C:\Program Files\R\R-3.5.3patched\bin\rscript.exe",r"MachineLearning\MachineLearningScript.R"])
