# Steve Goldman, Space Telescope Science Institute, sgoldman@stsci.edu
import os
import copy
import glob
import time
import ipdb
import importlib
import numpy as np
import astropy.units as u
from fnmatch import fnmatch
from astropy.io import ascii
from desk.dusty_fit import dusty_fit
from desk.grams_fit import grams_fit
from desk.interpolate_dusty import interpolate_dusty
from astropy.table import Table, Column
from multiprocessing import Value
from desk import config, plotting_seds, get_remote_models, parameter_ranges

importlib.reload(config)

# Non-fitting commands #########################################################
def grids():
    # Prints the model grids available for fitting.
    print("\nGrids:")
    for item in config.grids:
        print("\t" + str(item))
    print("\n")


# returns interpolate model as csv for any model grid
def get_model(grid_name, teff_new, tinner_new, tau_new):
    interpolate_dusty(grid_name, float(teff_new), float(tinner_new), float(tau_new))


################################################################################

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
    """
    :param data: input data in tuple of x and y arrays
    :param norm_model: closest wavelength values to data in 1-D array (from trim)
    :return: trimmed model in 2 column np.array
    """
    # normalization range
    stats = [least2(data[1], norm_model * x) for x in trials]
    return stats


# for each target, fit spectra with given models (.fits file)
def sed_fitting(*args, **kargs):
    # passes arguments to either dusty_fit or grams_fit
    if fnmatch(grid_type, "grams*"):
        return grams_fit(*args ** kargs)
    else:
        return dusty_fit(*args, **kargs)


def fit(
    source="carbon",
    distance=config.target["distance_in_kpc"],
    grid=config.fitting["model_grid"],
):
    """Fits the seds of sources with specified grid.

    Parameters
    ----------
    source : str
        Name of target in array of strings (or one string).
    distance : float
        Distance to source(s) in kiloparsecs.
    grid : str
        Name of model grid.

    """

    # set variables
    global grid_type
    grid_type = copy.copy(grid)
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
    def add_variables(source):
        return sed_fitting(
            source,
            distance,
            model_grid,
            grid_dusty,
            grid_outputs,
            counter,
            number_of_targets,
        )

    if fnmatch(source, "*.csv"):
        number_of_targets = 1
        add_variables(source)
    elif os.path.isdir(source):
        source_dir = (source + "/").replace("//", "/")
        if glob.glob(source_dir + "/*.csv"):
            files = glob.glob(source + "/" + "*.csv")
            number_of_targets = len(files)
            # with Pool(processes=cpu_count() - 1) as pool:
            #     pool.map(sed_fitting, [target_string for target_string in files])

            for target_string in files:
                add_variables(target_string)
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
