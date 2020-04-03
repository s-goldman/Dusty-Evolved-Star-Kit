# Steve Goldman, Space Telescope Science Institute, sgoldman@stsci.edu
import os
import sys
import copy
import glob
import time
import ipdb
import math
import numpy as np
import astropy.units as u
from astropy.io import ascii
from fnmatch import fnmatch
from astropy.table import Table, Column


def remove_old_output_files():
    if os.path.exists("fitting_results.txt"):
        os.remove("fitting_results.txt")
    if os.path.exists("fitting_plotting_outputs.txt"):
        os.remove("fitting_plotting_outputs.txt")


def make_output_files_dusty():
    remove_old_output_files()
    with open("fitting_results.csv", "w") as f:
        f.write("source,L,vexp_predicted,teff,tinner,odep,mdot\n")
        f.close()
    with open("fitting_plotting_outputs.csv", "w") as f:
        f.write("target_name,data_file,norm,index,grid_name,teff,tinner,odep\n")
        f.close()


def make_output_files_grams():
    remove_old_output_files()
    with open("fitting_results.csv", "w") as f:
        f.write("source,L,rin,teff,tinner,odep,mdot\n")
        f.close()
    with open("fitting_plotting_outputs.csv", "w") as f:
        f.write("target_name,data_file,norm,index,grid_name,teff,tinner,odep\n")
        f.close()


# for each target, fit spectra with given models (.fits file)
def sed_fitting(model_grid, *args, **kargs):
    # passes arguments to either dusty_fit or grams_fit
    if fnmatch(model_grid, "grams*"):
        raise ValueError("\n\n\n ***Currently Unavailble*** \n")
        # return grams_fit(model_grid, *args, **kargs)
    else:
        return dusty_fit(model_grid, *args, **kargs)
