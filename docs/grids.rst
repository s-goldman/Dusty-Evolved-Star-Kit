===== 
Grids
=====

Oxygen-Rich Model Grids
-----------------------

Oss-Orich-aringer (*N*\ =2,000): Uses warm silicates from `Ossenkopf et
al. 1992`_ and photospheric models from `Aringer et al. 2016`_. Provides
ranges in effective temperature (2600-3400 K: 200 K interval) inner dust
temperature (600-1200K: 200 K interval) and optical depth (0.1 - 50: 100
spaced logarithmicly). Standard `MRN`_ grain size distribution from
0.005 - 0.25 microns.

Oss-Orich-bb (*N*\ =2,000): Same as Oss-Orich-aringer but using black
bodies instead of the photospheric models.

Crystalline-20-bb (*N*\ =2,000): Same as Oss-Orich-bb but using 20%
crystalline silicate grains from `Jaeger et al. 1994`_.

corundum-20-bb (*N*\ =2,000): Same as Oss-Orich-bb but using 20%
corundum grains from `Begemann et al. 1997`_.

big-grain (*N*\ =2,000): Same as Oss-Orich-aringer but using a higher
maximum dust grain size of 0.35.

fifth-iron (*N*\ =500): Same as Oss-Orich-aringer but with 20% iron
grains from `Henning et al. 1995`_, and an effective temperature of 3400
K.

half-iron (*N*\ =500): Same as Oss-Orich-aringer but with 50% iron
grains from `Henning et al. 1995`_, and an effective temperature of 3400
K.

one-fifth-carbon (*N*\ =500): Same as Oss-Orich-aringer but with 20%
amorphous carbon grains from `Zubko et al. 1996`_, and an effective
temperature of 3400 K.

arnold-palmer (*N*\ =2,000): Same as Oss-Orich-aringer but with 50%
amorphous carbon grains from `Zubko et al. 1996`_.

Carbon-Rich Model Grids
-----------------------

Zubko-Crich-aringer (*N*\ =2,000): Same as Oss-Orich-aringer but with
amorphous carbon grains from `Zubko et al. 1996`_.

Zubko-Crich-bb (*N*\ =2,000): Same as Zubko-Crich-aringer but using
black bodies instead of the photospheric models.

.. _the-dust-growth-model-grids-from-nanni-et-al-2019:

Dust growth grids
-----------------

The dust growth model grids from `Nanni et al. (2019)`_

H11-LMC (*N*\ =90,899): A carbon-rich grid for the LMC metallicity (1/2
solar) using optical constants from `Hanner et al. (1988)`_.

H11-SMC (*N*\ =91,058): A carbon-rich grid for the SMC metallicity (1/5
solar) using optical constants from `Hanner et al. (1988)`_.

J1000-LMC (*N*\ =85,392): A carbon-rich grid for the LMC metallicity
(1/2 solar) using optical constants from `Jager et al. (1998)`_

J1000-SMC (*N*\ =85,546): A carbon-rich grid for the SMC metallicity
(1/5 solar) using optical constants from `Jager et al. (1998)`_


The GRAMS model grids 
----------------------

The GRAMS model grids from `Sargent et al. 2011`_ and `Srinivasan et al. 2011`_.

grams-carbon (*N*\ =12,244): A 2D carbon-rich grid using the `2DUST`_
code for the LMC metallicity (1/2 solar) using optical constants from
`Zubko et al. 1996`_.

grams-oxygen (*N*\ =68,601): A 2D oxygen-rich grid using the `2DUST`_
code for the LMC metallicity (1/2 solar) using optical constants from
`Ossenkopf et al. 1992`_.

.. code:: diff

   - Warning: results uncertain outside of 20-150 kpc

.. _Sargent et al. 2011: https://ui.adsabs.harvard.edu/abs/2011ApJ...728...93S/abstract
.. _Srinivasan et al. 2011: https://ui.adsabs.harvard.edu/abs/2011A%26A...532A..54S/abstract
.. _2DUST: https://2dust.stsci.edu/index.cgi
.. _Zubko et al. 1996: https://ui.adsabs.harvard.edu/abs/1996MNRAS.282.1321Z/abstract
.. _Ossenkopf et al. 1992: https://ui.adsabs.harvard.edu/abs/1992A%26A...261..567O/abstract
.. _Aringer et al. 2016: https://ui.adsabs.harvard.edu/abs/2016MNRAS.457.3611A/abstract
.. _MRN: https://ui.adsabs.harvard.edu/abs/1977ApJ...217..425M/abstract
.. _Jaeger et al. 1994: https://ui.adsabs.harvard.edu/abs/1994A%26A...292..641J/abstract
.. _Begemann et al. 1997: https://ui.adsabs.harvard.edu/abs/1997ApJ...476..199B/abstract
.. _Henning et al. 1995: https://ui.adsabs.harvard.edu/abs/1995A%26AS..112..143H/abstract
.. _Zubko et al. 1996: https://ui.adsabs.harvard.edu/abs/1996MNRAS.282.1321Z/abstract
.. _Nanni et al. (2019): https://ui.adsabs.harvard.edu/abs/2019MNRAS.487..502N/abstract
.. _Hanner et al. (1988): https://ui.adsabs.harvard.edu/abs/1988ioch.rept.....H/abstract
.. _the-grams-model-grids-sargent-et-al-2011-srinivasan-et-al-2011:
