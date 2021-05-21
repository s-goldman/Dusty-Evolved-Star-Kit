import sys
import math
import seaborn as sns
import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np
from fnmatch import fnmatch
from astropy.table import Table
from desk.set_up import get_data

sns.set_palette("colorblind")


def plot_phot(x_data, y_data, ax):
    ax.scatter(x_data, y_data)
    return ax


def plot_model(x_model, y_model, ax):
    ax.plot(x_model, y_model, c="k", linewidth=0.4, linestyle="--", zorder=2)
    return ax


def wm2_to_Jy(wave_in_microns, wm2):
    wm2_w_units = (wm2 * u.W / (u.m * u.m)) / (
        (wave_in_microns * u.um).to(u.Hz, equivalencies=u.spectral())
    )
    jy = wm2_w_units.to(u.Jy).value
    return jy


def source_name_annotation(name, ax):
    ax.annotate(
        str(name).replace("_", " "),
        (0.95, 0.8),
        xycoords="axes fraction",
        ha="right",
        fontsize=14,
    )


def counter_annotations(counter, ax):
    ax.annotate(
        str(counter + 1),
        (0.075, 0.85),
        ha="left",
        va="center",
        xycoords="axes fraction",
        fontsize=14,
    )
    return ax


def set_inward_ticks(ax):
    ax.get_xaxis().set_tick_params(which="both", direction="in", labelsize=12)
    ax.get_yaxis().set_tick_params(which="both", direction="in", labelsize=12)
    return ax


def set_limits(x_model, y_model, x_data, y_data, ax):
    # set y_limits using median of model in wavelength range of data
    median = np.median(y_model[(x_model > np.min(x_data)) & (x_model < np.max(x_data))])
    y_min = median - 2  # room below
    y_max = median + 1.75  # room above
    # addes to range if median data is out of range
    y_diff = np.median(y_data) - median
    if y_diff > 0:
        y_max = y_max + y_diff
    else:
        y_min = y_min + y_diff
    ax.set_xlim(-0.99, 2.49)
    ax.set_ylim(y_min, y_max)
    return ax


def add_axis_labels(fig, fontsize, _flux):
    # Common figure labels
    ax = fig.add_subplot(111, frameon=False)
    ax.tick_params(labelcolor="none", top=False, bottom=False, left=False, right=False)
    ax.grid(False)
    ax.set_xlabel(r"log $\lambda$ ($\mu m$)", labelpad=10, fontsize=fontsize)
    if _flux == "Jy":
        ax.set_ylabel(r"log F$_{\nu}$ " + "(Jy)", labelpad=15, fontsize=fontsize)
    else:
        ax.set_ylabel(
            r"log $\lambda$ F$_{\lambda}$ " + "(W m$^{-2}$)",
            labelpad=15,
            fontsize=fontsize,
        )
    return fig


def get_model_and_data_for_plotting(
    counter, target, source_path, source_filename, flux
):
    """
    Gets data from target.csv file and model from grid file.

    Parameters
    ----------
    counter : int
        The nth item being fit, starting at 1.
    target : astropy table row
        Results of fit item read from fitting_plotting_outputs.csv.
    source_path: str
        Path of source
    source_filename: str
        Filename of fitting results
    flux: str
        flux type (Wm2 or Jy)
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
    input_file = Table.read(source_path + "/" + source_filename)
    grid_dusty = Table.read(
        full_path + "models/" + str(input_file["grid_name"][0]) + "_models.hdf5"
    )

    x_data, y_data = get_data.get_values(target["file_name"])
    x_model_init, y_model_init = grid_dusty[
        target["number"] - 1
    ]  # model_id starts at 1

    x_model_select = x_model_init[np.where(y_model_init != 0)]
    y_model_select = y_model_init[np.where(y_model_init != 0)]
    y_model_scaled = y_model_select * np.power(10, input_file[counter]["norm"])

    if flux == "Jy":
        y_model_plot = wm2_to_Jy(x_model_select, y_model_scaled)
        y_data_plot = wm2_to_Jy(x_data, y_data)
    else:
        # wm2
        y_model_plot = y_model_scaled
        y_data_plot = y_data

    x_model_log = np.log10(x_model_select)
    y_model_log = np.log10(y_model_plot)

    x_data_log = np.log10(x_data)
    y_data_log = np.log10(y_data_plot)

    return x_model_log, y_model_log, x_data_log, y_data_log


def single_figures(source_path, source_filename, dest_path, flux):
    """
    Takes results from fitting_plotting_outputs.csv and plots SEDs.
    Plots in individual figures.

    Returns
    -------
    png's
        SED figures with data in blue and model in black.

    """
    try:
        input_file = Table.read(source_path + "/" + source_filename)
    except:
        raise FileNotFoundError(
            "fitting_results.csv missing. Make sure you have run the ``fit'' command."
        )

    for counter, target in enumerate(input_file):
        # gets data for plotting
        x_model, y_model, x_data, y_data = get_model_and_data_for_plotting(
            counter, target, source_path, source_filename, flux=flux
        )

        # Figure plotting
        fig, ax1 = plt.subplots(1, 1, sharex=True, sharey=True, figsize=(6, 4))
        set_limits(x_model, y_model, x_data, y_data, ax1)
        plot_model(x_model, y_model, ax1)
        plot_phot(x_data, y_data, ax1)
        ax1.annotate(
            str(target["source"]).replace("_", " "),
            (0.95, 0.9),
            xycoords="axes fraction",
            ha="right",
            fontsize=14,
        )
        add_axis_labels(fig, 12, flux)
        fig.savefig(
            dest_path + "/" + "output_sed_" + str(target["source"]) + ".png",
            dpi=200,
            bbox_inches="tight",
        )
        plt.close()


def create_fig(source_path, source_filename, dest_path, save_name, flux):
    """Creates single SED figure of all fit SEDs using the source_filename file.

    Parameters
    ----------
    source_path : str
        Path to source.
    source_filename : str
        fit results filename.
    dest_path : str
        Path to save figure.
    save_name : str
        Figure filename to be saved.
    flux: str
        flux type (Wm2 or Jy)

    Returns
    -------
    png
        SED figure with data in blue and model in black.
    """

    try:
        input_file = Table.read(source_path + "/" + source_filename)
    except:
        raise FileNotFoundError(
            "fitting_results.csv missing. Make sure you have run the ``fit'' command."
        )

    if flux == "Wm2":
        print("Using Wm2\n")
    elif flux == "Jy":
        print("Using Jy\n")
    else:
        print(
            "Unidentified option: "
            + str(flux)
            + "\nUsing Wm2. Alternative option is Jy."
        )

    n = len(input_file)  # number of fit sources

    # setting figure size and axes for different numbers of fit sources
    if n != 1:
        if n == 2:
            fig, axs = plt.subplots(2, 1, sharex=True, sharey=True, figsize=(6, 7.5))
        elif n == 3:
            fig, axs = plt.subplots(3, 1, sharex=True, sharey=True, figsize=(6, 7.5))
        elif n > 17:
            print(
                "\n\n\tToo many sources for combined figure. Use the function `desk sed_indiv` \n\t"
                + "to create individual figures. You can also retrieve the best-fit model \n\t"
                + "and create your own SED figure using the `desk save_model` function. \n\n"
            )
            sys.exit()
        else:
            figure_rows = math.ceil(n / 3)
            fig, axs = plt.subplots(
                figure_rows,
                3,
                sharex=True,
                sharey=True,
                figsize=(8, (figure_rows * 1.5)),
            )
            axs = axs.ravel()

        # axis common labels
        add_axis_labels(fig, 14, flux)

        for counter, target in enumerate(input_file):
            # gets data for plotting
            x_model, y_model, x_data, y_data = get_model_and_data_for_plotting(
                counter, target, source_path, source_filename, flux
            )

            # plotting
            plot_model(x_model, y_model, axs[counter])
            plot_phot(x_data, y_data, axs[counter])

            # set axis limits
            if counter == 0:
                set_limits(x_model, y_model, x_data, y_data, axs[counter])

            # annotations
            if len(input_file) < 4:
                source_name_annotation(target["source"], axs[counter])
            else:
                counter_annotations(counter, axs[counter])

            # ticks
            set_inward_ticks(axs[counter])

        # set ticks for empty cells
        n_empty_cells = len(axs.ravel()) % len(input_file)
        if n_empty_cells == 1:
            set_inward_ticks(axs.ravel()[-1])
        elif n_empty_cells == 2:
            set_inward_ticks(axs.ravel()[-1])
            set_inward_ticks(axs.ravel()[-2])

        # save figure
        plt.subplots_adjust(wspace=0, hspace=0)
        fig.savefig(dest_path + "/" + save_name, dpi=200, bbox_inches="tight")
        plt.close()
    else:
        single_figures(source_path, source_filename, dest_path)


# if __name__ == "__main__":
#     create_fig()
