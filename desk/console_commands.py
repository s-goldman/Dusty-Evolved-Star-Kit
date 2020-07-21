# Steve Goldman, Space Telescope Science Institute, sgoldman@stsci.edu
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
    full_grid,
)
from desk.fitting import dusty_fit
from desk.outputs import plotting_seds, interpolate_dusty

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


def save_model(grid_name, luminosity, teff, tinner, tau, distance_in_kpc):
    """ See interpolate_dusty.
    """
    interpolate_dusty.interpolate(
        grid_name,
        float(luminosity),
        float(teff),
        float(tinner),
        float(tau),
        float(distance_in_kpc),
    )


def sed_indiv():
    """Creates an individual SED figure for each SED fit using the
    results in the 'fitting_results.csv' file.

    Returns
    -------
    multiple pngs

    """
    plotting_seds.single_figures()


def fit(
    source=desk_path + "put_target_data_here",
    distance=config.target["distance_in_kpc"],
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
    distance : str, float
        Distance to source(s) in kiloparsecs.
    grid : str
        Name of model grid.
    n : str or int
        Number of times to scale the grid between the
        lum_min and lum_max specified in the config.py script
        (essentially grid density).
    min_wavelength : float
        Minimum wavelength to fit, the other data will still be shown
        in the output SED.
    max_wavelength : float
        Maximum wavelength to be fit.
    multiprocessing : bool
        Flag that, if true, uses all but one of the user's
        available cores for the fitting.
    testing : bool
        Flag for testing that uses only the first 3 rows of the mode grids.
    """

    # Set-up ###################################################################
    # bayesian fitting currently in development
    bayesian_fit = False

    # get data filenames
    file_names = get_data.compile_data(source)

    # gets models
    grid_dusty, grid_outputs = get_models.get_model_grid(grid, testing)

    # create class for scaling to full grids
    full_grid_params = full_grid.instantiate(
        grid, grid_dusty, grid_outputs, float(distance), int(n)
    )
    # scale to full grids and get distance scaling factors
    full_outputs, full_model_grid = full_grid.retrieve(full_grid_params)

    # get model wavelengths
    model_wavelength_grid = grid_dusty["wavelength_um"][0]

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

    # remove old / create new output files
    create_output_files.make_output_files_dusty(fit_params)

    if multiprocessing == True:
        # Multi-core fitting
        pool = Pool(processes=cpu_count() - 1)
        mapfunc = partial(dusty_fit.fit_single_source, fit_params=fit_params)
        pool.map(mapfunc, range(len(file_names)), chunksize=1)
    else:
        # Single-core fitting
        [dusty_fit.fit_single_source(x, fit_params) for x in range(len(file_names))]

    # automatically create sed figure
    # plotting_seds.create_fig()


if __name__ == "__main__":
    fit()
