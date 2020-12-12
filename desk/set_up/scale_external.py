import numpy as np
from astropy.table import Column, Table


def scale_by_distance(_outputs, _models, scaling_factor):
    """Scale external model fluxes and normalization value.

    Parameters
    ----------
    _outputs : astropy table
        grid outputs.
    _models : astropy table
        grid models.
    scaling_factor : float
        Scaling factor to scale grids to distance.

    Returns
    -------
    _outputs : astropy table
        Updated astropy table with scaled vexp, and mdot.
    scaled_models : astropy table
        astropy table with sclaed fluxes

    """
    # get log normalization for model
    _outputs["norm"] = np.log10(_outputs["norm"] / scaling_factor * _outputs["lum"])

    # scale grid_fluxes
    scaled_models = []
    print("Scaling model grid by distance (" + str(len(_models)) + " models)")

    for i, lum_val in enumerate(_outputs["lum"]):
        scaled_flux_array = np.multiply(
            _models["flux_wm2"][i], lum_val / scaling_factor
        )
        scaled_models.append(scaled_flux_array)

    full_models = Table(
        (_models["wavelength_um"], Column(scaled_models, name="flux_wm2"))
    )

    return _outputs, full_models
