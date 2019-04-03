import os, time

# Runs Cuckoo Bash to start up bash side
os.system('start bash cuckoo_run_bash.sh')
time.sleep(10)

# Runs Cuckoo
os.system('start cmd @cmd /k cuckoo')
time.sleep(10)

# Runs Cuckoo Web
os.system('start cmd @cmd /k cuckoo web')
time.sleep(10)

# Runs Cuckoo API
os.system('start cmd @cmd /k cuckoo api')
time.sleep(10)

# Starts up Web Browser
os.system('start http://localhost:8000')
