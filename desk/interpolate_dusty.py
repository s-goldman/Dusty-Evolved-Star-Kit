import os, sys, pdb
import numpy as np
from astropy.table import Table
from scipy.interpolate import RegularGridInterpolator
from desk import fitting_tools

# Example
# grid_name = "Oss-Orich-bb"
# teff_new = 4010
# tinner_new = 900
# tau_new = 0.146


def interpolate(grid_name, teff_new, tinner_new, tau_new):
    # checks if grid files available
    full_path = str(__file__.replace("interpolate_dusty.py", ""))
    fitting_tools.check_models(grid_name, full_path)
    try:
        output_array = Table.read(
            full_path + "models/" + grid_name + "_outputs.csv", format="csv"
        )
        grid_dusty = Table.read(full_path + "models/" + grid_name + "_models.fits")
        waves = grid_dusty[0][0]
    except:
        raise Exception(
            "Could not find model grid. Please double check input or try another grid. To see available grids use the command: desk grids"
        )
        sys.exit()

    # create interpolator
    tau = np.unique(output_array["odep"])
    teff = np.unique(output_array["teff"])
    tinner = np.unique(output_array["tinner"])

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
        sys.exit()

    # if model already exists
    if (teff_new in teff) & (tinner_new in tinner) & (tau_new in tau):
        print("Model exists:")
        ind = np.where(
            (output_array["teff"] == teff_new)
            & (output_array["tinner"] == tinner_new)
            & (output_array["odep"] == tau_new)
        )[0][0]
        interp_dusty = Table((grid_dusty[ind]["col0"], grid_dusty[ind]["col1"]))
        expansion_velocity = output_array["vexp"][ind]
        mass_loss_rate = output_array["mdot"][ind]

    else:
        print("Interpolating model:")
        array = np.zeros((len(teff), len(tinner), len(tau), len(waves)))
        mass_loss_array = np.zeros((len(teff), len(tinner), len(tau)))
        expansion_velocity_array = np.zeros((len(teff), len(tinner), len(tau)))

        for i in range(0, len(teff)):
            for j in range(0, len(tinner)):
                for k in range(0, len(tau)):
                    mc_index = np.where(
                        (teff[i] == output_array["teff"])
                        & (tinner[j] == output_array["tinner"])
                        & (tau[k] == output_array["odep"])
                    )
                    if np.any(mc_index):
                        array[i][j][k] = grid_dusty[mc_index[0][0]][1]
                        mass_loss_array[i][j][k] = output_array["mdot"][mc_index]
                        expansion_velocity_array[i][j][k] = output_array["vexp"][
                            mc_index
                        ]
        interpolator = RegularGridInterpolator((teff, tinner, tau, waves), array)
        mdot_interpolator = RegularGridInterpolator(
            (teff, tinner, tau), mass_loss_array
        )
        vexp_interpolator = RegularGridInterpolator(
            (teff, tinner, tau), expansion_velocity_array
        )

        interp_array = []
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


if __name__ == "__main__":
    interpolate()
