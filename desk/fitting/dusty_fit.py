# Steve Goldman, Space Telescope Science Institute, sgoldman@stsci.edu
import csv
import ipdb
import numpy as np
from desk.set_up import config, get_data
from astropy.table import Table

import desk.console_commands
from desk.fitting import fitting_tools


def fit_single_source(source_number : int, fit_params):
    """Fits a single source with the data and models included in class fit_params.

    Parameters
    ----------
    source_number : int
        Index of source in list of targets.
    fit_params : Class
        Fit parameters generated by desk.set_up.get_inputs.fitting_parameters().

    Returns
    -------
    Results from the best-fit model are appended to "fitting_results.csv",
    and results are printed.

    """
    source_file_name = fit_params.file_names[source_number]
    full_outputs = fit_params.full_outputs
    data = get_data.get_values(
        source_file_name,
        fit_params.min_wavelength,
        fit_params.max_wavelength,
        fitting=True,
    )

    if fit_params.grid == "grams":
        # models are not trimmed as the two grids are uneven. They are kept
        # the same size for speed.
        liklihood = np.array(
            [
                fitting_tools.fit.fit_data(
                    data,
                    [
                        fit_params.full_model_grid["wavelength_um"][i],
                        fit_params.full_model_grid["flux_wm2"][i],
                    ],
                )
                for i in range(0, len(fit_params.full_model_grid["flux_wm2"]))
            ]
        )

    else:
        # trim models
        trimmed_model_wavelength, trimmed_model_fluxes = fitting_tools.trim_grid(
            data, fit_params
        )

        # calculate chi squared values for each model
        liklihood = np.array(
            [
                fitting_tools.fit.fit_data(
                    data, [trimmed_model_wavelength, x["flux_wm2"]]
                )
                for x in trimmed_model_fluxes
            ]
        )
    best_fit = full_outputs[np.argmax(liklihood)]
    out = Table(best_fit)
    
    target_name = source_file_name.split("/")[-1][:-4].replace("IRAS-", "IRAS ")

    # creates results file
    with open("fitting_results.csv", "a") as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(
            [target_name]
            + [str(x) for x in out[0]]
            + [source_file_name]
            + [fit_params.distance]
        )
        f.close()

    # make clear that grams is dust mass loss rates
    mass_loss_str = "Gas"
    if "grams" in fit_params.grid:
        mass_loss_str = "Dust"
        
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
        (f"{mass_loss_str} mass loss (scaled)\t\t|\t" + str("%.2E" % float(best_fit["scaled_mdot"])))
        + " Msun/yr"
    )
    print("-" * 56)
    
    if "grams" in fit_params.grid:
        print("\n**Note: GRAMS uses DUST mass loss rates, not gas mass loss rates.**\n")

    if fit_params.save_model_spectrum == True:
        if (fit_params.grid in config.external_grids) | (fit_params.grid == "grams"):
            print(
                "Saving output model spectrum still in development for external grids"
            )
        else:
            print("Saving output model spectrum.")
            desk.console_commands.save_model(
                fit_params.grid,
                best_fit["number"],
                best_fit["grid_idx"],
                best_fit["lum"],
                fit_params.distance,
                custom_output_name="dusty_" + target_name + "_model_",
            )
