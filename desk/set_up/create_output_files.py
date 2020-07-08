# Steve Goldman, Space Telescope Science Institute, sgoldman@stsci.edu
import os
from desk.set_up import config


def remove_old_output_files():
    # removes results file from previous run
    if os.path.exists("fitting_results.txt"):
        os.remove("fitting_results.txt")


def make_output_files_dusty(fit_params):
    # Removes and then creates output file for run
    remove_old_output_files()
    if fit_params.grid in config.nanni_grids:
        with open("fitting_results.csv", "w") as f:
            f.write(
                "source , model_id, mdot, M, teff, L, Cex, CO, Zi, tinner, dmdt_c, dmdt_sic, dmdt_ir, vexp, vmax, tauV, tau1, tauK, odep, tau11, spectrum, ogleU, ogleB, ogleV, ogleI, BesU, BesB, BesV, BesR, BesI, denisI, denisJ, denisK, irsfJ, irsfH, irsfK, esoJ, esoH, esoK, esoL, 2massJ, 2massH, 2massK, saaoJ, saaoH, saaoK, saaoL, caspiJ, caspiH, caspiK, caspiL, irac36, irac45, irac58, irac80, mips24, mips70, iras12, iras25, iras60, WISE1, WISE2, WISE3, WISE4, AkarN3, AkarS7, AkaS9W, AkaS11, AkaL15, AkL18W, AkaL24, calw1, calw2, calw7, calw10, MSXA, MACHOB, MACHOR, grid, norm, file_name\n"
            )
            f.close()

    else:
        with open("fitting_results.csv", "w") as f:
            f.write(
                "source, grid, teff, tinner, model_id, odep, norm, L, vexp,mdot, file_name\n"
            )
            f.close()
