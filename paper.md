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
    affiliation: 1
affiliations:
 - name: Space Telescope Science Institute, 3700 San Martin Drive, Baltimore, MD 21218, USA
   index: 1
date: 15 July 2020
bibliography: paper.bib
---

# Summary

One of the few ways that we can understand the environment around dusty stars and how much material they contribute back to the Universe, is by fitting their brightness at different wavelengths with models that account for how the energy transfers through the dust. Codes for creating models have been developed and refined [@Elitzur:2001; @Ueta:2003], but a code for easily fitting data to grids of realistic models has been up-to-this-point unavailable.

The ``DESK`` is a python package that fits photometry or spectra of evolved stars, or the Spectral Energy Distribution (SED), to grids of radiative transfer models using a least-squares method. The package includes newly created grids using a variety of different dust species, and state-of-the-art dust growth grids [@Nanni:2019].

Results from these grids (e.g. luminosity, mass-loss rate) can vary dramatically as a result of the unknown properties of evolved stars, especially the oxygen-rich Asymptotic Giant Branch (AGB) stars [@Srinivasan:2011; @Goldman:2017]. It is also a challenge to compare results as they are calculated based on measured values of the dust (optical constants) which can not be interpolated over. To understand the ranges and estimated errors of fitted results, they must be compared to results from different model grids.

This package is designed to easily compare stellar samples and model grids for a better understanding of the results and their uncertainties. The package can be installed using `pip` and, using "entrypoints", can be accessed from any terminal prompt once installed. The fitting method uses a brute-force technique to ensure a true best fit. Grids of radiative transfer models can easily be created and added to the model grid library. The available model grids for this version are listed in
Table 1.

Table 1

| Grid name           | Size   | Type | Atmospheric model | Optical constants                                          | References                     |
|---------------------|--------|------|-------------------|------------------------------------------------------------|--------------------------------|
| Oss-Orich-aringer   | 2,000  | O    | COMARCS           | Warm silicates                                             | @Ossenkopf:1992; @Aringer:2016 |
| Oss-Orich-bb        | 2,000  | O    | Black body (BB)   | Warm silicates                                             | @Ossenkopf:1992; @Aringer:2016 |
| Crystalline-20-bb   | 2,000  | O    | BB                | 80% warm silicates 20% crystalline silicates               | @Ossenkopf:1992; @Aringer:2016 |
| corundum-20-bb      | 2,000  | O    | BB                | 80% warm silicates 20% corundum silicates                  | @Ossenkopf:1992; @Aringer:2016 |
| big-grain           | 2,000  | O    | BB                | Warm silicates with higher maximum dust grain size of 0.35 | @Ossenkopf:1992; @Aringer:2016 |
| fifth-iron          | 500    | O    | BB                | 80% warm silicates 20% iron grains                         | @Ossenkopf:1992; @Aringer:2016 |
| half-iron           | 500    | O    | BB                | 50% warm silicates 50% iron grains                         | @Ossenkopf:1992; @Aringer:2016 |
| one-fifth-carbon    | 500    | O    | BB                | 80% warm silicates 20% carbonaceous grains                 | @Ossenkopf:1992; @Aringer:2016 |
| arnold-palmer       | 500    | O    | BB                | 50% warm silicates 50% carbonaceous grains                 | @Ossenkopf:1992; @Aringer:2016 |
| desk-mix            | xx,xxx | O    | MARCS             | Mixture of olivine(48-88%), corundum(8-48%), and iron (4%) | @Ossenkopf:1992; @Aringer:2016 |
| Zubko-Crich-aringer | 2,000  | C    | COMARCS           | amorphous carbon grains                                    |                                |
| Zubko-Crich-bb      | 2,000  | C    | BB                | amorphous carbon grains                                    |                                |
| H11-LMC             | 90,899 | C    | COMARCS           | Dust-growth grid with 1/2 solar metallicity                |                                |
| H11-SMC             | 91,058 | C    | COMARCS           | Dust-growth grid with 1/5 solar metallicity                |                                |
| J1000-LMC           | 85,392 | C    | COMARCS           | Dust-growth grid with 1/2 solar metallicity                |                                |
| J1000-SMC           | 85,546 | C    | COMARCS           | Dust-growth grid with 1/5 solar metallicity                |                                |

# Figures

![An example of three massive oxygen-rich AGB stars in the Large Magellanic Cloud (LMC) galaxy fit with the default oxygen-rich model grid (Oss-Orich-bb). These three example sources can be fit, and this figure can be created, using the command `desk fit` and then the command `desk sed`.  ](docs/example.png)

# References
