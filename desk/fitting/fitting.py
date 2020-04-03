import csv
import copy
import math
import ipdb
import numpy as np
from desk import console_commands, config
from astropy.table import Table, Column, vstack, hstack


class fit:
    """Fitting tools for least square fit"""

    def trim(data, model_trim):
        """Removes data outside of wavelegth range of model grid.

        Parameters
        ----------
        data : 2-D array
            input data in 2-D array of wavelength and flux.
        model_trim : type
            input model in 2-D array of wavelength and flux.

        Returns
        -------
        2-D array
            Trimmed input model in 2-D array of wavelength and flux.

        """
        indexes = np.where(
            np.logical_and(
                model_trim[0] >= np.min(data[0]), model_trim[0] <= np.max(data[0])
            )
        )
        return model_trim[0][indexes], model_trim[1][indexes]

    def find_closest(data_wave, model_wave, model_flux):
        """Find model values corresponding to the closest values in the data

        Parameters
        ----------
        data_wave : 1-D array
            wavelengths of data in microns.
        model_wave : 1-D array
            wavelengths of model in microns.
        model_flux : 1-D array
            scaled flux of model in W M-2

        Returns
        -------
        closest_data_flux: array
            Array of the closest data wavelength values, to the model wavelength values.

        """
        idx = np.searchsorted(model_wave, data_wave)
        idx = np.clip(idx, 1, len(model_wave) - 1)
        left = model_wave[idx - 1]
        right = model_wave[idx]
        idx -= data_wave - left < right - data_wave
        closest_data_flux = model_flux[idx]
        return closest_data_flux

    def least2(data, model_l2):
        # least squares fit
        stat = np.nansum(np.square(data - model_l2) / model_l2)
        return stat

    def fit_data(data, model):
        """trims the data, finds the closest match, and returns chi square value

        Parameters
        ----------
        data : 2D array
            Data with wavelength in microns and flux in W M-2
        model : 2D array
            model with wavelength in microns and scaled flux in W M-2

        Returns
        -------
        stats: float
            chi square value.

        """
        trimmed_wave, trimmed_flux = fit.trim(data, model)
        matched_model = fit.find_closest(data[0], trimmed_wave, trimmed_flux)
        stats = fit.least2(data[1], matched_model)
        return stats
