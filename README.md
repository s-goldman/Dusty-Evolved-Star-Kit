
Dusty-Evolved-Star-Kit<img align="left" width="100" height="100" src="docs/the_desk.png">
=========================================================================================
[![Documentation Status](https://img.shields.io/badge/pypi-DESK-blue.svg)](https://pypi.org/project/desk/)
[![Documentation Status](https://readthedocs.org/projects/dusty-evolved-star-kit/badge/?version=latest)](https://dusty-evolved-star-kit.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://travis-ci.org/s-goldman/Dusty-Evolved-Star-Kit.svg?branch=master)](https://travis-ci.org/s-goldman/Dusty-Evolved-Star-Kit)
[![arXiv paper](https://img.shields.io/badge/arXiv-1610.05761-blue.svg)](https://arxiv.org/abs/1610.05761)


The DESK is an SED-fitting python scripts for fitting data from evolved stars (photometry or spectra) with [DUSTY](https://github.com/ivezic/dusty) 1-D radiative transfer models.
The package is currently in development and all contributions are welcomed. For current progress, see the Issues tab at the top of the page. The DESK currently contains scripts for:
1. Converting the output files from DUSTY to two fits files
2. Least square fitting of the models to data
3. Plotting the results

**Input**: A csv with the first column as wavelength in um and second column as flux in Jy or W m2 (File can have other columns).

**Output**: Results file specifying the best fit model parameters, as well as a results file with specifics for plotting the output.

**Options**: In the sed_fitting.py you can specify:
 * model grid
 * distance (in kpc)
 * the wavelength range to fit
 * normalizations range for fitting
 * binning of the normalization range

**Available model grids**:
Several grids are **already available** and are located in the _models_ directory (change using the model_grid variable in the config.py file), but you can also create your own model grid or download the state-of-the-art dust growth models by Nanni et al. (2019).

_Update (15 Apr 2019): Starkey site currently down: Nanni et al. (2019) models currently unavailable_

To create your own [DUSTY](https://github.com/ivezic/dusty) grid:
1. Run dusty
2. Put all outputs (spectra files .s* and output files *.out) into a directory of the same name (see example grid directories)
3. Run the dusty_to_grid.py script

This will create two fits files containing all spectra (*directoryname*_models.fits), and all outputs (*directoryname*_outputs.fits).

Documentation
-------------

The documentation will soon be found on [readthedocs](http://dusty-evolved-star-kit.readthedocs.io/en/latest/).


Installing the DESK
-------------------

Clone the github repository using `git clone https://github.com/s-goldman/Dusty-Evolved-Star-Kit.git`.

Fitting with the DESK
----------------------

All of the important script files can be found in "/dusty-evolved-star-kit/python_scripts"

Just add the csv data files you want to fit to the *put_target_data_here* directory, select your options (shown above) within the config.py script, and then run sed_fitting.py in python.

<img src="docs/example.png"  width="400" height="500">

Attribution
-----------

The method used is similar to that of [Goldman et al. 2017](https://ui.adsabs.harvard.edu/abs/2017MNRAS.465..403G/abstract); a more in-depth publication is in prep.

License
-------

This project is Copyright (c) [Dr. Steven Goldman](http://www.stsci.edu/~sgoldman/) and licensed under
the terms of the BSD 3-Clause license.
