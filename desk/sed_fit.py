from __future__ import absolute_import
import os
import pdb
import time
import math
import importlib
import subprocess
import numpy as np
import astropy.units as u
import matplotlib.pyplot as plt
from tqdm import tqdm
from matplotlib import rc
from fnmatch import fnmatch
from astropy.io import ascii
from functools import partial
from scipy import interpolate
from multiprocessing import Process
from desk import config, remove_old_files, plotting_seds, get_padova, parameter_ranges
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
    full_path = str(__file__.replace('sed_fit.py', ''))
    # for multiple sources
    for item in os.listdir(full_path + 'put_target_data_here/'):
        if fnmatch(item, "*csv"):
            targets.append(full_path + 'put_target_data_here/' + item)
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
    # pdb.set_trace()
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

    # appends data for plotting later
    follow_up_array.append(np.array(grid_outputs[model_index]))
    target_name = (target.split('/')[-1][:15]).replace('IRAS-', 'IRAS ')
    follow_up_names.append(target_name)
    follow_up_index.append(model_index)
    follow_up_normilazation.append(trials[trial_index])

    if fnmatch(config.fitting['model_grid'], 'grams*'):
        print(Table(grid_outputs[model_index]))
        latex_array.append(grid_outputs[model_index])

    else:
        # calculates luminosity and scales outputs
        luminosity = int(np.power(10.0, distance_norm - math.log10(trials[trial_index]) * -1))
        scaled_vexp = float(grid_outputs[model_index]['vexp']) * (luminosity / 10000) ** 0.25
        scaled_mdot = grid_outputs[model_index]['mdot'] * ((luminosity / 10000) ** 0.75) * (
                config.target['assumed_gas_to_dust_ratio'] / 200) ** 0.5

        # creates output file
        latex_array.append((target_name, str(luminosity), str(np.round(scaled_vexp, 1)), str(
            int(grid_outputs[model_index]['teff'])), str(int(grid_outputs[model_index]['tinner'])), str(
            grid_outputs[model_index]['odep']), "%.3E" % float(scaled_mdot)))

        # printed output
        if config.output['printed_output'] == 'True':
            print()
            print()
            print(('             Target: ' + target_name + '        ' + str(counter + 1) + '/' + str(len(targets))))
            print('-------------------------------------------------')
            print(("Luminosity\t\t\t|\t" + str(round(luminosity))))
            print(("Optical depth\t\t\t|\t" + str(grid_outputs[model_index]['odep'])))
            print(("Expansion velocity (scaled)\t|\t" + str(round(scaled_vexp, 2))))
            print(("Mass loss (scaled)\t\t|\t" + str("%.2E" % float(scaled_mdot))))
            print('-------------------------------------------------')
        return latex_array, follow_up_normilazation, follow_up_names, follow_up_index, follow_up_array

    # with Pool(processes=number_of_cores_to_use) as pool:
    #         pool.map(sed_fitting, targets)


def main(arg_input=get_targets(), dist=config.target['distance_in_kpc']):
    # set variables
    global counter
    global grid_dusty
    global grid_outputs
    global distance_norm
    global latex_array
    global full_path
    global follow_up_array
    global follow_up_index
    global follow_up_names
    global follow_up_normilazation
    follow_up_array = []
    follow_up_names = []
    follow_up_index = []
    follow_up_normilazation = []
    latex_array = []
    start = time.time()
    # normalization calculation
    # solar constant = 1379 W
    # distance to sun in kpc 4.8483E-9
    distance_norm = math.log10(((int(dist) / 4.8482E-9) ** 2) / 1379)

    full_path = str(__file__.replace('sed_fit.py', ''))

    # remove old file
    remove_old_files.remove()

    # check if padova
    if not os.path.isfile(full_path + 'models/' + config.fitting['model_grid'] + '_models.fits'):
        print('Models not in directory')
        user_proceed = input('Download model [y]/n? (may take 30 minutes): ')
        if user_proceed == 'y' or user_proceed == '':
            get_model(config.fitting['model_grid'])
        else:
            raise ValueError('Choose another model (in config.py file)')
    else:
        print('You already have the models!')
        print('Great job')

    grid_dusty = Table.read(full_path + 'models/' + config.fitting['model_grid'] + '_models.fits')
    grid_outputs = Table.read(full_path + 'models/' + config.fitting['model_grid'] + '_outputs.csv')

    # Model grid check
    if len(grid_dusty) == len(grid_outputs):
        pass
    else:
        raise ValueError("Model grid input error: mismatch in model spectra and model output")

    # SED FITTING
    # pdb.set_trace()
    for counter, target_string in tqdm(enumerate(arg_input)):
        sed_fitting(target_string)

    # saves results csv file
    if fnmatch(config.fitting['model_grid'], 'grams*'):
        print(Table(grid_outputs[model_index]))

    else:
        file_a = Table(np.array(latex_array), names=(
            'source', 'L', 'vexp_predicted', 'teff', 'tinner', 'odep', 'mdot'), dtype=(
            'S16', 'int32', 'f8', 'int32', 'int32', 'f8', 'f8'))
        file_a.write('fitting_results.csv', format='csv', overwrite=True)

    # saves plotting file
    file_b = Table(np.array(follow_up_array))
    file_b.add_column(Column(follow_up_index, name='index'), index=0)
    file_b.add_column(Column(follow_up_normilazation, name='norm'), index=0)
    file_b.add_column(Column(arg_input, name='data_file'), index=0)
    file_b.add_column(Column(follow_up_names, name='target_name'), index=0)
    file_b.write('fitting_plotting_outputs.csv', format='csv', overwrite=True)

    # remove old file
    remove_old_files.remove()

    if config.output['figures_single_multiple_or_none'] == 'single':
        print('\nCreating figure')
        create_fig()  # runs plotting script
    else:
        print('No figure created. To automatically generate a figure or multiple figures change the ' +
              '"figures_single_multiple_or_none" variable in the config.py script to "single" or "multiple".')

    if not os.path.isfile("parameter_ranges_" + config.fitting['model_grid'] + ".png"):
        print('Creating parameter range figure')
        create_par()

    end = time.time()
    print()
    print('Time: ' + str("%.2f" % float((end - start) / 60)) + ' minutes')


if __name__ == '__main__':
    main()
