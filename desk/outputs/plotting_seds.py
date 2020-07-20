import math, ipdb
import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np
from fnmatch import fnmatch
from astropy.table import Table
from desk.set_up import get_data


def get_model_and_data_for_plotting(counter, target):
    """
    Gets data from target.csv file and model from grid file.

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
    """
    full_path = str(__file__.replace("outputs/plotting_seds.py", ""))
    input_file = Table.read("fitting_results.csv")
    grid_dusty = Table.read(
        full_path + "models/" + str(input_file["grid"][0]) + "_models.hdf5"
    )

    x_data, y_data = get_data.get_values(target["file_name"])
    x_model, y_model = grid_dusty[target["model_id"] - 1]  # model_id starts at 1

    x_model = x_model[np.where(y_model != 0)]
    y_model = y_model[np.where(y_model != 0)]

    if fnmatch(input_file["grid"][0], "grams*"):
        y_model = y_model * u.Jy
        y_model = y_model.to(
            u.W / (u.m * u.m), equivalencies=u.spectral_density(x_model * u.um)
        )

    else:
        y_model = y_model * u.W / (u.m * u.m)
        y_model = y_model * np.power(10, input_file[counter]["norm"])

    # logscale
    x_model = np.log10(x_model)
    y_model = np.log10(y_model.value)
    x_data = np.log10(x_data)
    y_data = np.log10(y_data)
    return x_model, y_model, x_data, y_data


def create_fig():
    """
    Takes results from fitting_plotting_outputs.csv and plots SED.

    Returns
    -------
    png
        SED figure with data in blue and model in black.

    """
    # full_path = str(__file__.replace("outputs/plotting_seds.py", ""))
    input_file = Table.read("fitting_results.csv")
    # grid_dusty = Table.read(
    #     full_path + "models/" + str(input_file["grid"][0]) + "_models.fits"
    # )

    # setting axes
    axislabel = r"log $\lambda$ F$_{\lambda}$ (W m$^{-2}$)"
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
        x_model, y_model, x_data, y_data = get_model_and_data_for_plotting(
            counter, target
        )

        # find median y_model values in data range
        median = np.median(
            y_model[(x_model > np.min(x_data)) & (x_model < np.max(x_data))]
        )

        y_min = median - 2
        y_max = median + 2

        y_diff = np.median(y_data) - median

        if y_diff > 0:
            y_max = y_max + y_diff
        else:
            y_min = y_min - y_diff

        # plotting
        if len(input_file) == 1:
            ax1.set_xlim(-0.99, 2.49)
            ax1.set_ylim(y_min, y_max)
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
                str(target["source"]).replace("_", ""),
                (0.07, 0.85),
                xycoords="axes fraction",
                fontsize=14,
            )
            ax1.get_xaxis().set_tick_params(which="both", direction="in", labelsize=15)
            ax1.get_yaxis().set_tick_params(which="both", direction="in", labelsize=15)
            ax1.set_xlabel(r"log $\lambda$ ($\mu m$)", labelpad=10)
            ax1.set_ylabel(
                r"log $\lambda$ F$_{\lambda}$ " + "(W m$^{-2}$)", labelpad=10
            )
        else:
            axs[counter].set_xlim(-0.99, 2.49)
            axs[counter].set_ylim(y_min, y_max)
            axs[counter].plot(
                x_model, y_model, c="k", linewidth=0.4, linestyle="--", zorder=2
            )
            axs[counter].scatter(x_data, y_data, c="blue")
            axs[counter].annotate(
                str(target["source"]).replace("_", ""),
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
            axs[counter].set_xlabel(r"log $\lambda$ ($\mu m$)", labelpad=10)
            axs[counter].set_ylabel(axislabel, labelpad=10)

        # pdb.set_trace()
    plt.subplots_adjust(wspace=0, hspace=0)
    fig.savefig("output_sed.png", dpi=200, bbox_inches="tight")
    plt.close()


def single_figures():
    """
    Takes results from fitting_plotting_outputs.csv and plots SEDs.
    Plots in individual figures.

    Returns
    -------
    png's
        SED figures with data in blue and model in black.

    """
    # full_path = str(__file__.replace("outputs/plotting_seds.py", ""))
    input_file = Table.read("fitting_results.csv")
    # grid_dusty = Table.read(
    #     full_path + "models/" + str(input_file["grid"][0]) + "_models.fits"
    # )

    for counter, target in enumerate(input_file):
        # gets data for plotting
        x_model, y_model, x_data, y_data = get_model_and_data_for_plotting(
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
            str(target["source"]).replace("_", " "),
            (0.07, 0.85),
            xycoords="axes fraction",
            fontsize=14,
        )
        ax1.get_xaxis().set_tick_params(which="both", direction="in", labelsize=15)
        ax1.get_yaxis().set_tick_params(which="both", direction="in", labelsize=15)
        ax1.set_xlabel(r"log $\lambda$ ($\mu m$)", labelpad=10)
        ax1.set_ylabel(r"log $\lambda$ F$_{\lambda}$ " + "(W m$^{-2}$)", labelpad=10)
        fig.savefig(
            "output_sed_" + str(target["source"]) + ".png", dpi=200, bbox_inches="tight"
        )
        plt.close()


if __name__ == "__main__":
    create_fig()
