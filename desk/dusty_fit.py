import csv
import copy
import math
import ipdb
import numpy as np
from copy import deepcopy
from desk import console_commands, config, set_up
from astropy.table import Table, Column, vstack, hstack
from create_full_grid import *
from compute_grid_weights import *
from fitting import fit

__all__ = ["dusty_fit"]


def dusty_fit(
    source,
    distance,
    model_grid,
    wavelength_grid,
    full_model_grid,
    full_outputs,
    grid_outputs,
    counter,
    number_of_targets,
):

    # gets target data
    data_wave, data_flux = set_up.get_data(source)

    stat_values = [
        fit.fit_data([data_wave, data_flux], [wavelength_grid, x])
        for x in full_model_grid["col0"]
    ]
    stat_array = np.array(stat_values)

    # obtains best fit model and model index
    liklihood = np.exp(-0.5 * stat_array)
    liklihood /= np.sum(liklihood)  # normalize

    grid_weights = compute_total_weights(full_outputs, ["mdot", "vexp", "lum", "odep"])
    probability_distribution = liklihood * grid_weights
    best_model = np.argmax(liklihood)

    # print and save results
    target_name = (source.split("/")[-1][:15]).replace("IRAS-", "IRAS ")

    # normalizes output values by the set distance
    distance_value = float(copy.copy(distance))
    distance_norm = math.log10(((float(distance) / 4.8482e-9) ** 2) / 1379)
    luminosity = full_outputs["lum"][best_model]
    scaled_vexp = full_outputs["scaled_vexp"][best_model]
    scaled_mdot = full_outputs["scaled_mdot"][best_model]
    teff = int(full_outputs["teff"][best_model])
    tinner = int(full_outputs["tinner"][best_model])
    odep = full_outputs["odep"][best_model]
    trial = full_outputs["trial"][best_model]
    model_index = best_model % len(grid_outputs)  # remainder

    # creates results file
    latex_array = [
        target_name,
        luminosity,
        np.round(scaled_vexp, 1),
        teff,
        tinner,
        odep,
        "%.3E" % float(scaled_mdot),
    ]

    # creates file for creating figure
    plotting_array = [
        target_name,
        source,
        trial,
        model_index,
        model_grid,
        teff,
        tinner,
        odep,
    ]

    # printed output
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
        print(("Expansion velocity (scaled)\t|\t" + str(round(scaled_vexp, 2))))
        print(("Gas mass loss (scaled)\t\t|\t" + str("%.2E" % float(scaled_mdot))))
        print("-------------------------------------------------")

    # saves files
    with open("fitting_results.csv", "a") as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(np.array(latex_array))
        f.close()

    with open("fitting_plotting_outputs.csv", "a") as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(np.array(plotting_array))
        f.close()
    counter.value += 1

    return best_model
