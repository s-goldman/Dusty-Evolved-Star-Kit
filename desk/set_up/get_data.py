# Steve Goldman, Space Telescope Science Institute, sgoldman@stsci.edu
import os
import glob
import ipdb
import numpy as np
import astropy.units as u
from astropy.io.ascii import read
from fnmatch import fnmatch
from desk.set_up import error_messages


def get_values(filename, min_wavelength=0, max_wavelength=1000, fitting=False):
    """
    Reads csv file, convets Jy to Wm2, sorts both by wavelength.
    Returns both as 1D arrays.

    Parameters
    ----------
    filename : str
        Name of csv file name. The file should have: Column 0: wavelength in um, Column 1: flux in Jy
    max_wavelength:float
        The maximum wavelength in um to fit the data.
    min_wavelength:float
        The maximum wavelength in um to fit the data

    Returns
    -------
    x: 1D array
        wavelength in um
    y: 1D array
        flux in w/m2

    """

    table = read(filename, delimiter=",", names=[])
    table.rename_columns((table.colnames[0], table.colnames[1]), ("wavelength", "flux"))
    if fitting == True:
        table = table[
            (table["wavelength"] > float(min_wavelength))
            & (table["wavelength"] < float(max_wavelength))
        ]
        if len(table) < 2:
            print(table)
            raise error_messages.Fitting_Range_Error(
                "\n\nCurrent Range: "
                + str(min_wavelength)
                + " - "
                + str(max_wavelength)
                + " um\n"
            )
    # remove empty fluxes and bad wavelengths
    real_data = table[(table["wavelength"] > 0) & (table["flux"] > 0)]
    real_data.sort(real_data.colnames[0])
    x = np.array(real_data.columns[0])
    y = np.array(real_data.columns[1])
    y = y * u.Jy
    y = y.to(u.W / (u.m * u.m), equivalencies=u.spectral_density(x * u.um))
    return x, np.array(y)


def compile_data(source):

    """
    Returns array with csv filename or csv filenames in specified directory.

    Parameters
    ----------
    source : str
        user input source name

    Returns
    -------
    data: array
        array with 1 or multiple filenames

    """

    # checks if single source with good filename
    if fnmatch(source, "*.csv"):
        try:
            with open(source) as f:
                f.readlines()
                data = np.array([source])
        except IOError:
            raise error_messages.BadFilenameError(source)
    # checks if dir with csv files
    elif os.path.isdir(source):
        source_dir = (source + "/").replace("//", "/")  # if input dir ends in /
        if glob.glob(source_dir + "/*.csv"):
            file_names = glob.glob(source + "/" + "*.csv")
            data = np.array(file_names)
        else:
            raise error_messages.BadSourceDirectoryError(source)
    else:
        raise error_messages.BadFilenameError(source)
    return data
