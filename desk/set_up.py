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
from astropy.table import Table, Column
from desk.dusty_fit import dusty_fit
from desk.grams_fit import grams_fit
from desk import config, get_remote_models

# Checks if model exists and if it's a csv file or directory of csv files
def check_models(model_grid, full_path):
    """Checks if model grids are available and returns the full path to the model.
    If the model is not downloaded, it is downloaded via Box.

    Parameters
    ----------
    model_grid : str
        Name of model grid to use.
    full_path : str
        full path to desk.

    Returns
    -------
    csv_file: str
        The full path/name of the model outputs file.
    fits_file: str
        The full path/name of the model grid file.

    """
    csv_file = full_path + "models/" + model_grid + "_outputs.csv"
    fits_file = full_path + "models/" + model_grid + "_models.fits"

    # Checks if grid is available
    if os.path.isfile(csv_file) and os.path.isfile(fits_file):
        print("\nYou already have the grid!\n")
    else:
        # asks if you want to download the models
        user_proceed = input("Models not found locally, download the models [y]/n?: ")
        if user_proceed == "y" or user_proceed == "":
            # downloads models
            get_remote_models.get_models(model_grid)
        elif user_proceed == "n":
            raise ValueError("Please make another model selection")
        elif user_proceed != "y" and user_proceed != "n":
            raise ValueError("Invalid selection")
    return (csv_file, fits_file)


def get_model_grid(grid):
    """Gets the real model grid name if the defaults were chosen,
    and runs check models.

    Parameters
    ----------
    grid : str
        Model grid name.

    Returns
    -------
    grid_dusty : 2 column astropy table with array of wavelengths and array of
    fluxes in each column of each row
        The (intial) model grid wavelengths and fluxes. This is not the full model
        grid with appended scaled models.

    grid_outputs : astropy table
        The model grid parameters corresponding to the grid_dusty model grids
    """
    full_path = str(__file__.replace("set_up.py", ""))
    grid_type = copy.copy(grid)

    # create output files
    if fnmatch(grid_type, "grams*"):
        make_output_files_grams()
    else:
        make_output_files_dusty()

    # User input for models
    if grid == "carbon":
        model_grid = "Zubko-Crich-bb"
    elif grid == "oxygen":
        model_grid = "Oss-Orich-bb"
    else:
        if grid in config.grids:
            model_grid = grid
        else:
            raise ValueError(
                "\n\nUnknown grid. Please make another model selection.\n\n To see options use: desk grids\n"
            )
    csv_file_name, fits_file_name = check_models(model_grid, full_path)

    grid_dusty = Table.read(fits_file_name)
    grid_outputs = Table.read(csv_file_name)

    return grid_dusty, grid_outputs, model_grid


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
