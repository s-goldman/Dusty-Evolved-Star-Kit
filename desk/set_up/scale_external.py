import numpy as np
from fnmatch import fnmatch
from astropy.table import Column, Table


def scale_by_distance(_grid_name, _outputs, _models, scaling_factor, distance):
    """Scale external model fluxes and normalization value.

    Parameters
    ----------
    _grid_name : str
        name of grid specified
    _outputs : astropy table
        grid outputs.
    _models : astropy table
        grid models.
    scaling_factor : float
        Scaling factor to scale grids to distance.
    distance :
        distance in kpc

    Returns
    -------
    _outputs : astropy table
        Updated astropy table with scaled vexp, and mdot.
    scaled_models : astropy table
        astropy table with sclaed fluxes

    """

    print("Scaling model grid by distance (" + str(len(_models)) + " models)")

    if fnmatch(_grid_name, "grams*"):
        # Norm is the log normalization for plotting GRAMS
        _outputs["norm"] = np.log10(
            _outputs["norm"] * np.square(50) / np.square(distance)
        )
        scaled_models = _models["flux_wm2"] * np.power(10, _outputs["norm"][0])
        if (distance < 20) | (distance > 150):
            print(
                "\n"
                + "=" * 75
                + "\nWARNING:\n"
                + "\nThis is beyond the suggested range (20-150 kpc) "
                + "for using the GRAMS grids.\n"
                + "This may result in unrealistic geometries.\n\n"
                + "=" * 75
            )

    else:
        # Norm is the log normalization for plotting Nanni et al. models
        _outputs["norm"] = np.log10(_outputs["norm"] / scaling_factor * _outputs["lum"])
        scaled_models = []
        for i, lum_val in enumerate(_outputs["lum"]):
            scaled_flux_array = np.multiply(
                _models["flux_wm2"][i], lum_val / scaling_factor
            )
            scaled_models.append(scaled_flux_array)

    full_models = Table(
        (_models["wavelength_um"], Column(scaled_models, name="flux_wm2"))
    )

    return _outputs, full_models
