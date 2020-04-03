# Steve Goldman, Space Telescope Science Institute, sgoldman@stsci.edu
from time import time
import ipdb
import numpy as np
from multiprocessing import Value
from desk.set_up import (
    get_inputs,
    get_data,
    create_output_files,
    get_models,
    config,
    create_full_grid,
)
from desk.fitting import dusty_fit


# Non-fitting commands #########################################################
def grids():
    # Prints the model grids available for fitting.
    print("\nGrids:")
    for item in config.grids:
        print("\t" + str(item))
    print("\n")


def fit(source="desk/put_target_data_here", distance=50, grid="Oss-Orich-bb"):
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

    # SET-UP ###################################################################
    # progress tracking
    start = time()
    counter = Value("i", 0)

    # get inputs
    user = get_inputs.users(source, distance, grid)

    # remove old / create new output files
    create_output_files.remove_old_output_files()
    create_output_files.make_output_files_dusty()

    # get data filenames
    file_names, n_sources = get_data.compile_data(source)

    # gets data in array of [source[waves, fluxes], source[waves, fluxes], ...]
    data = [get_data.get_values(x) for x in file_names]

    # gets models
    grid_dusty, grid_outputs, model_grid = get_models.get_model_grid(grid)

    # create scaling factors for larger model grid
    scaling_factors = create_full_grid.generate_scaling_factors(distance)

    # create larger grid by scaling and appending current grid
    model_wavelength_grid = grid_dusty["col0"][0]
    full_outputs = create_full_grid.create_full_outputs(
        grid_outputs, distance, scaling_factors
    )
    full_model_grid = create_full_grid.create_full_model_grid(
        grid_dusty, scaling_factors
    )

    # Fitting ##################################################################
    dusty_fit.fit_single_source(
        file_names[0],
        data[0],
        user,
        model_wavelength_grid,
        full_model_grid,
        full_outputs,
        counter=1,
        number_of_targets=3,
    )


if __name__ == "__main__":
    fit()
