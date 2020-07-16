# Steve Goldman, Space Telescope Science Institute, sgoldman@stsci.edu
import math
import ipdb
from tqdm import tqdm
import numpy as np
import astropy.units as u
from copy import deepcopy
from astropy.table import Table, Column, vstack
from desk.set_up import config


class instantiate:
    """Creates class with parameters needed to scale to the full grids"""

    def __init__(self, grid, grid_dusty, grid_outputs, distance, n):
        self.grid = grid
        self.grid_dusty = grid_dusty
        self.grid_outputs = grid_outputs
        # factor to multiply the model flux by to scale flux to a 1 Lsun star at
        # user-given given distance
        # derived using L/Lsun=4*pi*(d/dsun)^2 * F/Fsun
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


def scale_vexp(expansion_velocities, luminosities):
    """Scales expansion velocity by the luminosity and gas-to-dust ratio see:
    Elitzur & Ivezić 2001, MNRAS, 327, 403
    (https://ui.adsabs.harvard.edu/abs/2001MNRAS.327..403E/abstract)

    Parameters
    ----------
    expansion_velocities : array
        expansion velocities from original model grid.
    luminosities : array
        unique luminosity values created by generate_model_luminosities.

    Returns
    -------
    scaled_expansion_velocities: array
        scaled expansion velocities.

    """

    scaled_expansion_velocities = (
        np.array(expansion_velocities)
        * (np.array(luminosities) / 10000) ** 0.25
        * (config.target["assumed_gas_to_dust_ratio"] / 200) ** (-0.5)
    )
    return scaled_expansion_velocities


def scale_mdot(mass_loss_rates, luminosities):
    """Scales mass loss rates by the luminosity and gas-to-dust ratio see:
    Elitzur & Ivezić 2001, MNRAS, 327, 403
    (https://ui.adsabs.harvard.edu/abs/2001MNRAS.327..403E/abstract)

    Parameters
    ----------
    mass_loss_rates : array
        mass-loss rates from original model grid.
    luminosities : array
        unique luminosity values created by generate_model_luminosities.

    Returns
    -------
    scaled_mdot: array
        scaled mass loss rates.

    """
    scaled_mdot = (
        np.array(mass_loss_rates)
        * ((np.array(luminosities) / 10000) ** 0.75)
        * (config.target["assumed_gas_to_dust_ratio"] / 200) ** 0.5,
    )[0]
    return scaled_mdot


def scale_dusty_outputs(luminosities, grid_outputs, scaling_factor):
    _grid_outputs = vstack(([grid_outputs] * len(luminosities)))

    # create lum col
    lum_col = Column(
        np.ndarray.flatten(
            np.array([np.full(len(grid_outputs), x) for x in luminosities])
        ),
        name="lum",
        dtype="int",
    )

    # scale mass-loss rate and expansion velocity using functions
    scaled_vexp_col = Column(scale_vexp(_grid_outputs["vexp"], lum_col), "scaled_vexp")
    scaled_mdot_col = Column(scale_mdot(_grid_outputs["mdot"], lum_col), "scaled_mdot")
    _grid_outputs["norm"] = _grid_outputs["norm"] / scaling_factor * lum_col
    _grid_outputs.add_columns([lum_col, scaled_vexp_col, scaled_mdot_col])
    _grid_outputs.remove_columns(["vexp", "mdot"])
    return _grid_outputs


def scale_dusty_models(unique_luminosities, _grid, scaling_factor):
    # scale grid_fluxes
    full_grid = [
        (_grid["flux_wm2"] / scaling_factor * lum_val)
        for lum_val in unique_luminosities
    ]

    return vstack(full_grid)


def scale_model_flux_to_distance(grid_outputs, _grid_fluxes):
    # used for nanni and dusty models
    for i in tqdm(range(0, len(grid_outputs["lum"]))):
        _grid_fluxes[i][0] *= grid_outputs["lum"][i]
        grid_outputs["norm"][i] *= grid_outputs["lum"][i]
    return _grid_fluxes


def reconfigure_nanni_models(_full_outputs):
    """reconfigures model grids to work with DESK framework"""
    # model_id starts at 1
    _full_outputs.add_column(
        Column(np.arange(1, len(_full_outputs) + 1), name="model_id"), index=0
    )
    _full_outputs.rename_columns(
        ["L", "vexp", "mdot"], ["lum", "scaled_vexp", "scaled_mdot"]
    )
    return _full_outputs


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

    print(
        "Scaling to full grid ("
        + "{:,}".format((len(full_grid_params.grid_outputs) * full_grid_params.n))
        + " models)"
    )
    if full_grid_params.grid in config.nanni_grids:
        full_model_grid = scale_model_fluxes_to_distance(
            full_grid_params.grid_outputs, full_grid_params.grid_dusty
        )
        full_outputs = full_grid_params.grid_outputs
    else:
        # scale DUSTY outputs
        unique_luminosities = generate_model_luminosities(full_grid_params.n)
        full_outputs = scale_dusty_outputs(
            unique_luminosities,
            full_grid_params.grid_outputs,
            full_grid_params.scaling_factor_flux_to_Lsun,
        )

        # scale DUSTY models
        expanded_grid = scale_dusty_models(
            unique_luminosities,
            full_grid_params.grid_dusty,
            full_grid_params.scaling_factor_flux_to_Lsun,
        )
        # full_model_grid = scale_model_flux_to_distance(full_outputs, expanded_grid)
    full_outputs["norm"] = np.log10(full_outputs["norm"])
    return full_outputs, expanded_grid
