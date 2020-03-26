"""
Grid Weights
============
The use of a non-uniformly spaced grid complicates the marginalization
step as the trick of summation instead of integration is used.  But this
trick only works when the grid is uniformly spaced in all dimensions.
If the grid is not uniformly spaced, weights can be used to correct
for the non-uniform spacing.
"""
import numpy as np
import ipdb
from astropy.table import Table, Column

__all__ = ["compute_total_weights"]


def compute_bin_boundaries(tab):
    """
    Computes bin boundaries
    Parameters
    ----------
    tab : numpy array
       centers of each bin
    Returns
    -------
    tab2 : numpy array
       boundaries of the bins
    Note
    ----
    The bin boundaries are defined as the midpoint between each value in tab.
    At the two edges, 1/2 of the bin width is subtractted/added to the
    min/max of tab.
    """
    temp = tab[1:] - np.diff(tab) / 2.0
    tab2 = np.empty(len(tab) + 1)
    tab2[0] = tab[0] - np.diff(tab)[0] / 2.0
    tab2[-1] = tab[-1] + np.diff(tab)[-1] / 2.0
    tab2[1:-1] = temp
    return tab2


def compute_bin_weights(unique_values):
    """
    Computes the mass weights to set a uniform prior on linear mass
    Parameters
    ----------
    masses : numpy vector
        masses
    Returns
    -------
    mass_weights : numpy vector
       weights to provide a constant SFR in linear age
    """
    # sort the initial mass along this isochrone
    indexes = np.argsort(unique_values)

    # Compute the mass bin boundaries
    value_bounds = compute_bin_boundaries(unique_values[indexes])

    # compute the weights = bin widths
    value_weights = np.empty(len(unique_values))
    value_weights[indexes] = np.diff(value_bounds)

    # normalize to avoid numerical issues (too small or too large)
    value_weights /= np.average(value_weights)

    return value_weights


def compute_weights(_grid, _grid_param):
    """Returns grid and prior weigths for given paramters.

    Parameters
    ----------
    _grid : 1D array
        Grid of radiative transfer model paramters

    Returns
    -------
    type: 1D arrays
        grid_weights for parameters
    """

    total_grid_weight = np.zeros(len(_grid), dtype=np.longfloat)
    unique_values = np.unique(_grid[_grid_param])
    grid_weights = compute_bin_weights(unique_values)
    # fill grid weights array
    for idx, _item in enumerate(unique_values):
        _index_grid = np.where(_grid[_grid_param] == unique_values[idx])[0]
        total_grid_weight[_index_grid] = grid_weights[idx]
        total_grid_weight /= np.sum(total_grid_weight)

    return total_grid_weight


def compute_total_weights(_grid, param_array):
    """Computes the total grid weights for the model grid.

    Parameters
    ----------
    param_array : 1D array
        Array of model grid column names

    Returns
    -------
    type : 1D array
        Total normalized grid weights for the model grid

    """
    weights = [compute_weights(_grid, x) for x in param_array]
    total_weights = np.prod(weights, axis=0)
    total_weights /= np.sum(total_weights)
    return total_weights
