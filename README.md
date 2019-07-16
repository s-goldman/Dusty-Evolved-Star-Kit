
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
Several grids are **already available** and are located in the _models_ directory (change using the model_grid variable in the config.py file). You can also specify the state-of-the-art dust growth models by [Nanni et al. (2019)](https://ui.adsabs.harvard.edu/abs/2019MNRAS.487..502N/abstract) which are automatically downloaded and used when selected. New grids will include the 2D [GRAMS model grid](https://2dust.stsci.edu/grams_models.cgi) based on the 2DUST code and [DARWIN models](https://arxiv.org/abs/1904.10943).

A module for creating your own [DUSTY](https://github.com/ivezic/dusty) grid is under development, but for now please email me ([Dr. Steven Goldman](http://www.stsci.edu/~sgoldman/)) directly for grid requests or for help with the pacakge. 

Documentation
-------------

The documentation will soon be found on [readthedocs](http://dusty-evolved-star-kit.readthedocs.io/en/latest/).


Install Using Python
-------------------

Install the package with the command `pip install desk` and then import the module with `import desk`. To run the main module, run `desk.sed_fitting.main(['name_of_target_1_data.csv'])` or `desk.sed_fitting.main(['name_of_target_1_data.csv', 'name_of_target_2_data.csv'])` for multiple sources (**Note the brackets**). This will fit the SEDs using the grid and options specified in config.py file or the config dictionary. Additional arguments exist to specify the distance to your targets and the model grid to use: arg_input=*targets*, dist=*distance in kpc*, grid=*name of model grid*. For example:

`desk.sed_fitting.main(['target.csv'], 50, 'H11-LMC')`

You can also select just 'oxygen' or 'carbon' to use the default models. Two results files, a figure of the parameter range, and an optional output_sed.png figure are automatically created. To create the figure you can also run `desk.plotting_seds.create_fig()`.

Command line Use
----------------------
Download on the main Git page (green box at the top of the screen), use `curl  -OL https://github.com/s-goldman/dusty_evolved_star_kit/tarball/master`, or use the command `git clone https://github.com/s-goldman/Dusty-Evolved-Star-Kit.git`

All of the important command line files (.py files) can be found in the `desk` subdirectory.

Just add the csv data files you want to fit to the *put_target_data_here* directory, select your options (shown above) within the config.py script, make sure you are the desk directory, and then use the command `python sed_fit.py`.

<img src="docs/example.png"  width="400" height="500">
This is an example of the output_sed.png file, where three massive oxygen-rich AGB stars from the LMC have been fit.

Oxygen-Rich Model Grids
-------------------
Oss-Orich-aringer (*N*=2,000): Uses warm silicates from [Ossenkopf et al. 1992](https://ui.adsabs.harvard.edu/abs/1992A%26A...261..567O/abstract) and photospheric models from [Aringer et al. 2016](https://ui.adsabs.harvard.edu/abs/2016MNRAS.457.3611A/abstract). Provides ranges in effective temperature (2600-3400 K: 200 K interval) inner dust temperature (600-1200K: 200 K interval) and optical depth (0.1 - 50: 100 spaced logarithmicly). Standard [MRN](https://ui.adsabs.harvard.edu/abs/1977ApJ...217..425M/abstract) grain size distribution from 0.005 - 0.25 microns.

Oss-Orich-bb (*N*=2,000): Same as Oss-Orich-aringer but using black bodies instead of the photospheric models.

Crystalline-20-bb (*N*=2,000): Same as Oss-Orich-bb but using 20% crystalline silicate grains from [Jaeger et al. 1994](https://ui.adsabs.harvard.edu/abs/1994A%26A...292..641J/abstract).

corundum-20-bb (*N*=2,000): Same as Oss-Orich-bb but using 20% corundum grains from [Begemann et al. 1997](https://ui.adsabs.harvard.edu/abs/1997ApJ...476..199B/abstract).

big-grains (*N*=2,000): Same as Oss-Orich-aringer but using a higher maximum dust grain size of 0.35.

fifth-iron (*N*=500): Same as Oss-Orich-aringer but with 20% iron grains from [Henning et al. 1995](https://ui.adsabs.harvard.edu/abs/1995A%26AS..112..143H/abstract), and an effective temperature of 3400 K.

half-iron (*N*=500): Same as Oss-Orich-aringer but with 50% iron grains from [Henning et al. 1995](https://ui.adsabs.harvard.edu/abs/1995A%26AS..112..143H/abstract), and an effective temperature of 3400 K.

one-fifth-carbon (*N*=500): Same as Oss-Orich-aringer but with 20% amorphous carbon grains from [Zubko et al. 1996](https://ui.adsabs.harvard.edu/abs/1996MNRAS.282.1321Z/abstract), and an effective temperature of 3400 K.

arnold-palmer (*N*=2,000): Same as Oss-Orich-aringer but with 50% amorphous carbon grains from [Zubko et al. 1996](https://ui.adsabs.harvard.edu/abs/1996MNRAS.282.1321Z/abstract).


Carbon-Rich Model Grids
-------------------
Zubko-Crich-aringer (*N*=2,000): Same as Oss-Orich-aringer but with amorphous carbon grains from [Zubko et al. 1996](https://ui.adsabs.harvard.edu/abs/1996MNRAS.282.1321Z/abstract).

Zubko-Crich-bb (*N*=2,000): Same as Zubko-Crich-aringer but using black bodies instead of the photospheric models.

arnold-palmer (*N*=2,000): Same as Oss-Orich-aringer but with 50% amorphous carbon grains from [Zubko et al. 1996](https://ui.adsabs.harvard.edu/abs/1996MNRAS.282.1321Z/abstract).



Dust Growth Model Grids from from [Nanni et al. (2019)](https://ui.adsabs.harvard.edu/abs/2019MNRAS.487..502N/abstract)
-------------------

H11-LMC (*N*=90,899): A carbon-rich grid for the LMC metallicity (1/2 solar) using optical constants from [Hanner et al. (1988)](https://ui.adsabs.harvard.edu/abs/1988ioch.rept.....H/abstract).

H11-SMC (*N*=91,058): A carbon-rich grid for the SMC metallicity (1/5 solar) using optical constants from [Hanner et al. (1988)](https://ui.adsabs.harvard.edu/abs/1988ioch.rept.....H/abstract).

J1000-LMC (*N*=85,392): A carbon-rich grid for the LMC metallicity (1/2 solar) using optical constants from [Jager et al. (1998)](https://ui.adsabs.harvard.edu/abs/1998A%26A...332..291J/abstract)

J1000-SMC (*N*=85,546): A carbon-rich grid for the SMC metallicity (1/5 solar) using optical constants from [Jager et al. (1998)](https://ui.adsabs.harvard.edu/abs/1998A%26A...332..291J/abstract)


Attribution
-----------

The method used is similar to that of [Goldman et al. 2017](https://ui.adsabs.harvard.edu/abs/2017MNRAS.465..403G/abstract); a more in-depth publication is in prep.

License
-------

This project is Copyright (c) [Dr. Steven Goldman](http://www.stsci.edu/~sgoldman/) and licensed under
the terms of the BSD 3-Clause license.
