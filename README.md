
Dusty-Evolved-Star-Kit<img align="left" width="100" height="100" src="docs/the_desk.png">
=========================================================================================
[![pypi](https://img.shields.io/badge/pypi-DESK-blue.svg)](https://pypi.org/project/desk/)
[![Documentation Status](https://readthedocs.org/projects/dusty-evolved-star-kit/badge/?version=latest)](https://dusty-evolved-star-kit.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://travis-ci.org/s-goldman/Dusty-Evolved-Star-Kit.svg?branch=master)](https://travis-ci.org/s-goldman/Dusty-Evolved-Star-Kit)
[![arXiv paper](https://img.shields.io/badge/arXiv-1610.05761-blue.svg)](https://arxiv.org/abs/1610.05761)
[![Steve Goldman](https://img.shields.io/badge/STScI-Steve%20Goldman-blue.svg)](http://www.stsci.edu/~sgoldman/)

The DESK is an SED-fitting python scripts for fitting data from evolved stars (photometry or spectra) with [DUSTY](https://github.com/ivezic/dusty) 1-D radiative transfer models.
The package is currently in development and all contributions are welcomed. For current progress, see the Issues tab at the top of the page.

**Input**: A csv with the first column as wavelength in um and second column as flux in Jy or W m2, which can be specified (File can have other columns).

**Output**: Two results files including the best fit model and corresponding stellar parameters, as well as an optional figure of the fit SED.

**Options**: In the sed_fitting.py you can specify:
 * model grid
 * distance (in kpc)
 * gas-to-dust ratio
 * the wavelength range to fit
 * output units (Jy or W m2)

**Available model grids**:
Several grids are **already available** and are located in the _models_ directory (change using the model_grid variable in the config.py file). You can also specify the state-of-the-art dust growth models by Nanni et al. (2019) which are automatically downloaded and used when selected. New grids will include the 2D [GRAMS model grid](https://2dust.stsci.edu/grams_models.cgi) based on the 2DUST code and 3D [DARWIN models](https://arxiv.org/abs/1904.10943).

_Update (15 Apr 2019): Starkey site currently down: Nanni et al. (2019) models currently unavailable_

A module for creating your own [DUSTY](https://github.com/ivezic/dusty) grid is under development, but for now please email me ([Dr. Steven Goldman](http://www.stsci.edu/~sgoldman/)) directly for grid requests or for help with the pacakge. 

Documentation
-------------

The documentation will soon be found on [readthedocs](http://dusty-evolved-star-kit.readthedocs.io/en/latest/).


Install Using Python
-------------------

Install the package with the command `pip install desk` and then import the module with `import desk`. To run the main module run `desk.sed_fitting.main(['name_of_target_1_data.csv'])` or `desk.sed_fitting.main(['name_of_target_1_data.csv', 'name_of_target_2_data.csv'])` for multiple sources. This will fit the SEDs using the grid and options specified in config.py file or the config.xxxx dictionary. Two results files, a figure of the parameter range, and an optional output_sed.png figure are automatically created. To create the figure you can also run `desk.plotting_seds.create_fig()`.

Command line Use
----------------------
Download on the main Git page (green box at the top of the screen) or use the command `git clone https://github.com/s-goldman/Dusty-Evolved-Star-Kit.git`

All of the important command line files (.py files) can be found in the `desk` subdirectory.

Just add the csv data files you want to fit to the *put_target_data_here* directory, select your options (shown above) within the config.py script, and then use the command `python sed_fitting.py`.

<img src="docs/example.png"  width="400" height="500">
This is an example of the output_sed.png file, where three massive oxygen-rich AGB stars from the LMC have been fit.

Attribution
-----------

The method used is similar to that of [Goldman et al. 2017](https://ui.adsabs.harvard.edu/abs/2017MNRAS.465..403G/abstract); a more in-depth publication is in prep.

License
-------

This project is Copyright (c) [Dr. Steven Goldman](http://www.stsci.edu/~sgoldman/) and licensed under
the terms of the BSD 3-Clause license.
