=====
Usage
=====

SED-Fitting
-----------

The Dusty-Evolved-Star-Kit can fit the spectra and photometry of evolved stars with both carbon- and oxygen-rich grids of radiative transfer models. This enables easy comparison of grids of models and different samples.

The input for this package is a csv file with wavelength in microns in the first column, and flux in Jy in the second column.

After installation with pip, in any command line prompt, use the command:

.. code-block:: console

	> desk grids

This will display the available grids for fitting. Next you need to point the package to your csv file, and specify the distance and grid of choice:

.. code-block:: console

	> desk fit --source='target_name.csv' --distance=50 --grid='H11-LMC'

or specify a directory with multiple csv files:

.. code-block:: console

	> desk fit --source='folder_of_csvs' --distance=30 --grid='Oss-Orich-bb'
	
Additional options include the density of the model grid (n). The strength of the 1D DUSTY models is that they can be scaled to create more luminous models. The DESK takes the initial grid and scales it n times (default: 50) to create a larger denser grid of sources within the luinosity limits (default: 1,000 - 150,000 Msun). The user may also specify a wavelength minimum and maximum. This will still show the full photometry in the final SED figure, but fit only the wavelength region specified. Lastly, the user can specify whether to fit using multiprocessing (using all but 1 computer cores) or single core fitting (multiprocessing=False):

.. code-block:: console

	> desk fit --source='target_name.csv' --distance=50 --grid='oxygen' --n=20 --min_wavelength=3.5 --max_wavelength=23 --multiprocessing=False

Outputs
-------
.. image:: ./example.png
	:width: 400
	:alt: SED example

This is an example of the output_sed.png file fitting three massive oxygen-rich AGB stars from the LMC. To produce individual figures subsequently run the command:

.. code-block:: console

	> desk single_fig
