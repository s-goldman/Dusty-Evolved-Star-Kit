import numpy as np
from astropy.table import Column, vstack
from desk.set_up import config


def scale_vexp(expansion_velocities, luminosities):
    """Scales expansion velocity by the luminosity and gas-to-dust ratio see:
    Elitzur & Ivezić 2001, MNRAS, 327, 403
    (https://ui.adsabs.harvard.edu/abs/2001MNRAS.327..403E/abstract)

    Parameters
    ----------
    expansion_velocities : array
        expansion velocities from original model grid.
    luminosities : array
        unique luminosity values created by generate_model_luminosities.

    Returns
    -------
    scaled_expansion_velocities: array
        scaled expansion velocities.

    """

    scaled_expansion_velocities = (
        np.array(expansion_velocities)
        * (np.array(luminosities) / 10000) ** 0.25
        * (config.target["assumed_gas_to_dust_ratio"] / 200) ** (-0.5)
    )
    return scaled_expansion_velocities


def scale_mdot(mass_loss_rates, luminosities):
    """Scales mass loss rates by the luminosity and gas-to-dust ratio see:
    Elitzur & Ivezić 2001, MNRAS, 327, 403
    (https://ui.adsabs.harvard.edu/abs/2001MNRAS.327..403E/abstract)

    Parameters
    ----------
    mass_loss_rates : array
        mass-loss rates from original model grid.
    luminosities : array
        unique luminosity values created by generate_model_luminosities.

    Returns
    -------
    scaled_mdot: array
        scaled mass loss rates.

    """
    scaled_mdot = (
        np.array(mass_loss_rates)
        * ((np.array(luminosities) / 10000) ** 0.75)
        * (config.target["assumed_gas_to_dust_ratio"] / 200) ** 0.5,
    )[0]
    return scaled_mdot


def scale(_outputs, _models, luminosities, scaling_factor):
    """Scale DUSTY models and outputs.

    Parameters
    ----------
    _outputs : astropy table
        grid outputs.
    _models : astropy table
        grid models.
    luminosities : array
        1-D array of luminosities
    scaling_factor : float
        Scaling factor to scale grids to distance.

    Returns
    -------
    full_outputs : astropy table
        Updated astropy table with scaled vexp, and mdot.
    full_model_grid : astropy table
        astropy table with sclaed fluxes

    """
    full_outputs = vstack(([_outputs] * len(luminosities)))

    # create lum col
    lum_col = Column(
        np.ndarray.flatten(np.array([np.full(len(_outputs), x) for x in luminosities])),
        name="lum",
        dtype="int",
    )

    # get log normalization for model
    full_outputs["norm"] = np.log10(full_outputs["norm"] / scaling_factor * lum_col)

    # replace vexps and mdots with scaled values
    scaled_vexp_col = Column(scale_vexp(full_outputs["vexp"], lum_col), "scaled_vexp")
    scaled_mdot_col = Column(scale_mdot(full_outputs["mdot"], lum_col), "scaled_mdot")
    full_outputs.add_columns([lum_col, scaled_vexp_col, scaled_mdot_col])
    full_outputs.remove_columns(["vexp", "mdot"])

    # scale grid_fluxes
    full_model_grid = vstack(
        [(_models["flux_wm2"] / scaling_factor * lum_val) for lum_val in luminosities]
    )

    return full_outputs, full_model_grid
