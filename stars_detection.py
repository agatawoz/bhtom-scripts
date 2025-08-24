'''

This script allows to detect objects in a FITS file using the Photutils library in Python.

'''

from astropy.io import fits
from astropy.stats import sigma_clipped_stats
import numpy as np
from photutils.detection import DAOStarFinder
import os
import yaml

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

    if sources > min_source:
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