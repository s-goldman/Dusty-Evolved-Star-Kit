import numpy as np
from desk.fitting import fitting_tools


def test_find_closest():
    """
    Test: find model flux closest in wavelength to data
    """
    model_wave = np.array([3, 4, 5, 6, 7, 8, 9, 10])
    data_wave = np.array([1, 4.4, 6.5, 6.6, 40])
    model_flux = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
    closest_fluxes = fitting_tools.fit.find_closest(data_wave, model_wave, model_flux)
    expected_closest_fluxes = np.array([0.1, 0.2, 0.5, 0.5, 0.8])
    np.testing.assert_allclose(
        closest_fluxes,
        expected_closest_fluxes,
        err_msg=("Closest model flux in wavelength error"),
    )


def test_fit_data():
    """
    Test: trim, find closest, return chi_square value
    """
    model = np.array(
        [
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
        ]
    )
    data = np.array([[2, 3, 6.5, 8.9, 9.9], [0.1, 0.2, 0.3, 0.4, 0.5]])
    chi_sq = fitting_tools.fit.fit_data(data, model)
    expected_chi_sq = 0.6571511212387309428
    np.testing.assert_allclose(
        chi_sq, expected_chi_sq, err_msg=("Fitting routine error")
    )
