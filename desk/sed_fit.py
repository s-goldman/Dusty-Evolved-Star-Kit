from __future__ import absolute_import
import os
import pdb
import csv
import time
import math
import importlib
import numpy as np
import astropy.units as u
import matplotlib.pyplot as plt
from matplotlib import rc
from fnmatch import fnmatch
from astropy.io import ascii
from scipy import interpolate
from multiprocessing import Process, Value, cpu_count
from desk import config, remove_old_files, plotting_seds, get_remote_models, parameter_ranges
from desk.parameter_ranges import create_par
from desk.plotting_seds import create_fig
from multiprocessing import Pool, cpu_count
from astropy.table import Table, Column

importlib.reload(config)

'''
Steve Goldman
Space Telescope Science Institute
Nov 16, 2018
sgoldman@stsci.edu

This package takes a photometry or a spectrum (or spectra) in csv format and fits it/them with a grid of models. 
The grids used here are converted from output from the DUSTY code (Elitzur & Ivezic 2001, MNRAS, 327, 403) using
the other script dusty_to_grid.py. The code interpolates and trims a version of the data and calculates the least
squares value for each grid in the model and the data. The DUSTY outputs are then scaled and returned in files:
fitting_results.csv and fitting_plotting_output.csv (for plotting the results). An example plotting script has also
been provided.
'''


def get_targets():
    global targets
    targets = []
    path = str(__file__.replace('sed_fit.py', ''))
    # for multiple sources
    for item in os.listdir(path + 'put_target_data_here/'):
        if fnmatch(item, "*csv"):
            targets.append(path + 'put_target_data_here/' + item)
    return targets


def get_data(filename):
    """
    :param filename: filename of input data. Should be csv with Column 0: wavelength in um and Col 1: flux in Jy
    :return: two arrays of wavelength (x) and flux (y) in unit specified in config.py
    """
    global log_average_flux_wm2
    table = ascii.read(filename, delimiter=',')
    table.sort(table.colnames[0])
    x = np.array(table.columns[0])
    y = np.array(table.columns[1])
    index = np.where((x > config.fitting['wavelength_min']) & (x < config.fitting['wavelength_max']))
    x = x[index]
    y = y[index]
    y = y * u.Jy
    y = y.to(u.W / (u.m * u.m), equivalencies=u.spectral_density(x * u.um))
    log_average_flux_wm2 = np.log10(np.median(y).value)
    return x, np.array(y)


def find_closest(target_wave, model_wave):
    """
    :param target_wave: Target wavelength in um
    :param model_wave: model wavelength in um
    :return: a 1-D array of the closest data wavelength values, to the model wavelength values
    """
    idx = np.searchsorted(model_wave[0], target_wave[0])
    idx = np.clip(idx, 1, len(model_wave[0]) - 1)
    left = model_wave[0][idx - 1]
    right = model_wave[0][idx]
    idx -= target_wave[0] - left < right - target_wave[0]
    closest_data_flux = model_wave[1][idx]
    return closest_data_flux


def least2(data, model_l2):
    return np.nansum(np.square(model_l2 - data))


def trim(data, model_trim):
    """
    :param data: input data in tuple of x and y arrays
    :param model_trim: input model
    :return: trims motimedel to wavelength range of data
    """
    indexes = np.where(np.logical_and(model_trim[0] >= np.min(data[0]), model_trim[0] <= np.max(data[0])))
    return np.vstack([model_trim[0][indexes], model_trim[1][indexes]])


def fit_norm(data, norm_model):
    """
    :param data: input data in tuple of x and y arrays
    :param norm_model: closest wavelength values to data in 1-D array (from trim)
    :return: trimmed model in 2 column np.array
    """
    global trials
    stats = []
    # normalization range
    # trials = np.linspace(config.fitting['min_norm'], config.fitting['max_norm'], config.fitting['ntrials'])
    trials = np.logspace(log_average_flux_wm2 - 2, log_average_flux_wm2 + 2, 1000)
    for t in trials:
        stat = least2(data[1], norm_model * t)
        stats.append(stat)
    return stats


# for each target, fit spectra with given models (.fits file)
def sed_fitting(target):
    stat_values = []
    raw_data = get_data(target)  # gets target data
    # model_x = grid_dusty[0][0][:]  # gets model wavelengths
    for model in np.array(grid_dusty):
        trimmed_model = trim(raw_data, model)  # gets fluxes for corresponding wavelengths of data and models
        matched_model = find_closest(raw_data, trimmed_model)
        stat_values.append(fit_norm(raw_data, matched_model))
    stat_array = np.vstack(stat_values)
    argmin = np.argmin(stat_array)
    model_index = argmin // stat_array.shape[1]
    trial_index = argmin % stat_array.shape[1]
    target_name = (target.split('/')[-1][:15]).replace('IRAS-', 'IRAS ')

    if fnmatch(config.fitting['model_grid'], 'grams*'):
        print(Table(grid_outputs[model_index]))

    else:
        # calculates luminosity and scales outputs
        luminosity = int(np.power(10.0, distance_norm - math.log10(trials[trial_index]) * -1))
        scaled_vexp = float(grid_outputs[model_index]['vexp']) * (luminosity / 10000) ** 0.25
        scaled_mdot = grid_outputs[model_index]['mdot'] * ((luminosity / 10000) ** 0.75) * (
                config.target['assumed_gas_to_dust_ratio'] / 200) ** 0.5

        teff = int(grid_outputs[model_index]['teff'])
        tinner = int(grid_outputs[model_index]['tinner'])
        odep = grid_outputs[model_index]['odep']

        # creates output file
        latex_array = [target_name, luminosity, np.round(scaled_vexp, 1),
                       teff, tinner, odep, "%.3E" % float(scaled_mdot)]

        plotting_array = [target_name, target, trials[trial_index], model_index, model_grid, teff, tinner,
                          grid_outputs[model_index]['number'], odep]

        # printed output
        if config.output['printed_output'] == 'True':
            print()
            print()
            print(('             Target: ' + target_name + '        ' + str(counter.value + 1) + '/' + str(len(targets))))
            print('-------------------------------------------------')
            print(("Luminosity\t\t\t|\t" + str(round(luminosity))))
            print(("Optical depth\t\t\t|\t" + str(grid_outputs[model_index]['odep'])))
            print(("Expansion velocity (scaled)\t|\t" + str(round(scaled_vexp, 2))))
            print(("Mass loss (scaled)\t\t|\t" + str("%.2E" % float(scaled_mdot))))
            print('-------------------------------------------------')
            with open('fitting_results.csv', 'a') as f:
                writer = csv.writer(f, delimiter=',', lineterminator='\n')
                writer.writerow(np.array(latex_array))
                f.close()

            with open('fitting_plotting_outputs.csv', 'a') as f:
                writer = csv.writer(f, delimiter=',', lineterminator='\n')
                writer.writerow(np.array(plotting_array))
                f.close()
    counter.value += 1


def main(arg_input=get_targets(), dist=config.target['distance_in_kpc'], grid=config.fitting['model_grid']):
    """
    :param arg_input: Name of target in array of strings (or one string)
    :param dist: distance to source(s) in kiloparsecs
    :param grid: Name of model grid
    :return:
    """
    # set variables
    global model_grid
    global counter
    global grid_dusty
    global grid_outputs
    global distance_norm
    global full_path
    start = time.time()
    counter = Value('i', 0)
    # normalization calculation
    # solar constant = 1379 W
    # distance to sun in kpc 4.8483E-9
    distance_norm = math.log10(((int(dist) / 4.8482E-9) ** 2) / 1379)
    full_path = str(__file__.replace('sed_fit.py', ''))

    # User input for models
    if grid == 'carbon':
        model_grid = 'Zubko-Crich-bb'
    elif grid == 'oxygen':
        model_grid = 'Oss-Orich-bb'
    else:
        model_grid = grid

    # file names to look for
    csv_file = full_path + 'models/' + model_grid + '_outputs.csv'
    fits_file = full_path + 'models/' + model_grid + '_models.fits'

    # check file path, if missing checks remote directory
    if os.path.isfile(csv_file) and os.path.isfile(fits_file):
        print('You already have the models!')
        print('Great job')

    else:
        # raise ValueError('Model grid does not exist. Please try another')
        user_proceed = input('Models not found locally, download the models [y]/n?: ')
        if user_proceed == 'y' or user_proceed == '':
            get_remote_models.get_models(grid)
        elif user_proceed == 'n':
            raise ValueError('Please make another model selection')
        elif user_proceed != 'y' and user_proceed != 'n':
            raise ValueError('Invalid selection')

    # gets models
    grid_dusty = Table.read(fits_file)
    grid_outputs = Table.read(csv_file)

    # Model grid equal lengths check
    if len(grid_dusty) == len(grid_outputs):
        pass
    else:
        raise ValueError("Model grid input error: mismatch in model spectra and model output")

    # Creates results files
    with open('fitting_results.csv', 'w') as f:
        f.write('source,L,vexp_predicted,teff,tinner,odep,mdot\n')
        f.close()
    with open('fitting_plotting_outputs.csv', 'w') as f:
        f.write('target_name,data_file,norm,index,grid_name,teff,tinner,number,odep\n')
        f.close()

    # SED FITTING ###############################
    with Pool(processes=cpu_count() - 1) as pool:
        pool.map(sed_fitting, [target_string for target_string in arg_input])

    # Saves results csv file
    if fnmatch(config.fitting['model_grid'], 'grams*'):
        print(Table(grid_outputs[model_index]))

    # creating figures
    if config.output['create_figure'] == 'yes':
        print('\n. . . Creating SED figure . . .')
        create_fig()  # runs plotting script
    else:
        print('No figure created. To automatically generate a figure change the ' +
              '"create_figure" variable in the config.py script to "yes".')

    if not os.path.isfile("parameter_ranges_" + config.fitting['model_grid'] + ".png"):
        print('. . . Creating parameter range figure . . .')
        create_par()

    end = time.time()
    print()
    print('Time: ' + str("%.2f" % float((end - start) / 60)) + ' minutes')


if __name__ == '__main__':
    main()
