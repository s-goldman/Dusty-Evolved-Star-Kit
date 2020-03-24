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

__all__ = ["compute_flat_prior_grid_weights"]


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


def compute_flat_prior_grid_weights(masses):
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
    sindxs = np.argsort(masses)

    # Compute the mass bin boundaries
    masses_bounds = compute_bin_boundaries(masses[sindxs])

    # compute the weights = bin widths
    mass_weights = np.empty(len(masses))
    mass_weights[sindxs] = np.diff(masses_bounds)

    # normalize to avoid numerical issues (too small or too large)
    mass_weights /= np.average(mass_weights)

    return mass_weights
