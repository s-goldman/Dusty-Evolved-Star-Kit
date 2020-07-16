import ipdb
import numpy as np
from astropy.table import Table
from scipy.interpolate import RegularGridInterpolator
from desk.set_up import get_models

# Example
# grid_name = "Oss-Orich-bb"
# teff_new = 4010
# tinner_new = 900
# tau_new = 0.146


def interpolate(grid_name, distance_in_kpc, teff_new, tinner_new, tau_new):
    # checks if grid files available
    grid_dusty, grid_outputs = get_models.get_model_grid(grid_name)
    waves = grid_dusty[0][0]

    # test = grid_dusty['col1'] * np.power(10, -distance_norm)
    # ipdb.set_trace()

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

    # if model already exists
    if (teff_new in teff) & (tinner_new in tinner) & (tau_new in tau):
        print("Model exists:")
        ind = np.where(
            (grid_outputs["teff"] == teff_new)
            & (grid_outputs["tinner"] == tinner_new)
            & (grid_outputs["odep"] == tau_new)
        )[0][0]
        interp_dusty = Table(
            (grid_dusty[ind]["wavelength_um"], grid_dusty[ind]["flux_wm2"])
        )
        expansion_velocity = grid_outputs["vexp"][ind]
        mass_loss_rate = grid_outputs["mdot"][ind]

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
        y_new = []

        for wavelength in waves:
            y_new.append(interpolator([teff_new, tinner_new, tau_new, wavelength])[0])
        interp_dusty = Table([waves, y_new])
        mass_loss_rate = mdot_interpolator([teff_new, tinner_new, tau_new])[0]
        expansion_velocity = vexp_interpolator([teff_new, tinner_new, tau_new])[0]

    print("\nExpansion velocity = " + "%.2f" % float(expansion_velocity) + " km/s")
    print("Gas mass-loss rate = " + "%.3E" % float(mass_loss_rate) + " Msun/yr\n")

    interp_dusty.write(
        grid_name
        + "_"
        + str(teff_new)
        + "_"
        + str(tinner_new)
        + "_"
        + str(tau_new)
        + ".csv",
        overwrite=True,
    )
