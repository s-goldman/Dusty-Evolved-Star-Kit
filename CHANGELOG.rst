=========
Changelog
=========

1.9.1 (unreleased)

 - Deprecated the 'distance' argument in favor of 'distance_in_kpc' to improve 
   clarity.
 - Bug fixes for int(distance_in_kpc) when source is within 1 kpc, and grid 
   trimming when none is needed. [#246, #247]

1.9.0 (2025-01-28)

 - Changes to ensure compatibility with Numpy 2.0 and Python 3.12.
 - Changes to conform to PEP 8 style guide, and best practices for versioning. 
 - Updated testing with github actions. 
 - Warning that GRAMS mass loss rates are dust production rates. 
 - Added model grids from Goldman et al. 2025



1.7.2 (2020-08-05)

 - Updates plots with now 17 source maximum for single SED figure. The sed and
   sed_indiv scripts now use a common set of functions to minimize duplicated code,
   and ensure consistency. 


1.7.1 (2020-08-05)

 - Minor bug fixes to the data retrieval script.


1.7.0 (2020-07-24)

 - First major release of least-squares fitting DESK. The package is stable with
   pytest testing through Github-actions (Ubuntu and OSX: Python 3.6, 3.7, 3.8),
   documentation with Sphinx on readthedocs, coverage with codecov,
   code quality checks with codacy, installation with pip, and hosted on Github.
   Model grids are downloaded using direct-download links on Box.

1.3.1 (2019-04-29)
------------------

 - First release on PyPI.
