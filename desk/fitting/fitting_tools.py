import ipdb
import numpy as np
from astropy.table import Table


def trim_grid(data, fit_params):
    """Trims model grid wavelengths and fluxes before fitting.

    Parameters
    ----------
    data : 2-D array
        input data in 2-D array of wavelength and flux.
    fit_params : Class
        fit parameters.

    Returns
    -------
    trimmed_model_wavelength : array
        Trimmed model wavelengths in microns
    trimmed_model_fluxes: astropy Table (1 column, array in each row)
        Trimmed model fluxes in W*M^-2

    """
    data_wavelength_min = np.amin(data[0])
    data_wavelength_max = np.amax(data[0])
    lower_trim_model_index = np.where(
        fit_params.model_wavelength_grid < data_wavelength_min
    )[0][-1]
    upper_trim_model_index = (
        np.where(fit_params.model_wavelength_grid > data_wavelength_max)[0][0] + 1
    )
    trimmed_model_wavelength = fit_params.model_wavelength_grid[
        lower_trim_model_index:upper_trim_model_index
    ]
    trimmed_model_fluxes = Table(
        [
            fit_params.full_model_grid["flux_wm2"][
                :, lower_trim_model_index:upper_trim_model_index
            ]
        ]
    )
    return trimmed_model_wavelength, trimmed_model_fluxes


class fit:

    """
    Fitting tools for least square fit.
    """

    def find_closest(data_wave, model_wave, model_flux):

        """
        Find model fluxes closest in wavelength to data.

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
        closest_model_flux: array
            Subset of model fluxes closest to each wavelength in data.

        """
        closest = np.searchsorted(model_wave, data_wave)
        idx = np.clip(closest, 1, len(model_wave) - 1)
        left = model_wave[idx - 1]
        right = model_wave[idx]
        idx -= data_wave - left < right - data_wave
        closest_model_flux = model_flux[idx]
        return closest_model_flux

    def least2_liklihood(_data, _model):
        """Finds the least-squares fit of the data and model.

        Parameters
        ----------
        _data : array
            Source data in W*M^-2.
        _model : array
            Model fluxes in W*M^-2.

        Returns
        -------
        prob : float
            The probability given the fit.

        """
        # least squares fit
        _stat = np.nansum(np.square(_data - _model) / _model)
        prob = np.exp(-0.5 * np.float128(_stat))
        return prob

    def fit_data(data, model):

        """
        Trims the data, finds the closest match, and returns chi square value.

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
        matched_model = fit.find_closest(data[0], model[0], model[1])
        liklihood = fit.least2_liklihood(data[1], matched_model)

        return liklihood
