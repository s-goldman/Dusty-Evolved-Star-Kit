=====
Grids
=====

The DESK_ downloads and fits both new and commonly-used model grids, automatically.
The grids are also available for download on Zenodo_. Columns are in wavelength (um) and flux density (W*m-2).

DUSTY model grids
-----------------

The DUSTY_ models are 1-D radiative transfer models that exploit
scaling relations to generate models. The model shape can be scaled
to any luminosity, expansion velocity, or mass-loss rate so long as the
combination of these three parameters remains the same. The DESK model grids
contain 500--2000 unique model shapes. Theses grids are scaled
to the desired number of luminosities between 1,000 and 150,000 using the
command option `--n`.

.. code-block:: console

	> desk fit --source='example.csv' --grid='Oss-Orich-aringer' --n=10

This command will scale the 'Oss-Orich-aringer' model grid of 2,000 unique model
shapes to luminosities at 1000, 17555, 34111, 50666, 67222, 83777, 100333, 116888,
133444, and 150000 solar luminosities (20,000 models).

The output model parameters of expansion velocity and gas mass-loss rate are
scaled using the relations from `Elitzur & Ivezić 2001`_. The model flux is scaled
using the brightness and distance to the sun, and scaling for the luminositiy
which is already in solar luminosities.

Only the default carbon (Zubko-Crich-bb) and oxygen-rich (Oss-Orich-bb) model grids
are downloaded during installation. Additional grids are downloaded when selected.
The number of unique models and the filesize of each grid are specified next to
the grid names below.

The models assume a standard `MRN`_ grain size distribution from
0.005 - 0.25 microns. The DUSTY code uses an exact calculation of the wind density
distribution by solving the hydrodynamics equations as a set coupled to radiative
transfer. This calculation extends to a distance of 10,000 times the inner radius (density type = 3,
within the DUSTY code).


Oxygen-rich DUSTY model grids
=============================

desk-mix (*N*\ = 19,200; 177 MB): Uses a grain mixture inspired by the More Of Dusty (MOD)
code (`Groenewegen 2012`_) based on the DUSTY code (`Elitzur & Ivezić 2001`_).
The dust grains assume a mixture of olivine grains
(MgFeSiO4) from `Dorschner et al. (1995)`_, corundum grains
(AlOx; amorphous porous Al2O3) from `Begemann et al. (1997)`_, and
iron grains (FeO) from `Henning et al. (1995)`_. The relative percentages of
olivine and corundum range from 48-98\% olivine in increments of 10\% and include either
2\% or 4\% iron grains. The grid uses oxygen-rich atmospheric MARCS models from
`Gustafsson et al. (2008)`_.

Oss-Orich-aringer (*N*\ =2,000; 14 MB): Uses warm silicates from
`Ossenkopf et al. (1992)`_ and photospheric models from
`Aringer et al. (2016)`_. Provides ranges in effective temperature
(2600-3400 K: 200 K interval) inner dust
temperature (600-1200K: 200 K interval) and optical depth (0.1 - 50: 100
spaced logarithmicly).

Oss-Orich-bb (*N*\ =2,000; 14 MB): Same as Oss-Orich-aringer but using black
bodies instead of the photospheric models.

Crystalline-20-bb (*N*\ =2,000; 14 MB): Same as Oss-Orich-bb but using 20%
crystalline silicate grains from `Jaeger et al. (1994)`_.

corundum-20-bb (*N*\ =2,000; 14 MB): Same as Oss-Orich-bb but using 20%
corundum grains from `Begemann et al. (1997)`_.

big-grain (*N*\ =2,000; 14 MB): Same as Oss-Orich-aringer but using a higher
maximum dust grain size of 0.35.

fifth-iron (*N*\ =500; 3 MB): Same as Oss-Orich-aringer but with 20% iron
grains from `Henning et al. (1995)`_, and an effective temperature of 3400
K.

half-iron (*N*\ =500; 3 MB): Same as Oss-Orich-aringer but with 50% iron
grains from `Henning et al. (1995)`_, and an effective temperature of 3400
K.

one-fifth-carbon (*N*\ =500; 3 MB): Same as Oss-Orich-aringer but with 20%
amorphous carbon grains from `Zubko et al. (1996)`_, and an effective
temperature of 3400 K.

arnold-palmer (*N*\ =2,000; 137 MB): Same as Oss-Orich-aringer but with 50%
amorphous carbon grains from `Zubko et al. (1996)`_.

Carbon-rich DUSTY model grids
=============================

Zubko-Crich-aringer (*N*\ =2,000; 145 MB): Same as Oss-Orich-aringer but with
amorphous carbon grains from `Zubko et al. (1996)`_.

Zubko-Crich-bb (*N*\ =2,000; 123 MB): Same as Zubko-Crich-aringer but using
black bodies instead of the photospheric models.

.. _the-dust-growth-model-grids-from-nanni-et-al-2019:

Dust growth grids
=================

The dust growth model grids from `Nanni et al. (2019)`_

H11-LMC (*N*\ =90,899; 770 MB): A carbon-rich grid for the LMC metallicity (1/2
solar) using optical constants from `Hanner et al. (1988)`_.

H11-SMC (*N*\ =91,058; 772 MB): A carbon-rich grid for the SMC metallicity (1/5
solar) using optical constants from `Hanner et al. (1988)`_.

J1000-LMC (*N*\ =85,392; 723 MB): A carbon-rich grid for the LMC metallicity
(1/2 solar) using optical constants from `Jaeger et al. (1998)`_

J1000-SMC (*N*\ =85,546; 724 MB): A carbon-rich grid for the SMC metallicity
(1/5 solar) using optical constants from `Jaeger et al. (1998)`_


2-D model grids
-------------------------


The GRAMS model grids
=====================

The GRAMS model grids from `Sargent et al. (2011)`_ and `Srinivasan et al. (2011)`_.
These models assume a density distribution of 1/r\ :sup:`2`, a modified KMH dust grain
distribution, and an assumed expansion velocity of 10 km/s.


grams-carbon (*N*\ =12,244; 41.3 MB): A 2D carbon-rich grid using the `2DUST`_
code for the LMC metallicity (1/2 solar) using optical constants from
`Zubko et al. (1996)`_.

grams-oxygen (*N*\ =68,601; 200 MB): A 2D oxygen-rich grid using the `2DUST`_
code for the LMC metallicity (1/2 solar) using optical constants from
`Ossenkopf et al. (1992)`_.

grams: Both Grams datasets combined

.. code:: diff

   - Warning: results uncertain outside of a distance 20-150 kpc.

.. _DESK: https://github.com/s-goldman/Dusty-Evolved-Star-Kit
.. _Zenodo: https://zenodo.org/record/4776833
.. _DUSTY: https://github.com/ivezic/dusty
.. _Elitzur & Ivezić 2001: https://ui.adsabs.harvard.edu/abs/2001MNRAS.327..403E/abstract
.. _Sargent et al. (2011): https://ui.adsabs.harvard.edu/abs/2011ApJ...728...93S/abstract
.. _Srinivasan et al. (2011): https://ui.adsabs.harvard.edu/abs/2011A%26A...532A..54S/abstract
.. _2DUST: https://ui.adsabs.harvard.edu/abs/2003ApJ...586.1338U/abstract
.. _Zubko et al. (1996): https://ui.adsabs.harvard.edu/abs/1996MNRAS.282.1321Z/abstract
.. _Ossenkopf et al. (1992): https://ui.adsabs.harvard.edu/abs/1992A%26A...261..567O/abstract
.. _Aringer et al. (2016): https://ui.adsabs.harvard.edu/abs/2016MNRAS.457.3611A/abstract
.. _MRN: https://ui.adsabs.harvard.edu/abs/1977ApJ...217..425M/abstract
.. _Jaeger et al. (1994): https://ui.adsabs.harvard.edu/abs/1994A%26A...292..641J/abstract
.. _Jaeger et al. (1998): https://ui.adsabs.harvard.edu/abs/1998A%26A...339..904J/abstract
.. _Begemann et al. (1997): https://ui.adsabs.harvard.edu/abs/1997ApJ...476..199B/abstract
.. _Henning et al. (1995): https://ui.adsabs.harvard.edu/abs/1995A%26AS..112..143H/abstract
.. _Zubko et al. (1996): https://ui.adsabs.harvard.edu/abs/1996MNRAS.282.1321Z/abstract
.. _Nanni et al. (2019): https://ui.adsabs.harvard.edu/abs/2019MNRAS.487..502N/abstract
.. _Hanner et al. (1988): https://ui.adsabs.harvard.edu/abs/1988ioch.rept.....H/abstract
.. _Groenewegen 2012: https://ui.adsabs.harvard.edu/abs/2012A&A...543A..36G/abstract
.. _Dorschner et al. (1995): https://ui.adsabs.harvard.edu/abs/1995A&A...300..503D/abstract
.. _Gustafsson et al. (2008): https://ui.adsabs.harvard.edu/abs/2008A%26A...486..951G/abstract
