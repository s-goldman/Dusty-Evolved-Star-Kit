# Steve Goldman, Space Telescope Science Institute, sgoldman@stsci.edu
import csv
import ipdb
import numpy as np
import matplotlib.pyplot as plt
from desk.set_up import config
from astropy.table import Table
from desk.fitting import fitting_tools
from desk.probabilities import compute_grid_weights, create_pdf
from desk.probabilities import create_prior, resample_prior_to_model_grid


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
    liklihood = np.array(
        [
            fitting_tools.fit.fit_data(data, [wavelength_grid, x["col0"]])
            for x in full_model_grid
        ]
    )
    ipdb.set_trace()
    liklihood /= np.sum(liklihood)  # normalized

    # compute grid weights
    grid_weights_odep = compute_grid_weights.grid_weights(full_outputs["odep"])

    # priors
    lmc_data = Table.read(
        config.path + "probabilities/priors/LMC_tables_H11_all.dat", format="ascii"
    )
    create_prior.prior(lmc_data, "dmdt", 2e-6)
    create_prior.prior(lmc_data, "L", 1000)

    p_dmdt = resample_prior_to_model_grid.resamp(full_outputs, "scaled_mdot", "dmdt")
    p_lum = resample_prior_to_model_grid.resamp(full_outputs, "lum", "L")

    # combined_grid_weights, priors, and liklihoods
    probs = grid_weights_odep * liklihood * p_dmdt * p_lum

    odep_best = create_pdf.par_pdf("odep", full_outputs, probs)
    lum_best = create_pdf.par_pdf("lum", full_outputs, probs)
    mdot_best = create_pdf.par_pdf("scaled_mdot", full_outputs, probs)
    vexp_best = create_pdf.par_pdf("scaled_vexp", full_outputs, probs)

    best_fit = full_outputs[np.argmax(probs)]

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
