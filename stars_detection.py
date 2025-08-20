'''

This script allows to detect objects in a FITS file using the Photutils library in Python.

'''

from astropy.io import fits
from astropy.stats import sigma_clipped_stats
import numpy as np
from photutils.detection import DAOStarFinder
import os

file_name = '2024-09-30_06-42-09_PKS0454-234_V_180.00s_1x1_0_0286_out.fits'
def detect_stars(file_name):

    #Read the FITS file from the current directory
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, file_name)
    hdul = fits.open(file_path)

    #Get the data from the FITS file
    data = hdul[0].data
    header = hdul[0].header
    object_name = header['OBJECT']

    #Close the FITS file
    hdul.close()

    #Calculate the mean, median and standard deviation of the data
    mean, median, std = sigma_clipped_stats(data)

    #Detect sources in the data
    daofind = DAOStarFinder(fwhm=3.0, threshold=5.*std)  
    sources = daofind(data - median) 

    if sources is not None and len(sources) > 10:
        return (object_name, len(sources))
    else:
        return (object_name, 0)
