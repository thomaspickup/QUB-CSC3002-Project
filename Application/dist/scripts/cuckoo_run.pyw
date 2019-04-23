import os, time

# Runs Cuckoo
os.system('start cmd @cmd /k cuckoo')
time.sleep(10)

# Runs Cuckoo Web
os.system('start cmd @cmd /k cuckoo web')
time.sleep(10)

# Runs Cuckoo API
os.system('start cmd @cmd /k cuckoo api')
time.sleep(10)
