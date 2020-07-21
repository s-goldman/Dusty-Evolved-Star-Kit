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


def interpolate(grid_name, distance_in_kpc, luminosity, teff_new, tinner_new, tau_new):
    """A script for returning a model within any grid or returning an interpolated
    model that fits within the given parameter space.

    Parameters
    ----------
    grid_name : str
        Name of grid used.
    distance_in_kpc : float
        Distance in kpc.
    luminosity :
        luminosity of model (in solar luminosities)
    teff_new : int
        Effective temperature of desired grid.
    tinner_new : int
        Inner dust temperature of desired grid.
    tau_new : float
        optical depth specified at 10 microns.

    Returns
    -------
    type : csv file
        File with desired model. Model parameters are printed.

    """
    # scaling factor
    scaling_factor = ((float(distance_in_kpc) / u.AU.to(u.kpc)) ** 2) / 1379

    # checks if grid files available
    grid_dusty, grid_outputs = get_models.get_model_grid(grid_name)
    waves = grid_dusty[0][0]

    # create interpolator
    tau = np.unique(grid_outputs["odep"])
    teff = np.unique(grid_outputs["teff"])
    tinner = np.unique(grid_outputs["tinner"])

    # checks if new values within range
    if (
        (teff.min() <= teff_new <= teff.max())
        & (tinner.min() <= tinner_new <= tinner.max())
        & (tau.min() <= tau_new <= tau.max())
    ):
        pass
    else:
        raise Exception(
            "Interpolation values outside of range. Try values in range:"
            "\n\nGrid: "
            + str(grid_name)
            + "\n\n\tTeff:\t"
            + str(teff.min())
            + " - "
            + str(teff.max())
            + "\n\tTinner:\t "
            + str(tinner.min())
            + " - "
            + str(tinner.max())
            + "\n\tTau:\t "
            + str(tau.min())
            + " - "
            + str(tau.max())
            + "\n"
        )
    # ipdb.set_trace()

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
        scaled_model = Table((grid_dusty[ind]["wavelength_um"], scaled_fluxes))

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

        interp_dusty = []

        for wavelength in waves:
            interp_dusty.append(
                interpolator([teff_new, tinner_new, tau_new, wavelength])[0]
            )

        # unscaled_values
        mass_loss_rate = mdot_interpolator([teff_new, tinner_new, tau_new])[0]
        expansion_velocity = vexp_interpolator([teff_new, tinner_new, tau_new])[0]

        if grid_name in config.nanni_grids:
            pass
        else:
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
