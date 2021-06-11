# Steve Goldman, Space Telescope Science Institute, sgoldman@stsci.edu
import ipdb
import pkg_resources

from multiprocessing import Pool, cpu_count
from functools import partial
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
import time

desk_path = str(__file__.replace("console_commands.py", ""))


def grids():
    """Prints the model grids available for fitting.

    """
    print("\nDUSTY Grids:")
    for item in config.grids:
        print("\t" + str(item))
    print("\nExternal Grids:")
    for item in config.external_grids + ["grams"]:
        print("\t" + str(item))
    print("\n")


def version():
    """Returns DESK version.
    """
    print("\n\tDESK version: " + pkg_resources.get_distribution("desk").version + "\n")


def sed(
    source_path=".",
    source_filename="fitting_results.csv",
    dest_path=".",
    save_name="output_sed.png",
    flux="Wm2",
):
    """Creates single SED figure of all fit SEDs using
    the 'fitting_results.csv' file.

    Parameters
    ----------
    source_path : str
        Path to source.
    source_filename : str
        fit results filename.
    dest_path : str
        Path to save figure.
    save_name : str
        Figure filename to be saved.
    flux: str
        flux type (Wm2 or Jy)
    Returns
    -------
    png
        SED figure with data in blue and model in black.
    """
    plotting_seds.create_fig(
        source_path, source_filename, dest_path, save_name, flux=flux
    )


def sed_indiv(
    source_path=".", source_filename="fitting_results.csv", dest_path=".", flux="Wm2"
):
    """Creates individual SED figures for all fit SEDs using
    the 'fitting_results.csv' file.

    Parameters
    ----------
    source_path : str
        Path to source.
    source_filename : str
        fit results filename.
    dest_path : str
        Path to save figure.
    save_name : str
        Figure filename to be saved.
    flux: str
        flux type (Wm2 or Jy)
    Returns
    -------
    png
        SED figure with data in blue and model in black.
    """
    plotting_seds.single_figures(source_path, source_filename, dest_path, flux=flux)


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


def fit(
    source=desk_path + "put_target_data_here",
    distance=config.target["distance_in_kpc"],
    grid=config.fitting["default_grid"],
    n=config.fitting["default_number_of_times_to_scale_models"],
    min_wavelength=config.fitting["default_wavelength_min"],
    max_wavelength=config.fitting["default_wavelength_max"],
    multiprocessing=cpu_count() - 1,
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
    multiprocessing : bool or int
        Uses all but one core if True, only one core if False, or uses the
        number of cores specified as an integer.
    testing : bool
        Flag for testing that uses only the first 3 rows of the mode grids.
    """

    # Set-up ###################################################################
    # timer
    startTime = time.time()

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

    if testing == False:
        # Get number of cores to use
        # trys (moves to except if not int(bool))
        if type(multiprocessing) == int:
            n_cores = multiprocessing

        # if True: max cores - 1, if False: 1 core
        else:
            if (multiprocessing == "True") | (multiprocessing == True):
                n_cores = cpu_count() - 1
            elif (multiprocessing == "False") | (multiprocessing == False):
                n_cores = 1
            else:
                raise ValueError(
                    "Multiprocessing error: Invalid option: " + str(multiprocessing)
                )

        # check if too many cores specificed
        if n_cores > cpu_count():
            raise ValueError(
                "Invalid multiprocessing options: Insufficient cores "
                + "\n Available cores: "
                + str(cpu_count())
            )
        # check if less than 1
        elif n_cores < 1:
            raise ValueError(
                "Invalid multiprocessing options. Value must be positive: "
                + str(multiprocessing)
            )

    elif (testing == True) | (grid == "desk-mix"):
        # ignore n_cores and replace with 1 if in testing mode
        n_cores = 1
    else:
        raise ValueError("Invalid testing options: " + str(testing))

    # Fitting
    print("\nFit parameters\n--------------")
    print("Grid:\t\t" + grid)
    print("Distance:\t" + str(distance) + " kpc")
    if fit_params.grid in config.external_grids:
        print("Grid density:\t" + str(n) + " (ignored as it is an external grids)")
    else:
        print("Grid density:\t" + str(n))
    print("# of cores:\t" + str(n_cores))

    if n_cores == 1:
        # Single-core fitting
        [dusty_fit.fit_single_source(x, fit_params) for x in range(len(file_names))]

    else:
        # Multi-core fitting
        pool = Pool(n_cores)
        mapfunc = partial(dusty_fit.fit_single_source, fit_params=fit_params)
        pool.map(mapfunc, range(len(file_names)), chunksize=1)

    print("See fitting_results.csv for more information.")

    # automatically create sed figure
    # plotting_seds.create_fig()

    # Print execution time
    executionTime = time.time() - startTime
    if executionTime < 200:
        print("Execution time: " + str("{:.2f}".format(executionTime)) + " s")
    elif (executionTime > 200) & (executionTime < 3600):
        print("Execution time: " + str("{:.2f}".format(executionTime / 60)) + " m")
    else:
        print("Execution time: " + str("{:.2f}".format(executionTime / 60 / 60)) + " h")


if __name__ == "__main__":
    fit()
