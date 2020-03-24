"""
Grid and Prior Weights
============
The use of a non-uniformly spaced grid complicates the marginalization
step as the trick of summation instead of integration is used.  But this
trick only works when the grid is uniformaly spaced in all dimensions.
If the grid is not uniformally spaced, weights can be used to correct
for the non-uniform spacing.
Basically, we want the maginalization using these grid weights to provide
flat priors on all the fit parameters.  Non-flat priors will be implemented
with prior weights.
"""
import numpy as np
from compute_grid_weights import *
import ipdb

__all__ = ["compute_mass_loss_tau_vexp_weights"]


def compute_mass_loss_tau_vexp_weights(_grid):
    """Returns grid and prior weigths for mass loss rate, optical depth, and
    expansion velosity.

    Parameters
    ----------
    _grid : 2D array
        Grid of radiative transfer model paramters

    Returns
    -------
    type: 3 1D arrays
        3 arrays for the three paramters
    """

    total_mdot_grid_weight = np.zeros(len(_grid))
    total_odep_grid_weight = np.zeros(len(_grid))
    total_vexp_grid_weight = np.zeros(len(_grid))

    unique_mdot = np.unique(_grid["mdot"])
    unique_odep = np.unique(_grid["odep"])
    unique_vexp = np.unique(_grid["vexp"])

    grid_weights_mdot = compute_flat_prior_grid_weights(unique_mdot)
    grid_weights_odep = compute_flat_prior_grid_weights(unique_odep)
    grid_weights_vexp = compute_flat_prior_grid_weights(unique_vexp)

    # fill mass loss grid weights array
    for mdx, _item in enumerate(unique_mdot):
        _index_grid_mdot = np.where(_grid["mdot"] == unique_mdot[mdx])[0]
        total_mdot_grid_weight[_index_grid_mdot] = grid_weights_mdot[mdx]

    # fill optical depth grid weights array
    for odx, _item in enumerate(unique_odep):
        _index_grid_odep = np.where(_grid["odep"] == unique_odep[odx])[0]
        total_odep_grid_weight[_index_grid_odep] = grid_weights_odep[odx]

    # fill expansion velocity grid weights array
    for vdx, _item in enumerate(unique_vexp):
        _index_grid_vexp = np.where(_grid["vexp"] == unique_vexp[vdx])[0]
        total_vexp_grid_weight[_index_grid_vexp] = grid_weights_vexp[vdx]

    total_mdot_grid_weight /= np.sum(total_mdot_grid_weight)
    total_odep_grid_weight /= np.sum(total_odep_grid_weight)
    total_vexp_grid_weight /= np.sum(total_vexp_grid_weight)

    return total_mdot_grid_weight, total_odep_grid_weight, total_vexp_grid_weight
