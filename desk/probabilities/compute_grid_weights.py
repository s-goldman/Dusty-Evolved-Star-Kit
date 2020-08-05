import numpy as np
import ipdb

__all__ = ["grid_weights"]


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
    At the two edges, 1/2 of the bin width is subtracted/added to the
    min/max of tab.
    """
    temp = tab[1:] - np.diff(tab) / 2.0
    tab2 = np.empty(len(tab) + 1)
    tab2[0] = tab[0] - np.diff(tab)[0] / 2.0
    tab2[-1] = tab[-1] + np.diff(tab)[-1] / 2.0
    tab2[1:-1] = temp
    return tab2


def compute_weights(mets):
    """
    Computes the metallicity weights to set a uniform prior on linear metallicity.
    Parameters
    ----------
    mets : numpy vector
        metallicities
    Returns
    -------
    metallicity_weights : numpy vector
       weights to provide a flat metallicity
    """
    # sort the initial mass along this isochrone
    sindxs = np.argsort(mets)

    # Compute the mass bin boundaries
    mets_bounds = compute_bin_boundaries(mets[sindxs])

    # compute the weights = bin widths
    mets_weights = np.empty(len(mets))
    mets_weights[sindxs] = np.diff(mets_bounds)

    # normalize to avoid numerical issues (too small or too large)
    mets_weights /= np.average(mets_weights)

    return mets_weights


def grid_weights(param_array):
    """The use of a non-uniformly spaced grid complicates the marginalization
    step as the trick of summation instead of integration is used.  But this
    trick only works when the grid is uniformly spaced in all dimensions.
    If the grid is not uniformly spaced, weights can be used to correct
    for the non-uniform spacing.

    Parameters
    ----------
    param_array : class
        Information needed for generating grid weights.

    Returns
    -------
    grid_weights : array
        1D array of grid weights. 

    """
    grid_weights = np.zeros(len(param_array))
    unique_vals = np.unique(param_array)
    weights = compute_weights(unique_vals)
    for i, val in enumerate(unique_vals):
        ind = np.where(param_array == val)
        grid_weights[ind] = weights[i]
    return grid_weights
