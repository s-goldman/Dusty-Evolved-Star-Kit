=====
Usage
=====

SED-Fitting
-----------

The Dusty-Evolved-Star-Kit can fit the spectra and photometry of evolved stars
with both carbon- and oxygen-rich grids of radiative transfer models.
This enables easy comparison of grids of models and different samples.

The input for this package is a csv file with wavelength in microns in the first
column, and flux in Jy in the second column.

After installation with pip, in any command line prompt, use the command:

.. code-block:: console

	> desk grids

This will display the available grids for fitting. Next you need to point the
package to your csv file, and specify the distance and grid of choice:

.. code-block:: console

	> desk fit --source='target_name.csv' --distance=50 --grid='H11-LMC'

or specify a directory with multiple csv files:

.. code-block:: console

	> desk fit --source='folder_of_csvs' --distance=30 --grid='Oss-Orich-bb'


Additional options
------------------

Users can also specify any-and-all of the following additional options. Requests
for more additional features can be submitted through the `issues`_ tab on the
`Github`_ page.

Grid density
============

.. code-block:: console

	> desk fit --source='target_name.csv' --n=200

The strength of the 1D
DUSTY models is that they can be scaled to create more luminous models. The DESK
takes the initial grid and scales it n times (default: 50) to create a larger
denser grid of sources within the luinosity limits (default: 1,000 - 150,000 Msun).
As the shape of the model is the same for each scaling of the grid, the distance to
the source(s) is important for an accurate results. A more realistic Bayesian method
of fitting is under development.

Wavelength range
================
.. code-block:: console

	> desk fit --source='target_name.csv' --min_wavelength=0.1 --max_wavelength=30
The user may also specify a wavelength minimum and maximum. This will still show
the full photometry in the final SED figure, but fit only the wavelength range
specified.


Multiprocessing
===============
The user can specify whether to fit using multiprocessing
(using all but 1 computer cores), single core fitting (multiprocessing=False), or
specify the number of cores to use (multiprocessing=6).
Multiprocessing uses a core per source, and will have little affect on small samples
or individual sources:

.. code-block:: console

	> desk fit --source='target_name.csv' --multiprocessing=True

Outputs
-------
.. image:: ./example.png
	:width: 400
	:alt: SED example

This is an example of the output_sed.png file fitting three massive oxygen-rich
AGB stars from the LMC. To produce individual figures subsequently run the command:

.. code-block:: console

	> desk sed_indiv


Use in Python Environment
-------------------------

SED-fitting can be done with the DESK within the python environment. To do this
simply import the package and use the 'fit' function in a similar manner as the
console commands.


.. code-block:: console

	>>> import desk
	>>> fit(source="target.csv", distance=3, grid="oxygen")

One can also use the sed, save_model, and grids in a similar fashion.

.. code-block:: console

	>>> sed()
	>>> grids()
	>>> save_model("Oss-Orich-bb", 10000, 2700, 1000, 0.4, 50)
	>>> save_model(grid_name="Oss-Orich-bb", luminosity=10000, teff=2700, tinner=1000, tau=0.4, distance_in_kpc=50)


Package Testing
---------------
The desk uses continuous integration testing through Github actions. This
automatically runs the package tests for several commonly used operating systems
and python versions, before every change that is made to the code.
The current status of the `tests`_ and `coverage`_.
are available online. To run the tests locally, download/clone the package and
use the command 'pytest' within the pacakge directory.

.. _github: https://github.com/s-goldman/Dusty-Evolved-Star-Kit/
.. _issues: https://github.com/s-goldman/Dusty-Evolved-Star-Kit/issues
.. _tests: https://github.com/s-goldman/Dusty-Evolved-Star-Kit/actions?query=workflow%3A%22Python+package%22
.. _coverage: https://codecov.io/gh/s-goldman/Dusty-Evolved-Star-Kit
