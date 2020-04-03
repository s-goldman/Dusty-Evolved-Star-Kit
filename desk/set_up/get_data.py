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


def get_values(filename):
    """Retrieves data by reading csv file.

    Parameters
    ----------
    filename : str
        Name of csv file name. The file should have:
            Column 0: wavelength in um
            Column 1: flux in Jy

    Returns
    -------
    2 arrays
        wavelength (x) and flux (y) in unit specified in config.py (default is w/m2)

    """
    table = ascii.read(filename, delimiter=",")
    table.sort(table.colnames[0])
    x = np.array(table.columns[0])
    y = np.array(table.columns[1])
    y = y * u.Jy
    y = y.to(u.W / (u.m * u.m), equivalencies=u.spectral_density(x * u.um))
    log_average_flux_wm2 = np.log10(np.median(y).value)
    return x, np.array(y)


def compile_data(source):
    """Returns array with csv filename or csv filenames in specified directory

    Parameters
    ----------
    source : str
        user input source name

    Returns
    -------
    data: array
        array with 1 or multiple filenames

    """
    # error messages
    class BadFilenameError(ValueError):
        pass

    class BadSourceDirectoryError(ValueError):
        pass

    if fnmatch(source, "*.csv"):
        try:
            with open(source) as f:
                number_of_targets = 1
                data = np.array(source)
        except IOError:
            raise BadFilenameError(source)
    elif os.path.isdir(source):
        source_dir = (source + "/").replace("//", "/")  # if input dir ends in /
        if glob.glob(source_dir + "/*.csv"):
            file_names = glob.glob(source + "/" + "*.csv")
            number_of_targets = len(file_names)
            data = np.array(file_names)
        else:
            raise BadSourceDirectoryError(source)
    else:
        raise BadFilenameError(source)
    return data, number_of_targets
