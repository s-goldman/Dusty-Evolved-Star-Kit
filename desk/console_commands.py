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
from copy import deepcopy
from astropy.table import Table, Column
from multiprocessing import Value
from create_full_grid import *
from dusty_fit import *
from desk import config, plotting_seds, get_remote_models
from desk import parameter_ranges, set_up, interpolate_dusty

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
    interpolate_dusty.interpolate(
        grid_name, float(teff_new), float(tinner_new), float(tau_new)
    )


def single_fig():
    plotting_seds.single_figures()


def fit(
    source="desk/put_target_data_here",
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

    # progress tracking
    start = time.time()
    counter = Value("i", 0)

    # gets models
    grid_dusty, grid_outputs, model_grid = set_up.get_model_grid(grid)

    # get full grids
    trials = create_trials(distance)
    wavelength_grid = grid_dusty["col0"][0]
    full_outputs = create_full_outputs(deepcopy(grid_outputs), distance, trials)
    full_model_grid = create_full_model_grid(grid_dusty, trials)

    def add_variables(source):
        pass

    # run SED fitting on csv or directory of csvs
    if fnmatch(source, "*.csv"):
        number_of_targets = 1
        best_model = dusty_fit(
            source,
            distance,
            model_grid,
            wavelength_grid,
            full_model_grid,
            full_outputs,
            grid_outputs,
            counter,
            number_of_targets,
        )

    elif os.path.isdir(source):
        source_dir = (source + "/").replace("//", "/")  # if input dir ends in /
        if glob.glob(source_dir + "/*.csv"):
            files = glob.glob(source + "/" + "*.csv")
            number_of_targets = len(files)
            for target_string in files:
                best_model = dusty_fit(
                    target_string,
                    distance,
                    model_grid,
                    wavelength_grid,
                    full_model_grid,
                    full_outputs,
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
