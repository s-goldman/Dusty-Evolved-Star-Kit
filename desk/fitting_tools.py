# Steve Goldman, Space Telescope Science Institute, sgoldman@stsci.edu
import os
import sys
import copy
import glob
import time
import ipdb
import math
import numpy as np
import astropy.units as u
from astropy.io import ascii
from fnmatch import fnmatch
from desk.dusty_fit import dusty_fit
from desk.grams_fit import grams_fit
from desk import config, get_remote_models

# Checks if model exists and if it's a csv file or directory of csv files
def check_models(model_grid, full_path):
    csv_file = full_path + "models/" + model_grid + "_outputs.csv"
    fits_file = full_path + "models/" + model_grid + "_models.fits"
    if os.path.isfile(csv_file) and os.path.isfile(fits_file):
        print("\nYou already have the grid!\n")
    else:
        user_proceed = input("Models not found locally, download the models [y]/n?: ")
        if user_proceed == "y" or user_proceed == "":
            get_remote_models.get_models(model_grid)
        elif user_proceed == "n":
            raise ValueError("Please make another model selection")
        elif user_proceed != "y" and user_proceed != "n":
            raise ValueError("Invalid selection")
    return (csv_file, fits_file)


def get_data(filename):
    """Retrieves data by reading csv file.

    Parameters
    ----------
    filename : str
        Name of csv file name. The file should have:
            Column 0: wavelength in um
            Column 1: flux in Jy

    Returns
    -------
    2 arrays
        wavelength (x) and flux (y) in unit specified in config.py (default is w/m2)

    """
    global log_average_flux_wm2
    table = ascii.read(filename, delimiter=",")
    table.sort(table.colnames[0])
    x = np.array(table.columns[0])
    y = np.array(table.columns[1])
    index = np.where(
        (x > config.fitting["wavelength_min"]) & (x < config.fitting["wavelength_max"])
    )
    x = x[index]
    y = y[index]
    y = y * u.Jy
    y = y.to(u.W / (u.m * u.m), equivalencies=u.spectral_density(x * u.um))
    log_average_flux_wm2 = np.log10(np.median(y).value)
    return x, np.array(y)


def create_trials(y_flux_array, distance):
    """Creates arrays of model fluxes normalize to +/- 2.

    Parameters
    ----------
    y_flux_array : array
        The flux of the model in w/m2.

    Returns
    -------
    array
        An array of model flux arrays for each normalized value

    """
    distance_norm = math.log10(((float(distance) / 4.8482e-9) ** 2) / 1379)
    lum_min = 10000  # solar luminosities
    lum_max = 200000
    trials = (
        np.linspace(
            np.log10(lum_min), np.log10(lum_max), config.fitting["number_of_tries"]
        )
        - distance_norm
    )
    return trials


def remove_old_output_files():
    if os.path.exists("fitting_results.txt"):
        os.remove("fitting_results.txt")
    if os.path.exists("fitting_plotting_outputs.txt"):
        os.remove("fitting_plotting_outputs.txt")


def make_output_files_dusty():
    remove_old_output_files()
    with open("fitting_results.csv", "w") as f:
        f.write("source,L,vexp_predicted,teff,tinner,odep,mdot\n")
        f.close()
    with open("fitting_plotting_outputs.csv", "w") as f:
        f.write("target_name,data_file,norm,index,grid_name,teff,tinner,odep\n")
        f.close()


def make_output_files_grams():
    remove_old_output_files()
    with open("fitting_results.csv", "w") as f:
        f.write("source,L,rin,teff,tinner,odep,mdot\n")
        f.close()
    with open("fitting_plotting_outputs.csv", "w") as f:
        f.write("target_name,data_file,norm,index,grid_name,teff,tinner,odep\n")
        f.close()


# for each target, fit spectra with given models (.fits file)
def sed_fitting(model_grid, *args, **kargs):
    # passes arguments to either dusty_fit or grams_fit
    if fnmatch(model_grid, "grams*"):
        raise ValueError("\n\n\n ***Currently Unavailble*** \n")
        # return grams_fit(model_grid, *args, **kargs)
    else:
        return dusty_fit(model_grid, *args, **kargs)
