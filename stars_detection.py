from astropy.io import fits
from astropy.stats import sigma_clipped_stats
import numpy as np
from photutils.detection import DAOStarFinder
import os

#Read the FITS file from the current directory
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, 'test.fits')
hdul = fits.open(file_path)

#Get the data from the FITS file
data = hdul[0].data

#Close the FITS file
hdul.close()

#Calculate the mean, median, and standard deviation of the data
mean, median, std = sigma_clipped_stats(data)

#Detect sources in the data
daofind = DAOStarFinder(fwhm=3.0, threshold=5.*std)  
sources = daofind(data - median) 

if sources is not None and len(sources) > 0:
    print(f" {len(sources)} stars decetcted.")
else:
    print("No stars decected")
