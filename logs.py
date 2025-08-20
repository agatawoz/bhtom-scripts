"""

This script creates logs after start detection of objects in FITS file.

"""
import datetime

def send_log(object_name, file_name, result, log_file):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    detected = "yes" if result else "no"
    log = f"[{time}] Object: {object_name} | File name: {file_name} | Detected: {detected}\n"


    with open(log_file, "a") as f:
        f.write(log)

