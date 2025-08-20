import subprocess
import argparse
import os
from stars_detection import detect_stars
from logs import send_log
import filter

log_path = 'log.txt'

print('Starting sending data to BHTOM')

parser = argparse.ArgumentParser(description="Process some parameters.")
parser.add_argument('--directory_path', default=None, help='The directory containing fits files')
directory_path = args.directory_path

#unzipping all files
subprocess.run(["bash", "unzip_files.sh", directory_path])

for file in os.listdir(directory_path):
    if file.endswith(".fits"):
        object_name, result = detect_stars(directory_path, file) #check if files contains targets and returns object name 
        send_log(object_name, file, result, log_path) #send log


