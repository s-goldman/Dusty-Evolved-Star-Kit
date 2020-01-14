---
title: 'The Dusty Evolved Star Kit (DESK): A Python package for fitting the Spectral Energy Distribution of Evolved Stars'
tags:
  - Python
  - astronomy
  - evolved stars
  - radiative transfer
  - stellar mass loss
authors:
  - name: Steven R. Goldman
    orcid: 0000-0002-8937-3844
    affiliation: 1 # (Multiple affiliations must be quoted)
affiliations:
 - name: Space Telescope Science Institute, 3700 San Martin Drive, Baltimore, MD 21218, USA
   index: 1
date: 10 January 2020
bibliography: paper.bib
---

# Summary

One of the few ways that we can understand the environment around evolved stars and how much material they contribute back to the interstellar medium, is by fitting the available data with models that account for the radiative transfer. Codes for calculating and creating models have been developed and refined `[@Elitzur:2001; @Ueta:2003]`, but a code for easily fitting data to grids of realistic models has been up-to-this-point unavailable.

The ``DESK`` is a python package that fits the available photometry or spectra of evolved stars, or the Spectral Energy Distribution (SED), to grids of 1- and 2-dimensional radiative transfer models using a least squares method. Grids include newly created grids using a variety of different dust species, the 2D GRAMS model grids `[@Sargent:2010; @Srinivasan:2011]`, and state-of-the-art dust growth grids by `@Nanni:2019`.

Results from these grids can vary dramatically as a result of unknown properties of evolved stars, especially the oxygen-rich Asymptotic Giant Branch (AGB) stars. It is also a challenge to compare results as they are calculated based on measured values (optical constants) which can not be interpolated over. To understand the ranges and estimated errors of fitted results, they must be compared to results from different model grids.

This package is designed for beginners to easily compare stellar samples and model grids for a better understanding of the uncertainties. The package can be installed using `pip` and, using "entrypoints", can be accessed from any terminal prompt once installed. The fitting method uses a brute-force technique to ensure a true best fit, and python multiprocessing for increased speed.

# Figures

An example of sources fit with an oxygen-rich grid  ![Example figure.](docs/example.png)

# References
