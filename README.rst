======================
Dusty-Evolved-Star-Kit
======================




The DESK is an SED-fitting python package for fitting data from evolved stars
(photometry or spectra) with radiative transfer model grids. The package
is currently in development and all contributions are welcomed. For current
progress, see the 'Issues' tab on the Github_ page. The package is ideal for
fitting small samples of dusty evolved stars. It will soon utilize a
bayesian-fitting strategy with mass-loss rate and luminosity distributions as
inputs (priors), and will provide a better fit to these broader sample
properties.

**Input**: A csv file with the first column as wavelength in um and second column
as flux in Jy. To fit multiple csv files, put them in a directory, and use the
directory name as the input.

**Output**: A csv file including the best fit model and corresponding
stellar parameters, as well as an optional figure of the fit SED.

Available model grids: Several grids are already available upon installation. A range of
other model grids, including state-of-the-art dust-growth models by `Nanni et al. (2019)`_
, are downloaded automatically and used when selected. Descriptions of the model
grids can be found in the Documentation_. A module for creating your own DUSTY_ grid
is under development, but for now, please email me (`Dr. Steven Goldman`_) directly
for potential grid requests or for help with the package.

* Free software: BSD license
* Documentation: https://dusty-evolved-star-kit.readthedocs.io.


* TODO

**Credits**: This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Github: https://github.com/s-goldman/Dusty-Evolved-Star-Kit
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _DUSTY : https://github.com/ivezic/dusty
.. _Documentation : https://dusty-evolved-star-kit.readthedocs.io/en/latest/grids.html
.. _Nanni et al. (2019) : https://ui.adsabs.harvard.edu/abs/ 2019MNRAS.487..502N/abstract
.. _GRAMS : https://2dust.stsci.edu/grams_models.cgi
.. _2DUST : https://2dust.stsci.edu/index.cgi
.. _`Dr. Steven Goldman` : http://www.stsci.edu/~sgoldman/
