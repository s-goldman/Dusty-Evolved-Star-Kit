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
    best_fit = full_outputs[np.argmax(liklihood)]
    out = Table(best_fit)
    out.remove_columns(["vexp", "mdot"])

    target_name = source_file_name.split("/")[-1][:-4].replace("IRAS-", "IRAS ")

    with open("fitting_results.csv", "a") as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow([target_name] + [str(x) for x in out[0]] + [source_file_name])
        f.close()

    # creates results file

    # printed output
    print()
    print()
    print(
        (
            "             Target: "
            + target_name
            + "        "
            + str(counter)
            + "/"
            + str(number_of_targets)
        )
    )
    print("-------------------------------------------------")
    print(("Luminosity\t\t\t|\t" + str(int(best_fit["lum"]))))
    print(("Optical depth\t\t\t|\t" + str(round(best_fit["odep"], 2))))
    print(("Expansion velocity (scaled)\t|\t" + str(round(best_fit["scaled_vexp"], 2))))
    print(
        ("Gas mass loss (scaled)\t\t|\t" + str("%.2E" % float(best_fit["scaled_mdot"])))
    )
    print("-------------------------------------------------")

    counter += 1
    return counter
