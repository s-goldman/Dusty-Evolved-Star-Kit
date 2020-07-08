# Steve Goldman, Space Telescope Science Institute, sgoldman@stsci.edu
import math
import ipdb
from tqdm import tqdm
import numpy as np
from copy import deepcopy
from astropy.table import Table, Column, vstack
from desk.set_up import config

# __all__ = ["generate_scaling_factors", "scale_to_full_grid", "create_full_model_grid"]


class instantiate:
    """docstring for create."""

    def __init__(self, grid, grid_dusty, grid_outputs, distance, n):
        self.grid = grid
        self.grid_dusty = grid_dusty
        self.grid_outputs = grid_outputs
        self.distance_norm = math.log10(((float(distance) / 4.8482e-9) ** 2) / 1379)
        self.n = n


def retrieve(full_grid_params):
    def scale_vexp(expansion_velocities, luminosities):
        scaled_expansion_velocities = Column(
            np.array(expansion_velocities) * (np.array(luminosities) / 10000) ** 0.25,
            name="scaled_vexp",
        )
        return scaled_expansion_velocities

    def scale_mdot(mass_loss_rates, luminosities):
        scaled_mdot = Column(
            np.array(mass_loss_rates)
            * ((np.array(luminosities) / 10000) ** 0.75)
            * (config.target["assumed_gas_to_dust_ratio"] / 200) ** 0.5,
            name="scaled_mdot",
        )
        return scaled_mdot

    def generate_scaling_factors(n):
        """
        Creates arrays of model fluxes from lum_min to lum_max.

        Returns
        -------
        scaling_vals : 1D numpy array
            An array of scaling factors that the model grid will be scaled to.
            As the model grids are used to create higher-luminosity models through scaling,
            this sets the different luminosities that each grid will have (i.e. the model
            grid will be appended by the same model grid scaled by each of the values
            in scaling_factors)
        """

        scaling_vals = (
            np.linspace(
                np.log10(config.fitting["lum_min"]),
                np.log10(config.fitting["lum_max"]),
                n,
            )
            - full_grid_params.distance_norm
        )
        return scaling_vals

    def reconfigure_nanni_models(_full_outputs):
        # model_id starts at 1
        _full_outputs.add_column(
            Column(np.arange(1, len(_full_outputs) + 1), name="model_id"), index=0
        )
        # _full_outputs.add_column(
        #     Column([full_grid_params.distance_norm] * len(_full_outputs), name="norm")
        # )
        _full_outputs.rename_columns(
            ["L", "vexp", "mdot"], ["lum", "scaled_vexp", "scaled_mdot"]
        )
        return _full_outputs

    def reconfigure_dusty_models(_full_outputs):

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

    def scale_to_full_grid(scaling_factors):

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
        _grid_outputs = deepcopy(full_grid_params.grid_outputs)
        grid_template = deepcopy(_grid_outputs)

        print(
            "Scaling to full grid ("
            + "{:,}".format((len(grid_template) * len(scaling_factors)))
            + " models)"
        )

        # for each scaling value, create and append a grid
        for i, trial in enumerate(tqdm(scaling_factors)):
            appended_trials = Column(np.full(len(grid_template), trial), name="trial")
            if i == 0:
                _grid_outputs.add_column(appended_trials)
            else:
                add_trials = deepcopy(grid_template)
                add_trials.add_column(appended_trials)
                _grid_outputs = vstack((_grid_outputs, add_trials))
        return _grid_outputs

    def create_full_model_grid(scaling_factors):
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
            for row in full_grid_params.grid_dusty["col1"]:
                scaled_rows.append(row * np.power(10, val))
        scaled_grid = Table([scaled_rows])
        return scaled_grid

    ##################
    if full_grid_params.grid in config.nanni_grids:
        scaling_factors = generate_scaling_factors(1)
        scaled_outputs = scale_to_full_grid(scaling_factors)
        full_outputs = reconfigure_nanni_models(scaled_outputs)
    else:
        scaling_factors = generate_scaling_factors(full_grid_params.n)
        scaled_outputs = scale_to_full_grid(scaling_factors)
        full_outputs = reconfigure_dusty_models(scaled_outputs)

    full_model_grid = create_full_model_grid(scaling_factors)

    return full_outputs, full_model_grid