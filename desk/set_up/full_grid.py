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
        # factor to multiply the model flux by to scale flux to a 1 Lsun star at given distance
        # derived using L/Lsun=4*pi*(d/dsun)^2 * F/Fsun
        # Fsun = 1379 W m-2
        self.scaling_factor_flux_to_Lsun = (
            (float(distance) / u.AU.to(u.kpc)) ** 2
        ) / 1379  #
        self.scaling_factor_flux_to_distance = 1379 * ((u.AU.to(u.kpc)) / distance) ** 2
        self.n = n


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

    def generate_model_luminosities(n):

        luminosities = np.logspace(
            np.log10(config.fitting["lum_min"]), np.log10(config.fitting["lum_max"]), n
        )
        return luminosities

    def scale_vexp(expansion_velocities, luminosities):
        """Scales expansion velocity by the luminosity and gas-to-dust ratio see:
        Elitzur & Ivezić 2001, MNRAS, 327, 403
        (https://ui.adsabs.harvard.edu/abs/2001MNRAS.327..403E/abstract)
        """
        scaled_expansion_velocities = Column(
            np.array(expansion_velocities)
            * (np.array(luminosities) / 10000) ** 0.25
            * (config.target["assumed_gas_to_dust_ratio"] / 200) ** (-0.5),
            name="scaled_vexp",
        )
        return scaled_expansion_velocities

    def scale_mdot(mass_loss_rates, luminosities):
        """Scales mass loss rate by the luminosity and gas-to-dust ratio see:
        Elitzur & Ivezić 2001, MNRAS, 327, 403
        (https://ui.adsabs.harvard.edu/abs/2001MNRAS.327..403E/abstract)
        """
        scaled_mdot = Column(
            np.array(mass_loss_rates)
            * ((np.array(luminosities) / 10000) ** 0.75)
            * (config.target["assumed_gas_to_dust_ratio"] / 200) ** 0.5,
            name="scaled_mdot",
        )
        return scaled_mdot

    def scale_dusty_outputs(luminosities):
        # norm is for lum not distance
        # duplicate grid for each luminosity
        _grid_outputs = vstack(([full_grid_params.grid_outputs] * len(luminosities)))

        # create lum col
        lum_col = Column(
            np.ndarray.flatten(
                np.array(
                    [
                        np.full(len(full_grid_params.grid_outputs), x)
                        for x in luminosities
                    ]
                )
            ),
            name="lum",
            dtype="int",
        )
        scaled_vexp_col = scale_vexp(_grid_outputs["vexp"], lum_col)
        scaled_mdot_col = scale_mdot(_grid_outputs["mdot"], lum_col)
        log_norm_factor = Column(
            np.log10(
                lum_col
                * full_grid_params.scaling_factor_flux_to_Lsun
                * full_grid_params.scaling_factor_flux_to_distance
            ),
            name="norm",
        )

        _grid_outputs.add_columns(
            [lum_col, scaled_vexp_col, scaled_mdot_col, log_norm_factor]
        )

        return _grid_outputs

    def scale_models_to_distance():
        distance_scaled_fluxes = Column(
            full_grid_params.grid_dusty["col1"]
            * full_grid_params.scaling_factor_flux_to_distance,
            name="model_flux_wm2",
        )
        return distance_scaled_fluxes

    def scale_models_to_lums(scaled_model_grid, luminosities):
        # duplicate grid for each luminosity
        _grid_dusty = vstack(([scaled_model_grid] * len(luminosities)))
        return _grid_dusty

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

    def reconfigure_dusty_models(_full_outputs):
        """recongfigures dusty grids, allowing for cross-use of desk functions
        with other model grids"""
        # adds luminosity column
        luminosity = Column(
            np.array(
                np.power(
                    10.0, full_grid_params.distance_norm - _full_outputs["trial"] * -1
                )
            ),
            name="lum",
        )
        _full_outputs.add_column(luminosity.astype(int))

        # scale other values by luminosities
        scaled_vexp = scale_vexp(_full_outputs["vexp"], _full_outputs["lum"])
        scaled_mdot = scale_mdot(_full_outputs["mdot"], _full_outputs["lum"])
        _full_outputs.remove_columns(["vexp", "mdot"])
        _full_outputs.add_columns([scaled_vexp, scaled_mdot])
        return _full_outputs

    print(
        "Scaling to full grid ("
        + "{:,}".format((len(full_grid_params.grid_outputs) * full_grid_params.n))
        + " models)"
    )
    if full_grid_params.grid in config.nanni_grids:
        full_model_grid = scale_models_to_distance()
        full_outputs = full_grid_params.grid_outputs
    else:
        # scale DUSTY outputs
        luminosities = generate_model_luminosities(full_grid_params.n)
        full_outputs = scale_dusty_outputs(luminosities)
        full_outputs.remove_columns(["vexp", "mdot"])

        # scale DUSTY models
        scaled_model_grid = scale_models_to_distance()
        full_model_grid = scale_models_to_lums(scaled_model_grid, luminosities)
    return full_outputs, full_model_grid
