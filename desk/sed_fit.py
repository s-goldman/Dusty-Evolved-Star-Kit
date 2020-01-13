from __future__ import absolute_import

import csv
import glob
import copy
import importlib
import math
import os
import pdb
import time
import functools
from fnmatch import fnmatch
from multiprocessing import Pool, cpu_count
from multiprocessing import Process, Value, cpu_count

import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np
from astropy.io import ascii
from astropy.table import Table, Column
from desk import config, plotting_seds, get_remote_models, parameter_ranges
from desk.dusty_fit import dusty_fit
from desk.grams_fit import grams_fit

from matplotlib import rc
from scipy import interpolate

importlib.reload(config)

"""
Steve Goldman
Space Telescope Science Institute
Nov 16, 2018
sgoldman@stsci.edu

This package takes a photometry or a spectrum (or spectra) in csv format and fits it/them with a grid of models.
The grids used here are converted from output from the DUSTY code (Elitzur & Ivezic 2001, MNRAS, 327, 403) using
the other script dusty_to_grid.py. The code interpolates and trims a version of the data and calculates the least
squares value for each grid in the model and the data. The DUSTY outputs are then scaled and returned in files:
fitting_results.csv and fitting_plotting_output.csv (for plotting the results). An example plotting script has also
been provided.
"""


def grids():
    print("\nGrids:")
    for item in config.grids:
        print("\t" + str(item))
    print("\n")


def get_model(grid_name, teff_new, tinner_new, tau_new):
    desk.interpolate_dusty(
        grid_name, float(teff_new), float(tinner_new), float(tau_new)
    )


def check_models(model_grid, full_path):
    csv_file = full_path + "models/" + model_grid + "_outputs.csv"
    fits_file = full_path + "models/" + model_grid + "_models.fits"
    if os.path.isfile(csv_file) and os.path.isfile(fits_file):
        print("\nYou already have the grid!\n")
        # print("Great job")

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
    """
    :param filename: filename of input data. Should be csv with Column 0: wavelength in um and Col 1: flux in Jy
    :return: two arrays of wavelength (x) and flux (y) in unit specified in config.py
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
    """
    :param target_wave: Target wavelength in um
    :param model_wave: model wavelength in um
    :return: a 1-D array of the closest data wavelength values, to the model wavelength values
    """
    idx = np.searchsorted(model_wave[0], target_wave[0])
    idx = np.clip(idx, 1, len(model_wave[0]) - 1)
    left = model_wave[0][idx - 1]
    right = model_wave[0][idx]
    idx -= target_wave[0] - left < right - target_wave[0]
    closest_data_flux = model_wave[1][idx]
    return closest_data_flux


def least2(data, model_l2):
    return np.nansum(np.square(model_l2 - data))


def trim(data, model_trim):
    """
    :param data: input data in tuple of x and y arrays
    :param model_trim: input model
    :return: trims motimedel to wavelength range of data
    """
    indexes = np.where(
        np.logical_and(
            model_trim[0] >= np.min(data[0]), model_trim[0] <= np.max(data[0])
        )
    )
    return np.vstack([model_trim[0][indexes], model_trim[1][indexes]])


def fit_norm(data, norm_model):
    """
    :param data: input data in tuple of x and y arrays
    :param norm_model: closest wavelength values to data in 1-D array (from trim)
    :return: trimmed model in 2 column np.array
    """
    stats = []
    # normalization range
    # trials = np.linspace(config.fitting['min_norm'], config.fitting['max_norm'], config.fitting['ntrials'])
    trials = np.logspace(
        log_average_flux_wm2 - 2,
        log_average_flux_wm2 + 2,
        config.fitting["number_of_tries"],
    )
    for t in trials:
        stat = least2(data[1], norm_model * t)
        stats.append(stat)
    return stats, trials


# for each target, fit spectra with given models (.fits file)
def sed_fitting(
    source, distance, model_grid, grid_dusty, grid_outputs, counter, number_of_targets
):
    if fnmatch(model_grid, "grams*"):
        grams_fit(
            source,
            distance,
            model_grid,
            grid_dusty,
            grid_outputs,
            counter,
            number_of_targets,
        )
    else:
        dusty_fit(
            source,
            distance,
            model_grid,
            grid_dusty,
            grid_outputs,
            counter,
            number_of_targets,
        )


def fit(
    source="default",
    distance=config.target["distance_in_kpc"],
    grid=config.fitting["model_grid"],
):
    """
    :param source: Name of target in array of strings (or one string)
    :param distance: distance to source(s) in kiloparsecs
    :param grid: Name of model grid
    :return:
    """
    # set variables
    start = time.time()
    counter = Value("i", 0)
    # normalization calculation
    # solar constant = 1379 W
    # distance to sun in kpc 4.8483E-9
    full_path = str(__file__.replace("sed_fit.py", ""))

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

    # check if models exist
    csv_file, fits_file = check_models(model_grid, full_path)

    # gets models
    grid_dusty = Table.read(fits_file)
    grid_outputs = Table.read(csv_file)

    # Model grid equal lengths check
    if len(grid_dusty) == len(grid_outputs):
        pass
    else:
        raise ValueError(
            "Model grid input error: mismatch in model spectra and model output"
        )

    # SED FITTING ###############################
    if fnmatch(source, "*.csv"):
        number_of_targets = 1
        sed_fitting(
            source,
            distance,
            model_grid,
            grid_dusty,
            grid_outputs,
            counter,
            number_of_targets,
        )
    elif os.path.isdir(source):
        source_dir = (source + "/").replace("//", "/")
        if glob.glob(source_dir + "/*.csv"):
            files = glob.glob(source + "/" + "*.csv")
            number_of_targets = len(files)
            # with Pool(processes=cpu_count() - 1) as pool:
            #     pool.map(sed_fitting, [target_string for target_string in files])
            for target_string in files:
                sed_fitting(
                    target_string,
                    distance,
                    model_grid,
                    grid_dusty,
                    grid_outputs,
                    counter,
                    number_of_targets,
                )
        else:
            raise ValueError(
                "\n\n\nERROR: No .csv files in that directory. Please make another selection.\n\n"
            )
    else:
        raise ValueError(
            "\n\n\nError: Not a .csv file. Please make another selection.\n\n"
        )

    # creating figures
    if config.output["create_figure"] == "yes":
        print("\n. . . Creating SED figure . . . . . . . . . . . .")
        plotting_seds.create_fig()  # runs plotting script
    else:
        print(
            "No figure created. To automatically generate a figure change the "
            + '"create_figure" variable in the config.py script to "yes".'
        )

    if not os.path.isfile("parameter_ranges_" + config.fitting["model_grid"] + ".png"):
        print(". . . Creating parameter range figure . . . . . .")
        parameter_ranges.create_par()

    end = time.time()
    print()
    print("Time: " + str("%.2f" % float((end - start) / 60)) + " minutes")


if __name__ == "__main__":
    fit()
