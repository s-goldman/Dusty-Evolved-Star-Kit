# Steve Goldman, Space Telescope Science Institute, sgoldman@stsci.edu
import math
import ipdb
from tqdm import tqdm
import numpy as np
import astropy.units as u
from desk.set_up import config, scale_dusty, scale_external


class instantiate:
    """Creates class with parameters needed to scale to the full grids"""

    def __init__(self, grid, grid_dusty, grid_outputs, distance, n):
        self.grid = grid
        self.grid_dusty = grid_dusty
        self.grid_outputs = grid_outputs
        self.distance = distance
        # factor to multiply the model flux by to scale flux to a 1 Lsun star at
        # user-given given distance
        # derived using L/Lsun=(d/dsun)^2 * F/Fsun
        # Fsun = 1379 W m-2
        self.scaling_factor_flux_to_Lsun = (
            (float(distance) / u.AU.to(u.kpc)) ** 2
        ) / 1379
        self.n = n


def generate_model_luminosities(n):
    """Creates an array of n luminosities from the lum_min and lum_max specified in
    the cofig.py script.

    Parameters
    ----------
    n : int
        number of luminosities to scale grid by.

    Returns
    -------
    luminosities : array
        array of luminosity values.

    """

    luminosities = np.logspace(
        np.log10(config.fitting["lum_min"]), np.log10(config.fitting["lum_max"]), n
    )
    return luminosities


def retrieve(full_grid_params):
    """Creates full scaled grid using data from full_grid_params Class.

    Parameters
    ----------
    full_grid_params : class
        Class using parameters from instantiate class.

    Returns
    -------
    full_outputs : astropy table
        scaled model grid outputs similar to grid_outputs
    full_model_grid : astropy table
        scaled models similar to grid_dusty

    """

    if (
        full_grid_params.grid in config.external_grids
    ) or full_grid_params.grid == "grams":
        full_outputs, full_model_grid = scale_external.scale_by_distance(
            full_grid_params.grid,
            full_grid_params.grid_outputs,
            full_grid_params.grid_dusty,
            full_grid_params.scaling_factor_flux_to_Lsun,
            full_grid_params.distance,
        )
    else:
        # scale DUSTY outputs
        print(
            "Scaling to full grid ("
            + "{:,}".format((len(full_grid_params.grid_outputs) * full_grid_params.n))
            + " models)"
        )
        unique_luminosities = generate_model_luminosities(full_grid_params.n)
        full_outputs, full_model_grid = scale_dusty.scale(
            full_grid_params.grid_outputs,
            full_grid_params.grid_dusty,
            unique_luminosities,
            full_grid_params.scaling_factor_flux_to_Lsun,
        )

    return full_outputs, full_model_grid
