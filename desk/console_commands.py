# Steve Goldman, Space Telescope Science Institute, sgoldman@stsci.edu
# from time import time
import ipdb
import pkg_resources

from multiprocessing import Pool, cpu_count
from functools import partial
import numpy as np
from desk.set_up import (
    get_inputs,
    get_data,
    create_output_files,
    get_models,
    config,
    create_full_grid,
)
from desk.fitting import dusty_fit
from desk.outputs import plotting_seds

desk_path = str(__file__.replace("console_commands.py", ""))


def grids():
    """Prints the model grids available for fitting.

    """
    print("\nGrids:")
    for item in config.grids:
        print("\t" + str(item))
    print("\n")


def version():
    """Returns DESK version.
    """
    print("\n\tDESK version: " + pkg_resources.get_distribution("desk").version + "\n")


def sed():
    """Creates single SED figure of all fit SEDs using
    the 'fitting_results.csv' file.

    Returns
    -------
    png

    """
    plotting_seds.create_fig()


def single_fig():
    """Creates an individual SED figure for each fit SED using the
    results in the 'fitting_results.csv' file.

    Returns
    -------
    multiple pngs

    """
    plotting_seds.single_figures()


def fit(
    source=desk_path + "put_target_data_here",
    distance=config.fitting["default_distance"],
    grid=config.fitting["default_grid"],
    n=config.fitting["default_number_of_times_to_scale_models"],
    min_wavelength=config.fitting["default_wavelength_min"],
    max_wavelength=config.fitting["default_wavelength_max"],
    multiprocessing=True,
    testing=False,
):
    """
    Fits the seds of sources with specified grid.


    Parameters
    ----------
    source : str
        Name of target in array of strings (or one string).
    distance : float
        Distance to source(s) in kiloparsecs.
    grid : str
        Name of model grid.
    """

    # Set-up ###################################################################
    bayesian_fit = False

    # get data filenames
    file_names = get_data.compile_data(source)

    # remove old / create new output files
    create_output_files.remove_old_output_files()
    create_output_files.make_output_files_dusty()

    # gets models
    grid_dusty, grid_outputs = get_models.get_model_grid(grid, testing)

    # does not scale nanni or grams models
    if grid in config.nanni_grids:
        full_model_grid = grid_dusty
        full_outputs = grid_outputs
        full_outputs.rename_columns(
            ["L", "vexp", "dmdt_ir"], ["lum", "scaled_vexp", "scaled_mdot"]
        )

    # elif grid in config.grams_grids:
    #     full_model_grid = grid_dusty
    #     full_outputs = grid_outputs
    #     full_model_grid.rename_columns(["LSPEC"], ["col0"])
    #     full_outputs.rename_columns(["mdot"], ["scaled_mdot"])
    #
    #     # does not calculate expansion velocity so set as 0
    #     full_outputs.add_column(Column([0] * len(full_outputs), name="scaled_vexp"))

    else:
        # update ids to number in grid
        grid_outputs["number"] = np.arange(0, len(grid_outputs))

        # create scaling factors for larger model grid
        scaling_factors = create_full_grid.generate_scaling_factors(distance, int(n))

        # create larger grid by scaling and appending current grid
        full_outputs = create_full_grid.create_full_outputs(
            grid_outputs, distance, scaling_factors
        )
        full_model_grid = create_full_grid.create_full_model_grid(
            grid_dusty, scaling_factors
        )
        full_outputs.remove_columns(["vexp", "mdot"])

    # get model wavelengths
    model_wavelength_grid = grid_dusty["col0"][0]

    # initialize fitting parameters
    fit_params = get_inputs.fitting_parameters(
        file_names,
        source,
        distance,
        grid,
        n,
        model_wavelength_grid,
        full_model_grid,
        full_outputs,
        min_wavelength,
        max_wavelength,
        bayesian_fit,
        testing,
    )

    if multiprocessing == True:
        # Multi-core fitting
        pool = Pool(processes=cpu_count() - 1)
        mapfunc = partial(dusty_fit.fit_single_source, fit_params=fit_params)
        pool.map(mapfunc, range(len(file_names)))
    else:
        # Single-core fitting
        [dusty_fit.fit_single_source(x, fit_params) for x in range(len(file_names))]

    # creates sed figure
    plotting_seds.create_fig()


if __name__ == "__main__":
    fit()
