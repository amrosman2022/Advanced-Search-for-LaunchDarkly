# Script file to run all the required files used for the platform. 
import subprocess
import time
import os

# Create the "uploads" directory if it does not exist
uploads_dir = os.path.join('.', 'Backend', 'uploads')
os.makedirs(uploads_dir, exist_ok=True)
print(f"Directory {uploads_dir} created or already exists.")

# Define the commands to run the servers
commands = [
    'python3 -m http.server 9000 --directory ./UI',  # Serve HTML files from a relative directory
    'python3 ./Backend/es_main.py',                        # Run es_main.py
    'python3 ./Backend/upLoadSvr/es_svrUploadCSV.py'                 # Run es_svrUploadCSV.py
]

# Start the processes
processes = []
for command in commands:
    print(f"Starting command: {command}")
    process = subprocess.Popen(command, shell=True)
    processes.append(process)

# Give some time for the servers to start
time.sleep(5)

# Check if all processes are still running
for i, process in enumerate(processes):
    if process.poll() is None:
        print(f"Command {i + 1} is running successfully.")
    else:
        print(f"Command {i + 1} has stopped unexpectedly.")

# Keep the script running to keep the servers alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Shutting down servers...")
    for process in processes:
        process.terminate()
