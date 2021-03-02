import ipdb
import numpy as np
import astropy.units as u
from astropy.table import Table
from scipy.interpolate import RegularGridInterpolator
from desk.set_up import get_models, scale_dusty, config

# Example
# grid_name = "Oss-Orich-bb"
# teff_new = 4010
# tinner_new = 900
# tau_new = 0.146


def check_input_range(
    grid_name, unique_teff, unique_tinner, unique_tau, teff_new, tinner_new, tau_new
):
    """Checks if the user-inputted model values are within the range of the model
    grid. This is critical for the interpolation.

    Parameters
    ----------
    gridname : str
        Name of model grid.
    unique_teff : array
        Unique effective temperatures within the model grid.
    unique_tinner : type
        Unique inner dust temperatures within the model grid.
    unique_tau : type
        Unique effective temperatures within the modelgrid.
    teff_new : type
        User-defined effective temperature.
    tinner_new : type
        User-defined inner dust temperature.
    tau_new : type
        User-defined optical depth at 10 microns.

    Returns
    -------
    Error
        Raises exception if outside of the model ranges of effective temperature,
        inner dust temperature or optical depth at 10 microns.

    """

    # checks if new values within range
    if (
        (unique_teff.min() <= teff_new <= unique_teff.max())
        & (unique_tinner.min() <= tinner_new <= unique_tinner.max())
        & (unique_tau.min() <= tau_new <= unique_tau.max())
    ):
        pass
    else:
        raise Exception(
            "Interpolation values outside of range. Try values in range:"
            "\n\nGrid: "
            + str(grid_name)
            + "\n\n\tTeff:\t"
            + str(unique_teff.min())
            + " - "
            + str(unique_teff.max())
            + "\n\tTinner:\t "
            + str(unique_tinner.min())
            + " - "
            + str(unique_tinner.max())
            + "\n\tTau:\t "
            + str(unique_tau.min())
            + " - "
            + str(unique_tau.max())
            + "\n"
        )


def interpolate(grid_name, luminosity, teff_new, tinner_new, tau_new, distance_in_kpc):
    """A script for returning a model within any grid or returning an interpolated
    model that fits within the given parameter space. The interpolation interpolates
    over the flux at each wavelength in the model grid.

    Parameters
    ----------
    grid_name : str
        Name of grid used.
    luminosity :
        luminosity of model (in solar luminosities)
    teff_new : int
        Effective temperature of desired grid.
    tinner_new : int
        Inner dust temperature of desired grid.
    tau_new : float
        optical depth specified at 10 microns.
    distance_in_kpc : float
        Distance in kpc.

    Returns
    -------
    type : csv file
        File with desired model. Model parameters are printed.

    """

    # Not available yet for external model grids (grids too large)
    if (grid_name in config.external_grids) | (grid_name == "desk-mix"):
        raise Exception("Currently unavailable for external model grids.")

    # scaling factor
    scaling_factor = ((float(distance_in_kpc) / u.AU.to(u.kpc)) ** 2) / 1379

    # gets models
    grid_dusty, grid_outputs = get_models.get_model_grid(grid_name)
    waves = grid_dusty[0][0]

    # create interpolator
    tau = np.unique(grid_outputs["odep"])
    teff = np.unique(grid_outputs["teff"])
    tinner = np.unique(grid_outputs["tinner"])

    check_input_range(grid_name, teff, tinner, tau, teff_new, tinner_new, tau_new)

    # if model already exists
    if (teff_new in teff) & (tinner_new in tinner) & (tau_new in tau):
        print("Model exists:")
        ind = np.where(
            (grid_outputs["teff"] == teff_new)
            & (grid_outputs["tinner"] == tinner_new)
            & (grid_outputs["odep"] == tau_new)
        )[0][0]
        mass_loss_rate = scale_dusty.scale_mdot(grid_outputs["mdot"][ind], luminosity)
        expansion_velocity = scale_dusty.scale_vexp(
            grid_outputs["vexp"][ind], luminosity
        )
        scaled_fluxes = grid_dusty[ind]["flux_wm2"] * luminosity / scaling_factor
        scaled_model = Table(
            (grid_dusty[ind]["wavelength_um"], scaled_fluxes),
            names=("wavelength_um", "flux_wm2"),
        )

    else:
        print("Interpolating model:")
        array = np.zeros((len(teff), len(tinner), len(tau), len(waves)))
        mass_loss_array = np.zeros((len(teff), len(tinner), len(tau)))
        expansion_velocity_array = np.zeros((len(teff), len(tinner), len(tau)))

        for i, _ in enumerate(teff):
            for j, _ in enumerate(tinner):
                for k, _ in enumerate(tau):
                    mc_index = np.where(
                        (teff[i] == grid_outputs["teff"])
                        & (tinner[j] == grid_outputs["tinner"])
                        & (tau[k] == grid_outputs["odep"])
                    )
                    if np.any(mc_index):
                        array[i][j][k] = grid_dusty[mc_index[0][0]][1]
                        mass_loss_array[i][j][k] = grid_outputs["mdot"][mc_index]
                        expansion_velocity_array[i][j][k] = grid_outputs["vexp"][
                            mc_index
                        ]
        interpolator = RegularGridInterpolator((teff, tinner, tau, waves), array)
        mdot_interpolator = RegularGridInterpolator(
            (teff, tinner, tau), mass_loss_array
        )
        vexp_interpolator = RegularGridInterpolator(
            (teff, tinner, tau), expansion_velocity_array
        )

        # interpolate model fluxes
        interp_dusty = []
        for wavelength in waves:
            interp_dusty.append(
                interpolator([teff_new, tinner_new, tau_new, wavelength])[0]
            )

        # unscaled_values
        mass_loss_rate = mdot_interpolator([teff_new, tinner_new, tau_new])[0]
        expansion_velocity = vexp_interpolator([teff_new, tinner_new, tau_new])[0]

        # scale dusty models
        mass_loss_rate = scale_dusty.scale_mdot(mass_loss_rate, luminosity)
        expansion_velocity = scale_dusty.scale_vexp(expansion_velocity, luminosity)
        scaled_fluxes = np.array(interp_dusty) * luminosity / scaling_factor

        scaled_model = Table(
            [waves, scaled_fluxes], names=("wavelength_um", "flux_wm2")
        )

    print("\nExpansion velocity = " + "%.2f" % float(expansion_velocity) + " km/s")
    print("Gas mass-loss rate = " + "%.3E" % float(mass_loss_rate) + " Msun/yr\n")

    scaled_model.write(
        grid_name
        + "_"
        + str(luminosity)
        + "_"
        + str(teff_new)
        + "_"
        + str(tinner_new)
        + "_"
        + str(tau_new)
        + ".csv",
        overwrite=True,
    )
