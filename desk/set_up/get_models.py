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
    repository = 5912191

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


def check_models(model_grid, respond, size_filename="desk_model_grid_sizes.csv"):

    """
    Checks if model grids are available and returns the full path to the model.
    If the model is not downloaded, it is downloaded via Box.

    Parameters
    ----------
    model_grid : str
        Name of model grid to use.
    respond: Bool
        Whether to print if models were found.

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
        if respond == True:
            print("\nYou already have the grid!\n")

    else:
        # asks if you want to download the models
        if respond == True:
            print("Models not found locally")
        get_remote_models(model_grid)
    return (outputs_file, models_file)


def get_model_grid(grid, testing=False, respond=True):
    """
    Gets the real model grid name if the defaults were chosen,and runs check_models.

    Parameters
    ----------
    grid : str
        Model grid name.
    testing: str
        Flag for testing that returns small grid (3 rows)
    respond: Bool
        Whether to print if models were found.

    Returns
    -------
    grid_dusty : 2 column astropy table with array of wavelengths (um) and array of
    fluxes (Wm^2) in each column of each row. The (intial) model grid wavelengths and fluxes.
    This is not the full model grid with appended scaled models.

    grid_outputs : astropy table
        The model grid parameters corresponding to the grid_dusty model grids
    """

    def return_model_grid(_model_grid_name, testing, respond):
        """Checks models and returns model grid and outputs.

        Parameters
        ----------
        _model_grid_name : str
            Name of model grid.
        testing : Bool
            Whether this is a test.
        respond: Bool
            Whether to print if models were found.

        Returns
        -------
        type
            Description of returned object.

        """
        outputs_file_name, models_file_name = check_models(_model_grid_name, respond)
        _grid_dusty = read_hdf5(models_file_name, testing)
        _grid_dusty.rename_columns(["col0", "col1"], ["wavelength_um", "flux_wm2"])

        _grid_outputs = read_hdf5(outputs_file_name, testing)
        _grid_outputs.add_column(Column([1] * len(_grid_outputs), name="norm"))
        return _grid_dusty, _grid_outputs

    # User input for models
    if grid == "carbon":
        grid_dusty, grid_outputs = return_model_grid(
            "amorphous-carbon", testing, respond
        )
    elif grid == "oxygen":
        grid_dusty, grid_outputs = return_model_grid("silicates", testing, respond)
    elif grid == "grams":
        from astropy.table import vstack

        # combine grams
        grid_dusty_a, grid_outputs_a = return_model_grid(
            "grams-oxygen", testing, respond
        )
        grid_dusty_b, grid_outputs_b = return_model_grid(
            "grams-carbon", testing, respond
        )

        grid_dusty_a["wavelength_um"] = Column(
            np.pad(grid_dusty_a["wavelength_um"], [(0, 0), (0, 19)])
        )
        grid_dusty_a["flux_wm2"] = Column(
            np.pad(grid_dusty_a["flux_wm2"], [(0, 0), (0, 19)])
        )
        grid_dusty = vstack((grid_dusty_a, grid_dusty_b))
        grid_outputs = vstack((grid_outputs_a, grid_outputs_b))

    else:
        if (grid in config.grids) | (grid in config.external_grids):
            grid_dusty, grid_outputs = return_model_grid(grid, testing, respond)
        else:
            raise ValueError(
                "\n\nUnknown grid. Please make another model selection.\n\n To see options use: desk grids or desk.grids() in python"
            )

    return grid_dusty, grid_outputs


def get_model_index_using_number(
    grid_name, grid_outputs, requested_grid_number, requested_grid_index=0
):
    """Returns the model_outputs index of a grid or external grid given.

    Parameters
    ----------
    grid_name : str
        Name of the desk grid for which you want a model.
    grid_outputs : astropy table
        outputs table read from the `*model*_outfits.hdf5` file.
    requested_grid_number : int
        `number` which is a column in the model_outputs. Number is unique for
        external grids but not for regular grids.
    requested_grid_index : int
        `grid_idx` which is a column in the model_outputs. For grids, number and
        grid_idx create unique identifier.

    Returns
    -------
    correct_index: int
        grid outputs index of correct model.

    """
    if grid_name in config.external_grids:
        correct_index = np.where(grid_outputs["number"] == requested_grid_number)[0]
    else:
        correct_index = np.where(
            (grid_outputs["number"] == requested_grid_number)
            & (grid_outputs["grid_idx"] == requested_grid_index)
        )[0]
    if len(correct_index) > 1:
        raise ValueError("Multiple models that match that criteria")
    return correct_index[0]
