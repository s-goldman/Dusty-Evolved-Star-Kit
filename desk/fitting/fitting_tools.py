import ipdb
import numpy as np


class fit:

    """
    Fitting tools for least square fit.
    """

    def trim(data, model_trim):

        """
        Removes data outside of wavelegth range of model grid.

        Parameters
        ----------
        data : 2-D array
            input data in 2-D array of wavelength and flux.
        model_trim : type
            input model in 2-D array of wavelength and flux.

        Returns
        -------
        model_trimmed_wavelengths : array
            Trimmed model wavelengths in microns
        model_trimmed_fluxes: array
            Trimmed model fluxes in W*M^-2
        """
        indexes = np.where(
            np.logical_and(
                model_trim[0] >= np.min(data[0]), model_trim[0] <= np.max(data[0])
            )
        )
        model_trimmed_wavelengths = model_trim[0][indexes]
        model_trimmed_fluxes = model_trim[1][indexes]

        return model_trimmed_wavelengths, model_trimmed_fluxes

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
        trimmed_model_wave, trimmed_model_flux = fit.trim(data, model)
        matched_model = fit.find_closest(
            data[0], trimmed_model_wave, trimmed_model_flux
        )
        liklihood = fit.least2_liklihood(data[1], matched_model)
        # ipdb.set_trace()
        return liklihood
