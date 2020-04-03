# Steve Goldman, Space Telescope Science Institute, sgoldman@stsci.edu
import csv
import ipdb
import numpy as np
import matplotlib.pyplot as plt
from desk.set_up import config
from desk.fitting import fitting_tools
from desk.probabilities import compute_grid_weights, create_pdf


def fit_single_source(
    source_file_name,
    data,
    user,
    wavelength_grid,
    full_model_grid,
    full_outputs,
    counter,
    number_of_targets,
):

    # calculate chi squared values for each model
    chi2_vals = np.array(
        [
            fitting_tools.fit.fit_data(data, [wavelength_grid, x["col0"]])
            for x in full_model_grid
        ]
    )

    # obtains best fit model and model index
    liklihood = np.exp(-0.5 * chi2_vals)
    liklihood /= np.sum(liklihood)  # normalized

    # compute grid weights
    grid_weights_odep = compute_grid_weights.grid_weights(full_outputs["odep"])

    # create 1d-pdfs
    pdf = create_pdf.pdf1d(full_outputs["odep"], 50, logspacing=True)

    # combined_grid_weights, priors, and liklihoods
    probs = grid_weights_odep * liklihood

    # calculates probabilities for each bin (bin width set by dif in bins)
    bins, bin_vals = create_pdf.pdf1d.gen1d(
        pdf, np.arange(0, len(grid_weights_odep)), probs
    )

    ipdb.set_trace()
    # return most_likely


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
