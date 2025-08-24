import subprocess
import argparse
import os
from stars_detection import detect_stars, rotuz_to_bhtom_name
from logs import send_log
import filters_tools.py
from send_data import upload_to_BHTOM

log_path = 'log.txt'
observatory_name = 'UZPW50_Chile_QHY268PRO'

def main():
    print('Starting sending data to BHTOM')
    parser = argparse.ArgumentParser(description="Process some parameters.")
    parseer.add_argument('--token', default=None, help='Your BHTOM token')
    parser.add_argument('--directory_path', default=None, help='The directory containing fits files')

    args = parser.parse_args()
    directory_path = args.directory_path
    token = args.token

    if not os.path.exists(directory_path):
        print(f"Directory '{directory_path}' does not exist.")
        exit(1)

    if token is None:
        print("Please provide a token.")
        exit(1)


    #unzipping all files
    subprocess.run(["bash", "unzip_files.sh", directory_path])

    processed = 0
    uploaded = 0

    for file in os.listdir(directory_path):
        if file.endswith(".fits"):
            full_path = os.path.join(directory_path, file)
            filter_name = BHTOM_filter(file)
            object_name, result = detect_stars(full_path, file) #check if files contains targets and returns object name 
            bhtom_name = rotuz_to_bhtom_name(object_name) #mappinng from rotuz to bhtom
            send_log(object_name, file, result, log_path) #send log
            processed += 1
            if result:
                upload_to_BHTOM(full_path, token, bhtom_name, filter_name, observatory_name)#send file to bhtom
                uploaded += 1

    print(f"Processed {processed} files, uploaded {uploaded}.")


if __name__ == "__main__":
    main()
