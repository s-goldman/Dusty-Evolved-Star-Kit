import math
import ipdb
import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np
from fnmatch import fnmatch
from astropy.io import ascii
from astropy.table import Table
from desk import config, fitting_tools
from matplotlib import rc


def get_model_and_data_for_plotting(counter, target):
    """Gets data from target.csv file and model from grid file.

    Parameters
    ----------
    counter : int
        The nth item being fit, starting at 1.
    target : astropy table row
        Results of fit item read from fitting_plotting_outputs.csv.

    Returns
    -------
    x_data: array
        log of the wavelength of the data in microns.
    y_data: array
        log of the flux of the data in w*m^-2
    x_model: array
        log of the wavelength of the model in microns.
    y_model: array
        log of the flux of the model in w*m^-2
    target_name: str
        targetname of source with underscores and extension removed

    """
    full_path = str(__file__.replace("plotting_seds.py", ""))
    input_file = Table.read("fitting_plotting_outputs.csv")
    grid_dusty = Table.read(
        full_path + "models/" + str(input_file["grid_name"][0]) + "_models.fits"
    )

    target_name = (target["target_name"]).replace(".csv", "").replace("_", " ")
    x_data, y_data = fitting_tools.get_data(target["data_file"])
    x_model, y_model = grid_dusty[target["index"]]
    x_model = x_model[np.where(y_model != 0)]
    if fnmatch(input_file["grid_name"][0], "grams*"):
        y_model = y_model * u.Jy
        y_model = y_model.to(
            u.W / (u.m * u.m), equivalencies=u.spectral_density(x_model * u.um)
        )
    else:
        y_model = y_model * u.W / (u.m * u.m)
    y_model = y_model[np.where(y_model != 0)] * input_file[counter]["norm"]

    # logscale
    x_model = np.log10(x_model)
    y_model = np.log10(y_model.value)
    x_data = np.log10(x_data)
    y_data = np.log10(y_data)
    return x_model, y_model, x_data, y_data, target_name


def create_fig():
    """Takes results from fitting_plotting_outputs.csv and plots SED.

    Returns
    -------
    png
        SED figure with data in blue and model in black.

    """

    full_path = str(__file__.replace("plotting_seds.py", ""))
    input_file = Table.read("fitting_plotting_outputs.csv")
    grid_dusty = Table.read(
        full_path + "models/" + str(input_file["grid_name"][0]) + "_models.fits"
    )

    # setting axes
    axislabel = "log $\lambda$ F$_{\lambda}$ (W m$^{-2}$)"
    if len(input_file) == 1:
        fig, ax1 = plt.subplots(1, 1, sharex=True, sharey=True, figsize=(8, 5))
    elif len(input_file) == 2:
        fig, axs = plt.subplots(2, 1, sharex=True, sharey=True, figsize=(8, 10))
    elif len(input_file) == 3:
        fig, axs = plt.subplots(3, 1, sharex=True, sharey=True, figsize=(8, 10))
    else:
        fig, axs = plt.subplots(
            math.ceil(len(input_file) / 3), 3, sharex=True, sharey=True, figsize=(8, 10)
        )
        axs = axs.ravel()

    for counter, target in enumerate(input_file):
        # gets data for plotting
        x_model, y_model, x_data, y_data, target_name = get_model_and_data_for_plotting(
            counter, target
        )

        if len(input_file) == 1:
            ax1.set_xlim(-0.99, 2.49)
            ax1.set_ylim(np.median(y_model) - 2, np.median(y_model) + 2)
            ax1.scatter(x_data, y_data, c="blue", label="data")
            ax1.plot(
                x_model,
                y_model,
                c="k",
                linewidth=0.5,
                linestyle="--",
                zorder=2,
                label="model",
            )
            ax1.annotate(
                target_name.replace("-", r"\textendash"),
                (0.07, 0.85),
                xycoords="axes fraction",
                fontsize=14,
            )
            ax1.get_xaxis().set_tick_params(which="both", direction="in", labelsize=15)
            ax1.get_yaxis().set_tick_params(which="both", direction="in", labelsize=15)
            ax1.set_xlabel("log $\lambda$ ($\mu m$)", labelpad=10)
            ax1.set_ylabel("log $\lambda$ F$_{\lambda}$ " + "(W m$^{-2}$)", labelpad=10)
        else:
            axs[counter].set_xlim(-0.99, 2.49)
            axs[counter].set_ylim(np.median(y_model) - 2, np.median(y_model) + 2)
            axs[counter].plot(
                x_model, y_model, c="k", linewidth=0.4, linestyle="--", zorder=2
            )
            axs[counter].scatter(x_data, y_data, c="blue")
            axs[counter].annotate(
                target_name.replace("-", r"\textendash"),
                (0.7, 0.8),
                xycoords="axes fraction",
                fontsize=14,
            )
            axs[counter].get_xaxis().set_tick_params(
                which="both", direction="in", labelsize=15
            )
            axs[counter].get_yaxis().set_tick_params(
                which="both", direction="in", labelsize=15
            )
            axs[counter].set_xlabel("log $\lambda$ ($\mu m$)", labelpad=10)
            axs[counter].set_ylabel(axislabel, labelpad=10)

        # pdb.set_trace()
    plt.subplots_adjust(wspace=0, hspace=0)
    fig.savefig("output_sed.png", dpi=200, bbox_inches="tight")
    plt.close()


def single_figures():
    """Takes results from fitting_plotting_outputs.csv and plots SEDs in individual
     figures.

    Returns
    -------
    png's
        SED figures with data in blue and model in black.

    """

    full_path = str(__file__.replace("plotting_seds.py", ""))
    input_file = Table.read("fitting_plotting_outputs.csv")
    grid_dusty = Table.read(
        full_path + "models/" + str(input_file["grid_name"][0]) + "_models.fits"
    )

    for counter, target in enumerate(input_file):
        # gets data for plotting
        x_model, y_model, x_data, y_data, target_name = get_model_and_data_for_plotting(
            counter, target
        )

        # Figure plotting
        fig, ax1 = plt.subplots(1, 1, sharex=True, sharey=True, figsize=(8, 5))
        ax1.set_xlim(-0.99, 2.49)
        ax1.set_ylim(np.median(y_model) - 3, np.median(y_model) + 3)
        ax1.scatter(x_data, y_data, c="blue", label="data")
        ax1.plot(
            x_model,
            y_model,
            c="k",
            linewidth=0.5,
            linestyle="--",
            zorder=2,
            label="model",
        )
        ax1.annotate(
            target_name.replace("_", " "),
            (0.07, 0.85),
            xycoords="axes fraction",
            fontsize=14,
        )
        ax1.get_xaxis().set_tick_params(which="both", direction="in", labelsize=15)
        ax1.get_yaxis().set_tick_params(which="both", direction="in", labelsize=15)
        ax1.set_xlabel("log $\lambda$ ($\mu m$)", labelpad=10)
        ax1.set_ylabel("log $\lambda$ F$_{\lambda}$ " + "(W m$^{-2}$)", labelpad=10)
        fig.savefig(
            "output_sed_" + str(target_name) + ".png", dpi=200, bbox_inches="tight"
        )
        plt.close()


if __name__ == "__main__":
    create_fig()
