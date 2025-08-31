import os
import subprocess
import argparse
import requests
from astropy.io import fits
from astropy.stats import sigma_clipped_stats
import numpy as np
from photutils.detection import DAOStarFinder
import yaml
import datetime
import re

log_path = 'log.txt'
observatory_name = 'UZPW50_Chile_QHY268PRO'


def upload_to_bhtom(file_path, token, target_name, filter_name, observatory_name):
    
    url = 'https://uploadsvc2.astrolabs.pl/upload/'

    with open(file_path, 'rb') as f:
        data = {
            'target': target_name,
            'filter': filter_name,
            'data_product_type': 'fits_file',
            'dry_run': 'False',
            'observatory': observatory_name
        }

        headers = {
            'Authorization': f'Token {token}'
        }

        response = requests.post(
            url=url,
            headers=headers,
            data=data,
            files={'files': f}
        )

    return response.json()

def detect_stars(file_path, min_source=10):

    #get the data from the FITS file
    with fits.open(file_path) as hdul:
        data = hdul[0].data
        header = hdul[0].header

    object_name = header.get('OBJECT', 'Unknown')

    #calculate the mean, median and standard deviation of the data
    mean, median, std = sigma_clipped_stats(data)

    #detect sources in the data
    daofind = DAOStarFinder(fwhm=3.0, threshold=5.*std)  
    sources = daofind(data - median) 

    if sources is not None and len(sources) > min_source:
        return (object_name, len(sources))
    else:
        return (object_name, 0)


def rotuz_to_bhtom_name(rotuz_name, file="bhtom_objects.yaml"):
    try:
        with open(file) as f:
            names = yaml.safe_load(f)
            print(f)
            return names.get(rotuz_name, rotuz_name)
    except FileNotFoundError:
        print(f"File '{file}' not found.")
        return None



def send_log(object_name, file_name, result, log_file):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    detected = "yes" if result else "no"
    log = f"[{time}] Object: {object_name} | File name: {file_name} | Detected: {detected}\n"


    with open(log_file, "a") as f:
        f.write(log)


filters = {"_B_" : "GaiaSP/B", "_V_" : "GaiaSP/V", "_R_" : "GaiaSP/R", "_U_" : "GaiaSP/I", "_I_" : "GaiaSP/I", 
        "_rs_" : "GaiaSP/r", "_gs_" : "GaiaSP/g", "_is_" : "GaiaSP/i", "_us_" : "GaiaSP/u", "_zs_" : "GaiaSP/z",
        " " : "GaiaSP/any"}

def get_filter(file):
    match = re.search(r'_([A-Za-z])_', file)
    if match:
        return match.group(0)
    else:
        return None

def BHTOM_filter(filter):
    return filters.get(filter)


def main():
    print('Starting sending data to BHTOM')
    parser = argparse.ArgumentParser(description="Process some parameters.")
    parser.add_argument('--token', default=None, help='Your BHTOM token')
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
