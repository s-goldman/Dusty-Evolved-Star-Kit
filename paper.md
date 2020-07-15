---
title: 'The Dusty Evolved Star Kit (DESK): A Python package for fitting the Spectral Energy Distribution of Evolved Stars'
tags:
  - Python
  - astronomy
  - asymptotic giant branch stars
  - radiative Transfer
  - stellar Mass Loss
  - spectral energy distribution fitting
authors:
  - name: Steven R. Goldman
    orcid: 0000-0002-8937-3844
    affiliation: 1 # (Multiple affiliations must be quoted)
affiliations:
 - name: Space Telescope Science Institute, 3700 San Martin Drive, Baltimore, MD 21218, USA
   index: 1
date: 15 July 2020
bibliography: paper.bib
---

# Summary

One of the few ways that we can understand the environment around dusty stars and how much material they contribute back to the Universe, is by fitting their brightness at different wavelenghts with models that account for how the energy trasfers through the dust. Codes for creating models have been developed and refined `[@Elitzur:2001; @Ueta:2003]`, but a code for easily fitting data to grids of realistic models has been up-to-this-point unavailable.

The ``DESK`` is a python package that fits photometry or spectra of evolved stars, or the Spectral Energy Distribution (SED), to grids of radiative transfer models using a least-squares method. The The package includes newly created grids using a variety of different dust species and state-of-the-art dust growth grids [`@Nanni:2019`].

Results from these grids (e.g. luminosity, mass-loss rate) can vary dramatically as a result of unknown properties of evolved stars, especially the oxygen-rich Asymptotic Giant Branch (AGB) stars. It is also a challenge to compare results as they are calculated based on measured values (optical constants) which can not be interpolated over. To understand the ranges and estimated errors of fitted results, they must be compared to results from different model grids.

This package is designed to easily compare stellar samples and model grids for a better understanding of results and their uncertainties. The package can be installed using `pip` and, using "entrypoints", can be accessed from any terminal prompt once installed. The fitting method uses a brute-force technique to ensure a true best fit. Grids of radiative trasfer models can easily be created and added to the downloadable library of model grids.

# Figures

An example of sources fit with an oxygen-rich grid  ![Example figure.](docs/example.png)

# References
