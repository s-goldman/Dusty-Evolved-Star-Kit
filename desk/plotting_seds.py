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

"""
Steve Goldman
Space Telescope Science Institute
May 17, 2018
sgoldman@stsci.edu

This script is for plotting the outputs of the sed_fitting script.
"""


def create_fig():
    """Takes results from fitting_plotting_outputs.csv and plots SED.

    Returns
    -------
    pdf
        SED figure with data in blue and model in black.

    """

    full_path = str(__file__.replace("plotting_seds.py", ""))
    input_file = Table.read("fitting_plotting_outputs.csv")
    grid_dusty = Table.read(
        full_path + "models/" + str(input_file["grid_name"][0]) + "_models.fits"
    )

    # setting axes
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
        axislabel = "log $\lambda$ F$_{\lambda}$ (W m$^{-2}$)"

        # logscale
        x_model = np.log10(x_model)
        y_model = np.log10(y_model.value)
        x_data = np.log10(x_data)
        y_data = np.log10(y_data)

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


def single_fig():
    """
    :return: Runs plotting script
    """

    full_path = str(__file__.replace("plotting_seds.py", ""))
    input_file = Table.read("fitting_plotting_outputs.csv")
    grid_dusty = Table.read(
        full_path + "models/" + str(input_file["grid_name"][0]) + "_models.fits"
    )

    # setting axes

    for counter, target in enumerate(input_file):
        # gets data for plotting
        target_name = (target["target_name"]).replace(".csv", "")
        x_data, y_data = fitting_tools.get_data(target["data_file"])
        x_model, y_model = grid_dusty[target["index"]]
        x_model = x_model[np.where(y_model != 0)]
        y_model = y_model[np.where(y_model != 0)] * input_file[counter]["norm"]
        if config.output["output_unit"] == "Wm^-2":
            axislabel = "log $\lambda$ F$_{\lambda}$ (W m$^{-2}$)"
        elif config.output["output_unit"] == "Jy":
            y_model = y_model * u.W / (u.m * u.m)
            y_model = y_model / ((x_model * u.um).to(u.Hz, equivalencies=u.spectral()))
            y_model = y_model.to(u.Jy).value
            axislabel = "log F$_{\lambda}$ (Jy)"
        else:
            raise ValueError("Unit in config.py not 'Wm^-2' or 'Jy'")

        # logscale
        x_model = np.log10(x_model)
        y_model = np.log10(y_model)
        x_data = np.log10(x_data)
        y_data = np.log10(y_data)

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
        plt.subplots_adjust(wspace=0, hspace=0)
        fig.savefig(
            "output_sed" + str(target_name) + ".png", dpi=200, bbox_inches="tight"
        )
        plt.close()


if __name__ == "__main__":
    create_fig()
