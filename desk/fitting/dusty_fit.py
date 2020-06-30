# Steve Goldman, Space Telescope Science Institute, sgoldman@stsci.edu
import csv
import ipdb
import numpy as np
from desk.set_up import config, get_data
from astropy.table import Table
from desk.fitting import fitting_tools
from desk.probabilities import compute_grid_weights, create_pdf
from desk.probabilities import create_prior, resample_prior_to_model_grid


def fit_single_source(source_number, fit_params):
    source_file_name = fit_params.file_names[source_number]
    full_model_grid = fit_params.full_model_grid
    full_outputs = fit_params.full_outputs
    data = get_data.get_values(
        source_file_name,
        fit_params.min_wavelength,
        fit_params.max_wavelength,
        fitting=True,
    )

    # calculate chi squared values for each model
    liklihood = np.array(
        [
            fitting_tools.fit.fit_data(
                data, [fit_params.model_wavelength_grid, x["col0"]]
            )
            for x in full_model_grid
        ]
    )

    if fit_params.bayesian_fit == True:
        # liklihood /= np.sum(liklihood)  # normalized
        # compute grid weights
        grid_weights_odep = compute_grid_weights.grid_weights(full_outputs["odep"])

        # priors
        lmc_data = Table.read(
            config.path + "probabilities/priors/LMC_tables_H11_all.dat", format="ascii"
        )
        create_prior.prior(lmc_data, "dmdt", 2e-6)
        create_prior.prior(lmc_data, "L", 1000)

        p_dmdt = resample_prior_to_model_grid.resamp(
            full_outputs, "scaled_mdot", "dmdt"
        )
        p_lum = resample_prior_to_model_grid.resamp(full_outputs, "lum", "L")
        # combined_grid_weights, priors, and liklihoods
        probs = grid_weights_odep * liklihood * p_dmdt * p_lum

        ## most likly values
        odep_best = create_pdf.par_pdf("odep", full_outputs, probs)
        lum_best = create_pdf.par_pdf("lum", full_outputs, probs)
        mdot_best = create_pdf.par_pdf("scaled_mdot", full_outputs, probs)
        vexp_best = create_pdf.par_pdf("scaled_vexp", full_outputs, probs)
        best = [odep_best, lum_best, mdot_best, vexp_best]

    else:
        probs = liklihood

    best_fit = full_outputs[np.argmax(liklihood)]
    out = Table(best_fit)

    target_name = source_file_name.split("/")[-1][:-4].replace("IRAS-", "IRAS ")

    # creates results file
    with open("fitting_results.csv", "a") as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow([target_name] + [str(x) for x in out[0]] + [source_file_name])
        f.close()

    # printed output
    print(
        "\n\n             Target: "
        + target_name
        + "\t\t"
        + str(source_number + 1)
        + "/"
        + str(len(fit_params.file_names))
    )
    print("-" * 56)
    print(("Luminosity\t\t\t|\t" + "{:,}".format((int(best_fit["lum"])))) + " Msun")
    print(("Optical depth (at 10 um)\t|\t" + str(round(best_fit["odep"], 2))))
    print(
        ("Expansion velocity (scaled)\t|\t" + str(round(best_fit["scaled_vexp"], 2)))
        + " km/s"
    )
    print(
        ("Gas mass loss (scaled)\t\t|\t" + str("%.2E" % float(best_fit["scaled_mdot"])))
        + " Msun/yr"
    )
    print("-" * 56)

    # fit_params.counter.value += 1
    # return fit_params.counter
