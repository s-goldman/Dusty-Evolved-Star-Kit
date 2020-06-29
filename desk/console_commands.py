# Steve Goldman, Space Telescope Science Institute, sgoldman@stsci.edu
# from time import time
import ipdb

# from multiprocessing import Value
import numpy as np
from astropy.table import Column
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


def grids():
    # Prints the model grids available for fitting.
    print("\nGrids:")
    for item in config.grids:
        print("\t" + str(item))
    print("\n")


def single_fig():
    plotting_seds.single_figures()


def fit(
    source="desk/put_target_data_here",
    distance=config.fitting["default_distance"],
    grid=config.fitting["default_grid"],
    n=config.fitting["default_number_of_models"],
    min_wavelength=config.fitting["default_wavelength_min"],
    max_wavelength=config.fitting["default_wavelength_max"],
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

    # SET-UP ###################################################################
    # progress tracking
    # start = time()
    # counter = Value("i", 0)

    # get inputs
    user = get_inputs.users(source, distance, grid)

    # remove old / create new output files
    create_output_files.remove_old_output_files()
    create_output_files.make_output_files_dusty()

    # get data filenames
    file_names = get_data.compile_data(source)

    # gets data in array of [source[waves, fluxes], source[waves, fluxes], ...]
    data = [
        get_data.get_values(x, min_wavelength, max_wavelength, fitting=True)
        for x in file_names
    ]

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

    # Fitting ##################################################################
    for i, _ in enumerate(data):
        dusty_fit.fit_single_source(
            file_names[i],
            data[i],
            user,
            model_wavelength_grid,
            full_model_grid,
            full_outputs,
            counter=i + 1,
            number_of_targets=len(data),
        )


def sed():
    plotting_seds.create_fig()


if __name__ == "__main__":
    fit()
