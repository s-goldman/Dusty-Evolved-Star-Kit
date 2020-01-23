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
from astropy.table import Table, Column
from multiprocessing import Value
from desk import config, plotting_seds, get_remote_models
from desk import parameter_ranges, fitting_tools, interpolate_dusty

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

    # set variables
    grid_type = copy.copy(grid)
    start = time.time()
    counter = Value("i", 0)
    # normalization calculation
    # solar constant = 1379 W
    # distance to sun in kpc 4.8483E-9
    full_path = str(__file__.replace("console_commands.py", ""))

    # create output files
    if fnmatch(grid_type, "grams*"):
        fitting_tools.make_output_files_grams()
    else:
        fitting_tools.make_output_files_dusty()

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
    csv_file, fits_file = fitting_tools.check_models(model_grid, full_path)

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
        return fitting_tools.sed_fitting(
            model_grid,
            source,
            distance,
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
