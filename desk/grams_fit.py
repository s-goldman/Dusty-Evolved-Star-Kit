import csv
import copy
import math
import ipdb
import numpy as np
from desk import sed_fit, config


def grams_fit(
    source, distance, model_grid, grid_dusty, grid_outputs, counter, number_of_targets
):
    """Function fits astropy table data with a least squares method.

    Parameters
    ----------
    source : str
        Name of the source being fit.
    distance : float
        Distance to source in kpc.
    model_grid : str
        Name of model grid being used.
    grid_dusty : astropy table
        Table with two items in each row item 1 being an array
        with wavelength in microns and item 2 being an array with flux in w/m2.
    grid_outputs : astropy table
        Table with each row showing the output results corresponding to each row
        in grid_dusty
    counter : int
        The nth item being fit.
    number_of_targets : int
        The total number of sources to be fit.

    """

    # Initialize variables
    stat_values = []

    # gets target data
    raw_data = sed_fit.get_data(source)

    #
    flux_scaling_factor = 50 ** 2 / float(distance) ** 2

    def trim_find_lsq(model):
        # removes data outside of wavelegth range of model grid
        trimmed_model = sed_fit.trim(raw_data, model)

        # gets fluxes for corresponding wavelengths of data and models
        matched_model = sed_fit.find_closest(raw_data, trimmed_model)

        # normalize model to specified distance
        scaled_matched_model = matched_model * flux_scaling_factor

        # fits source with least squares
        stats = sed_fit.least2(raw_data, matched_model)
        stat_values.append(stats)

    [trim_find_lsq(x) for x in grid_dusty]

    # obtains best fit model and model index
    stat_array = np.vstack(stat_values)
    argmin = np.argmin(stat_array)  # lowest chi square value
    model_index = argmin // stat_array.shape[1]
    target_name = (source.split("/")[-1][:15]).replace("IRAS-", "IRAS ")

    distance_value = float(copy.copy(distance))
    luminosity = grid_outputs[model_index]["lum"] * ((distance_value / 50) ** 2)
    teff = grid_outputs[model_index]["teff"]
    tinner = grid_outputs[model_index]["tinner"]
    odep = grid_outputs[model_index]["odep"]
    mdot = grid_outputs[model_index]["mdot"] * (distance_value / 50)
    rin = grid_outputs[model_index]["rin"] * (distance_value / 50)

    # creates output file
    latex_array = [
        target_name,
        luminosity,
        rin,
        teff,
        tinner,
        odep,
        "%.3E" % float(mdot),
    ]

    plotting_array = [
        target_name,
        source,
        flux_scaling_factor,
        model_index,
        model_grid,
        teff,
        tinner,
        odep,
    ]
    if config.output["printed_output"] == "True":
        print()
        print()
        print(
            (
                "             Target: "
                + target_name
                + "        "
                + str(counter.value + 1)
                + "/"
                + str(number_of_targets)
            )
        )
        print("-------------------------------------------------")
        print(("Luminosity\t\t\t|\t" + str(round(luminosity))))
        print(
            (
                "Optical depth\t\t\t|\t"
                + str(round(grid_outputs[model_index]["odep"], 3))
            )
        )
        print(("Inner Radius\t\t\t|\t" + str("%.2E" % float(rin))))
        print(("Dust production rate \t\t|\t" + str("%.2E" % float(mdot))))
        print("-------------------------------------------------")
    with open("fitting_results.csv", "a") as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(np.array(latex_array))
        f.close()

    with open("fitting_plotting_outputs.csv", "a") as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(np.array(plotting_array))
        f.close()
    counter.value += 1
