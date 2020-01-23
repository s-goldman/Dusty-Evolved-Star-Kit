import csv
import copy
import math
import numpy as np
from desk import console_commands, config, fitting_tools


def dusty_fit(
    model_grid, source, distance, grid_dusty, grid_outputs, counter, number_of_targets
):
    """Function fits astropy table data with a least squares method.

    Parameters
    ----------
    model_grid : str
        Name of model grid being used.
    source : str
        Name of the source being fit.
    distance : float
        Distance to source in kpc.
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
    raw_data = fitting_tools.get_data(source)

    trials = fitting_tools.create_trials(raw_data[1])

    stat_values.append(
        [fitting_tools.trim_find_lsq(x, raw_data, trials) for x in grid_dusty]
    )

    # obtains best fit model and model index
    stat_array = np.vstack(stat_values)
    argmin = np.argmin(stat_array)  # lowest chi square value
    model_index = argmin // stat_array.shape[1]
    trial_index = argmin % stat_array.shape[1]
    target_name = (source.split("/")[-1][:15]).replace("IRAS-", "IRAS ")

    # normalizes output values by the set distance
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
