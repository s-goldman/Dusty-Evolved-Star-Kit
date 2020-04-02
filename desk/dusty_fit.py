import csv
import copy
import math
import ipdb
import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt
from desk import console_commands, config, set_up
from astropy.table import Table, Column, vstack, hstack
from create_full_grid import *
from compute_grid_weights import *
from create_pdf import *
from fitting import fit

__all__ = ["dusty_fit", "print_save_results"]


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
    liklihood /= np.sum(liklihood)

    # grid_weights = compute_total_weights(full_outputs, ["mdot", "vexp", "lum", "odep"])
    grid_weights_odep = grid_weights(full_outputs["odep"])
    pdf = pdf1d(full_outputs["odep"], 50, logspacing=True)
    bins, bin_vals = pdf.gen1d(np.arange(0, len(grid_weights_odep)), grid_weights_odep)

    ipdb.set_trace()
    # probability_distribution = liklihood * grid_weights
    # probability_distribution = grid_weights
    # most_likely, stds = create_pdfs(full_outputs, probability_distribution, 50)
    return most_likely


def print_save_results(target_string, counter, number_of_targets, most_likely):

    # creates results file
    target_name = target_string.split("/")[-1][:-4].replace("IRAS-", "IRAS ")
    latex_array = [
        target_name,
        most_likely["lum"],
        np.round(most_likely["scaled_vexp"], 1),
        most_likely["teff"],
        most_likely["teff"],
        most_likely["odep"],
        "%.3E" % float(most_likely["scaled_mdot"]),
    ]
    with open("fitting_results.csv", "a") as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(np.array(latex_array))
        f.close()

    # printed output
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
    print(("Luminosity\t\t\t|\t" + str(int(most_likely["lum"]))))
    print(("Optical depth\t\t\t|\t" + str(round(most_likely["odep"], 2))))
    print(
        ("Expansion velocity (scaled)\t|\t" + str(round(most_likely["scaled_vexp"], 2)))
    )
    print(
        (
            "Gas mass loss (scaled)\t\t|\t"
            + str("%.2E" % float(most_likely["scaled_mdot"]))
        )
    )
    print("-------------------------------------------------")

    # saves files
    with open("fitting_results.csv", "a") as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(np.array(latex_array))
        f.close()

    counter.value += 1
