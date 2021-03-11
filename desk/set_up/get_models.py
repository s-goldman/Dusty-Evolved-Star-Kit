# Steve Goldman, Space Telescope Science Institute, sgoldman@stsci.edu
import os
import ipdb
import numpy as np
import h5py
from shutil import copyfile
from astropy.table import Table, Column
from astropy.utils.data import download_file
from desk.set_up import config


def read_hdf5(filename, testing):
    """Reads HDF5 file.

    Parameters
    ----------
    filename : str
        name of the file to be read including the full path.
    testing : str
        If testing flag enabled, the function will only return the
        first couple columns of the table.

    Returns
    -------
    out: astropy table
        contents of table at filename.

    """
    with h5py.File(filename, "r") as f:
        key = list(f.keys())[0]
        if (testing == True) | (testing == "True"):
            data = list(f[key][0:3])
        else:
            data = list(f[key])
    out = Table(np.array(data))
    return out


def get_remote_models(model_grid_name):
    """Downloads models and model results files (HDF5) from BOX.

    Parameters
    ----------
    model_grid_name : str
        Name of model grid to download.

    """
    # update if zeonodo repository updated
    repository = 4574453

    fname_dld_outputs = download_file(
        "https://zenodo.org/record/"
        + str(repository)
        + "/files/"
        + model_grid_name
        + "_outputs.hdf5?download=1"
    )
    fname_dld_models = download_file(
        "https://zenodo.org/record/"
        + str(repository)
        + "/files/"
        + model_grid_name
        + "_models.hdf5?download=1"
    )

    copyfile(
        fname_dld_outputs, config.path + "models/" + model_grid_name + "_outputs.hdf5"
    )
    copyfile(
        fname_dld_models, config.path + "models/" + model_grid_name + "_models.hdf5"
    )
    # \n Padova options: J400, J1000, H11, R12, R13'


def check_models(model_grid, size_filename="desk_model_grid_sizes.csv"):

    """
    Checks if model grids are available and returns the full path to the model.
    If the model is not downloaded, it is downloaded via Box.

    Parameters
    ----------
    model_grid : str
        Name of model grid to use.

    Returns
    -------
    outputs_file: str
        The full path/name of the model outputs file.
    models_file: str
        The full path/name of the model grid file.

    """

    outputs_file = config.path + "models/" + model_grid + "_outputs.hdf5"
    models_file = config.path + "models/" + model_grid + "_models.hdf5"

    # Checks if grid is available
    if os.path.isfile(outputs_file) and os.path.isfile(models_file):
        print("\nYou already have the grid!\n")

    else:
        # asks if you want to download the models
        print("Models not found locally")
        get_remote_models(model_grid)
    return (outputs_file, models_file)


def get_model_grid(grid, testing=False):
    """
    Gets the real model grid name if the defaults were chosen,and runs check_models.

    Parameters
    ----------
    grid : str
        Model grid name.
    testing: str
        Flag for testing that returns small grid (3 rows)

    Returns
    -------
    grid_dusty : 2 column astropy table with array of wavelengths (um) and array of
    fluxes (Wm^2) in each column of each row. The (intial) model grid wavelengths and fluxes.
    This is not the full model grid with appended scaled models.

    grid_outputs : astropy table
        The model grid parameters corresponding to the grid_dusty model grids
    """

    # User input for models
    if grid == "carbon":
        model_grid = "Zubko-Crich-bb"
    elif grid == "oxygen":
        model_grid = "Oss-Orich-bb"
    else:
        if (grid in config.grids) | (grid in config.external_grids):
            model_grid = grid
        else:
            raise ValueError(
                "\n\nUnknown grid. Please make another model selection.\n\n To see options use: desk grids or desk.grids() in python"
            )
    outputs_file_name, models_file_name = check_models(model_grid)

    grid_dusty = read_hdf5(models_file_name, testing)
    grid_dusty.rename_columns(["col0", "col1"], ["wavelength_um", "flux_wm2"])

    grid_outputs = read_hdf5(outputs_file_name, testing)
    grid_outputs.add_column(Column([1] * len(grid_outputs), name="norm"))

    return grid_dusty, grid_outputs
