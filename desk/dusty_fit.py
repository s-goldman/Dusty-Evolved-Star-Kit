import csv
import copy
import math
import numpy as np
from desk import sed_fit, config


def dusty_fit(
    source, distance, model_grid, grid_dusty, grid_outputs, counter, number_of_targets
):
    def make_output_files_dusty():
        with open("fitting_results.csv", "w") as f:
            f.write("source,L,vexp_predicted,teff,tinner,odep,mdot\n")
            f.close()
        with open("fitting_plotting_outputs.csv", "w") as f:
            f.write("target_name,data_file,norm,index,grid_name,teff,tinner,odep\n")
            f.close()

    make_output_files_dusty()
    # calculates luminosity and scales outputs
    stat_values = []
    raw_data = sed_fit.get_data(source)  # gets target data
    # model_x = grid_dusty[0][0][:]  # gets model wavelengths
    for model in np.array(grid_dusty):
        trimmed_model = sed_fit.trim(
            raw_data, model
        )  # gets fluxes for corresponding wavelengths of data and models
        matched_model = sed_fit.find_closest(raw_data, trimmed_model)
        stats, trials = sed_fit.fit_norm(raw_data, matched_model)
        stat_values.append(stats)
    stat_array = np.vstack(stat_values)
    argmin = np.argmin(stat_array)
    model_index = argmin // stat_array.shape[1]
    trial_index = argmin % stat_array.shape[1]
    target_name = (source.split("/")[-1][:15]).replace("IRAS-", "IRAS ")

    distance_value = float(copy.copy(distance))
    distance_norm = math.log10(((float(distance) / 4.8482e-9) ** 2) / 1379)
    luminosity = int(
        np.power(10.0, distance_norm - math.log10(trials[trial_index]) * -1)
    )
    scaled_vexp = (
        float(grid_outputs[model_index]["vexp"]) * (luminosity / 10000) ** 0.25
    )
    scaled_mdot = (
        grid_outputs[model_index]["mdot"]
        * ((luminosity / 10000) ** 0.75)
        * (config.target["assumed_gas_to_dust_ratio"] / 200) ** 0.5
    )

    teff = int(grid_outputs[model_index]["teff"])
    tinner = int(grid_outputs[model_index]["tinner"])
    odep = grid_outputs[model_index]["odep"]

    # creates output file
    latex_array = [
        target_name,
        luminosity,
        np.round(scaled_vexp, 1),
        teff,
        tinner,
        odep,
        "%.3E" % float(scaled_mdot),
    ]

    plotting_array = [
        target_name,
        source,
        trials[trial_index],
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
    with open("fitting_results.csv", "a") as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(np.array(latex_array))
        f.close()

    with open("fitting_plotting_outputs.csv", "a") as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(np.array(plotting_array))
        f.close()
    counter.value += 1
