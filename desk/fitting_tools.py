# Steve Goldman, Space Telescope Science Institute, sgoldman@stsci.edu
import os
import sys
import copy
import glob
import time
import ipdb
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


def find_closest(target_wave, model_wave):
    """Find values model values corresponding to the closest values in the data

    Parameters
    ----------
    target_wave : 1-D array
        Target wavelength in um.
    model_wave : 1-D array
        model wavelength in um.

    Returns
    -------
    array
        Array of the closest data wavelength values, to the model wavelength values.

    """
    idx = np.searchsorted(model_wave[0], target_wave[0])
    idx = np.clip(idx, 1, len(model_wave[0]) - 1)
    left = model_wave[0][idx - 1]
    right = model_wave[0][idx]
    idx -= target_wave[0] - left < right - target_wave[0]
    closest_data_flux = model_wave[1][idx]
    return closest_data_flux


def least2(data, model_l2):
    # least squares fit
    return np.nansum(np.square(model_l2 - data))


def trim(data, model_trim):
    """Removes data outside of wavelegth range of model grid.

    Parameters
    ----------
    data : 2-D array
        input data in 2-D array of wavelength and flux.
    model_trim : type
        input model in 2-D array of wavelength and flux.

    Returns
    -------
    2-D array
        Trimmed input model in 2-D array of wavelength and flux.

    """
    indexes = np.where(
        np.logical_and(
            model_trim[0] >= np.min(data[0]), model_trim[0] <= np.max(data[0])
        )
    )
    return np.vstack([model_trim[0][indexes], model_trim[1][indexes]])


def create_trials(y_flux_array):
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
    log_average_flux_wm2 = np.log10(np.median(y_flux_array))
    trials = np.logspace(
        log_average_flux_wm2 - 2,
        log_average_flux_wm2 + 2,
        config.fitting["number_of_tries"],
    )
    return trials


def fit_norm(data, norm_model, trials):
    """Short summary.

    Parameters
    ----------
    data : tuple
        input data in tuple of x and y arrays.
    norm_model : 1D array
        closest wavelength values from trim.
    trials : array
        least sqaures value for each model fit at each normalization.

    Returns
    -------
    type
        Description of returned object.

    """
    # normalization range
    stats = [least2(data[1], norm_model * x) for x in trials]
    return stats


def trim_find_lsq(model, raw_data, trials):
    """Uses other functions to trim the data, find the closest match, and try
    a range of normalization values.

    Parameters
    ----------
    model : astropy row of two arrays
        Astropy row with the first column containing an array of the model
        wavelegnths in microns. The second column is the model flux in w*m^-2.
    raw_data : 2D array
        First array is wavelength of data in microns, second array is the flux
        in w*m^-2.
    trials : type
        An array of normalization factors spaced +/-2 of the log_average_flux_wm2.

    Returns
    -------
    type array
        array of least sqaures value for each model fit at each normalization

    """
    # removes data outside of wavelegth range of model grid
    trimmed_model = trim(raw_data, model)

    # gets fluxes for corresponding wavelengths of data and models
    matched_model = find_closest(raw_data, trimmed_model)

    # fits source with n(set in config) models spanning 4 orders of magnitude
    stats = fit_norm(raw_data, matched_model, trials)
    return stats


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
        return grams_fit(model_grid, *args, **kargs)
    else:
        return dusty_fit(model_grid, *args, **kargs)
