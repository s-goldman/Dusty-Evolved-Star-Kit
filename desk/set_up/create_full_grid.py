# Steve Goldman, Space Telescope Science Institute, sgoldman@stsci.edu
import math
import ipdb
from tqdm import tqdm
import numpy as np
from copy import deepcopy
from astropy.table import Table, Column, vstack
from desk.set_up import config

__all__ = ["generate_scaling_factors", "create_full_outputs", "create_full_model_grid"]


def generate_scaling_factors(distance, number_of_models):
    """
    Creates arrays of model fluxes from lum_min to lum_max.

    Parameters
    ----------
    distance : float
        Distance to source in Kpc.

    Returns
    -------
    scaling_vals : 1D numpy array
        An array of scaling factors that the model grid will be scaled to.
        As the model grids are used to create higher-luminosity models through scaling,
        this sets the different luminosities that each grid will have (i.e. the model
        grid will be appended by the same model grid scaled by each of the values
        in scaling_factors)
    """

    distance_norm = math.log10(((float(distance) / 4.8482e-9) ** 2) / 1379)
    scaling_vals = (
        np.linspace(
            np.log10(config.fitting["lum_min"]),
            np.log10(config.fitting["lum_max"]),
            number_of_models,
        )
        - distance_norm
    )
    return scaling_vals


def create_full_outputs(_grid_outputs, distance, trials):

    """
    Returns the input grid for each luminosity in the form of trial.
    (scaling factor not including distance; e.g. -12.5, -13.5) specified by trials.
    Also includeds the scled vexp and mass loss rate.

    Parameters
    ----------
    _grid_outputs : astropy table
        model grid.
    distance : int or float
        distance in kpc.
    trials : array
        Array of scaling factors that does not include distance.

    Returns
    -------
    grid_outputs : astropy table
        The input astropy table but appeded to itself for each scaling factor.
        With the added columns for luminosity, scaled mdot, and sclaed vexp

    """

    grid_template = deepcopy(_grid_outputs)
    distance_norm = math.log10(((float(distance) / 4.8482e-9) ** 2) / 1379)

    print(
        "Scaling to full grid ("
        + "{:,}".format((len(grid_template) * len(trials)))
        + " models)"
    )

    # for each scaling value, create and append a grid
    for i, trial in enumerate(tqdm(trials)):
        appended_trials = Column(np.full(len(grid_template), trial), name="trial")
        if i == 0:
            _grid_outputs.add_column(appended_trials)
        else:
            add_trials = deepcopy(grid_template)
            add_trials.add_column(appended_trials)
            _grid_outputs = vstack((_grid_outputs, add_trials))

    # adds luminosity column
    luminosity = Column(
        np.array(np.power(10.0, distance_norm - _grid_outputs["trial"] * -1)),
        name="lum",
    )
    _grid_outputs.add_column(luminosity.astype(int))

    # adds scaled parameters of gas mass loss rate and expansion velocity
    scaled_vexp = Column(
        np.array(_grid_outputs["vexp"])
        * (np.array(_grid_outputs["lum"]) / 10000) ** 0.25,
        name="scaled_vexp",
    )
    scaled_mdot = Column(
        np.array(_grid_outputs["mdot"])
        * ((np.array(_grid_outputs["lum"]) / 10000) ** 0.75)
        * (config.target["assumed_gas_to_dust_ratio"] / 200) ** 0.5,
        name="scaled_mdot",
    )
    _grid_outputs.add_columns([scaled_vexp, scaled_mdot])
    return _grid_outputs


def create_full_model_grid(grid_dusty, scaling_factors):
    """
    Returns model flux grids for each luminosity scaling (scaling_factors).

    Parameters
    ----------
    grid_dusty : Astropy table with 1 column with flux grid in each row
        The (un-trimmed) flux grid in w/m^2 for each model, and for each luminosity
    scaling_factors : 1D array
        scaling factors.

    Returns
    -------
    type: Astropy table with 1 column with scaled flux grid (w m-2) in each row
        scaled flux grid

    """
    scaled_rows = []
    for val in scaling_factors:
        for row in grid_dusty["col1"]:
            scaled_rows.append(row * np.power(10, val))
    scaled_grid = Table([scaled_rows])
    return scaled_grid
