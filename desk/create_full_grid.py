import csv
import copy
import math
import ipdb
import numpy as np
from copy import deepcopy
from desk import console_commands, config
from astropy.table import Table, Column, vstack, hstack

__all__ = ["create_full_outputs", "create_full_model_grid", "create_trials"]


def create_trials(distance):
    """Creates arrays of model fluxes normalize to +/- 2.

    Parameters
    ----------
    distance : int
        distance in kpc

    Returns
    -------
    array
        An array of model flux arrays for each normalized value

    """
    distance_norm = math.log10(((float(distance) / 4.8482e-9) ** 2) / 1379)
    lum_min = 10000  # solar luminosities
    lum_max = 200000
    trials = (
        np.linspace(
            np.log10(lum_min), np.log10(lum_max), config.fitting["number_of_tries"]
        )
        - distance_norm
    )
    return trials


def create_full_outputs(_grid_outputs, distance, trials):
    """Returns the input grid for each luminosity in the form of trial
    (scaling factor not including distance; e.g. -12.5, -13.5) specified by trials.
    Also includeds the scled vexp and mass loss rate

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
    type: astropy table
        The input astropy table but appeded to itself for each luminosity.

    """
    distance_norm = math.log10(((float(distance) / 4.8482e-9) ** 2) / 1379)
    grid_template = deepcopy(_grid_outputs)

    for i, trial in enumerate(trials):
        appended_trials = Column(np.full(len(grid_template), trial), name="trial")
        if i == 0:
            _grid_outputs.add_column(appended_trials)
        else:
            add_trials = deepcopy(grid_template)
            add_trials.add_column(appended_trials)
            _grid_outputs = vstack((_grid_outputs, add_trials))

    # adds luminosities
    luminosity = Column(
        np.array(np.power(10.0, distance_norm - _grid_outputs["trial"] * -1)),
        name="lum",
    )

    _grid_outputs.add_column(luminosity.astype(int))

    # adds scaled parameters
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


def create_full_model_grid(grid_dusty, trials):
    """returns model flux grids for each luminosity scaling (trial).

    Parameters
    ----------
    grid_dusty : Astropy table with 1 column with flux grid in each row
        The (un-trimmed) flux grid in w/m^2 for each model, and for each luminosity
    trials : 1D array
        scaling factors.

    Returns
    -------
    type: Astropy table with 1 column with scaled flux grid in each row
        scaled flux grid

    """
    scaled_rows = []
    for i, trial in enumerate(trials):
        for j, row in enumerate(grid_dusty["col1"]):
            scaled_rows.append(row * np.power(10, trial))
    scaled_grid = Table([scaled_rows])
    return scaled_grid
