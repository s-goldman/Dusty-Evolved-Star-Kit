import os
import time
import math
import config
import subprocess
import pdb
import numpy as np
import astropy.units as u
import matplotlib.pyplot as plt
from fnmatch import fnmatch
from astropy.io import ascii
from functools import partial
from astropy.table import Table, Column
from matplotlib import rc
from scipy import interpolate
from plotting_seds import create_fig
from tqdm import tqdm
'''
Steve Goldman
Space Telescope Science Institute
May 17, 2018
sgoldman@stsci.edu

This package takes a spectrum (or spectra) in csv format and fits it/them with a grid of models. 
The grids used here are converted from output from the DUSTY code (Elitzur & Ivezic 2001, MNRAS, 327, 403) using
the other script dusty_to_grid.py. The code interpolates and trims a version of the data and calculates the least
squares value for each grid in the model and the data. The DUSTY outputs are then scaled and returned in files:
fitting_results.csv and fitting_plotting_output.csv (for plotting the results). 
'''

# set variables
targets = []
latex_array = []
target_names = []
follow_up_array = []
follow_up_names = []
follow_up_index = []
follow_up_normilazation = []
start = time.time()

# normalization calculation
# solar constant = 1379 W
# distance to sun in kpc 4.8483E-9
distance_norm = math.log10(((int(config.target['distance_in_kpc'])/4.8482E-9)**2)/1379)

# normalization range
trials = np.linspace(config.fitting['min_norm'], config.fitting['max_norm'], config.fitting['ntrials'])

# for multiple sources
for item in os.listdir('../put_target_data_here/'):
    if fnmatch(item, "*csv"):
        targets.append('../put_target_data_here/'+item)

# example source
# targets = ['../put_target_data_here/IRAS_04509-6922.csv']  # comment out for all sources

grid_dusty = Table.read('../models/'+config.fitting['model_grid']+'_models.fits')
grid_outputs = Table.read('../models/'+config.fitting['model_grid']+'_outputs.csv')


def get_data(filename):
    table = ascii.read(filename, delimiter=',')
    table.sort(table.colnames[0])
    x = np.array(table.columns[0])
    y = np.array(table.columns[1])
    index = np.where((x > config.fitting['wavelength_min']) & (x < config.fitting['wavelength_max']))
    x = x[index]
    y = y[index]
    y = y * u.Jy
    y = y.to(u.W/(u.m * u.m), equivalencies=u.spectral_density(x * u.um))
    return x, np.array(y)


def find_closest(target_wave, model_wave):
    idx = np.searchsorted(model_wave[0], target_wave[0])
    idx = np.clip(idx, 1, len(model_wave[0])-1)
    left = model_wave[0][idx-1]
    right = model_wave[0][idx]
    idx -= target_wave[0] - left < right - target_wave[0]
    closest_data_flux = model_wave[1][idx]
    return closest_data_flux


def least2(data, model_l2):
    return np.square(model_l2 - data).sum()


def trim(data, model_trim):
    # gets dusty model range that matches data
    indexes = np.where(np.logical_and(model_trim[0] >= np.min(data[0]), model_trim[0] <= np.max(data[0])))
    return np.vstack([model_trim[0][indexes], model_trim[1][indexes]])


def fit_norm(data, norm_model):
    stats = []
    for t in trials:
        stat = least2(data[1], norm_model*t)
        stats.append(stat)
    return stats


# for each target, fit spectra with given models (.fits file)
for counter, target in enumerate(targets):
    stat_values = []
    raw_data = get_data(target)  # gets target data
    model_x = grid_dusty[0][0][:]  # gets model wavelengths
    for model in np.array(grid_dusty):
        trimmed_model = trim(raw_data, model)  # gets fluxes for corresponding wavelengths of data and models
        matched_model = find_closest(raw_data, trimmed_model)
        stat_values.append(fit_norm(raw_data, matched_model))
    stat_array = np.vstack(stat_values)
    argmin = np.argmin(stat_array)
    model_index = argmin // stat_array.shape[1]
    trial_index = argmin % stat_array.shape[1]

    # calculates luminosity and scales outputs
    luminosity = int(np.power(10.0, distance_norm - math.log10(trials[trial_index]) * -1))
    scaled_vexp = float(grid_outputs[model_index]['vexp']) * (luminosity / 10000) ** 0.25
    scaled_mdot = grid_outputs[model_index]['mdot'] * ((luminosity / 10000) ** 0.75) * (
            config.target['assumed_gas_to_dust_ratio'] / 200) ** 0.5

    # creates output file
    target_name = (target.split('/')[-1][:15]).replace('IRAS-', 'IRAS ')
    latex_array.append((target_name, str(luminosity), str(np.round(scaled_vexp, 1)), str(
        int(grid_outputs[model_index]['teff'])), str(int(grid_outputs[model_index]['tinner'])), str(
        grid_outputs[model_index]['odep']), "%.3E" % float(scaled_mdot)))

    # appends data for plotting later
    follow_up_array.append(np.array(grid_outputs[model_index]))
    follow_up_names.append(target_name)
    follow_up_index.append(model_index)
    follow_up_normilazation.append(trials[trial_index])

    # printed output
    print()
    print()
    print(('             Target: '+target_name+'        '+str(counter+1)+'/'+str(len(targets))))
    print('-------------------------------------------------')
    print(("Luminosity\t\t\t|\t"+str(round(luminosity))))
    print(("Optical depth\t\t\t|\t"+str(grid_outputs[model_index]['odep'])))
    print(("Expansion velocity (scaled)\t|\t"+str(round(scaled_vexp, 2))))
    print(("Mass loss (scaled)\t\t|\t"+str("%.2E" % float(scaled_mdot))))
    print('-------------------------------------------------')

# saves results csv file
file_a = Table(np.array(latex_array), names=(
    'source', 'L', 'vexp_predicted', 'teff', 'tinner', 'odep', 'mdot'), dtype=(
    'S16', 'int32', 'f8', 'int32', 'int32', 'f8', 'f8'))
file_a.write('../fitting_results.csv', format='csv', overwrite=True)

# saves plotting file
file_b = Table(np.array(follow_up_array))
file_b.add_column(Column(follow_up_index, name='index'), index=0)
file_b.add_column(Column(follow_up_normilazation, name='norm'), index=0)
file_b.add_column(Column(targets, name='data_file'), index=0)
file_b.add_column(Column(follow_up_names, name='target_name'), index=0)
file_b.write('../fitting_plotting_outputs.csv', format='csv', overwrite=True)


print('\nCreating figure')
create_fig()  # runs plotting script

end = time.time()
print()
print('Time: '+str("%.2f" % float((end - start)/60))+' minutes')
