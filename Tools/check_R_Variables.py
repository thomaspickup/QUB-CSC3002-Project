import os

# Current R Path is shown below
rPath = r"C:\Program Files\R\R-3.5.3patched\bin"
envPath = os.getenv("PATH")

# If its not contained in the system variable - add it
if rPath not in envPath:
    # Adds to system variable PATH
    os.environ["PATH"] = envPath + ";" + rPath
    print("- Adding R to system path")
