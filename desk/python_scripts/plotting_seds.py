import os
import math
import subprocess
import pdb
import shutil
import numpy as np
import astropy.units as u
import matplotlib.pyplot as plt
from glob import glob
from fnmatch import fnmatch
from multiprocessing import cpu_count, Pool
from functools import partial
from astropy.table import Table, Column
from matplotlib import rc
from scipy import interpolate
'''
Steve Goldman
Space Telescope Science Institute
May 17, 2018
sgoldman@stsci.edu

This script is for plotting the outputs of the sed_fitting script.
'''

rc('text', usetex=True)
plt.rcParams['font.family'] = 'serif'
plt.rcParams['mathtext.fontset'] = 'dejavuserif'
plt.rcParams['text.usetex'] = True
plt.rcParams['text.latex.unicode'] = True

input_file = Table.read('../fitting_plotting_outputs.csv')
grid_dusty = Table.read('../models/'+str(input_file['grid_name'][0])+'_models.fits')
grid_outputs = Table.read('../models/'+str(input_file['grid_name'][0])+'_outputs.csv')


def get_data(filename):
    table = Table.read(filename)
    x = np.array(table.columns[0])
    y = np.array(table.columns[1])
    y = y * u.Jy
    y = y.to(u.W/(u.m * u.m), equivalencies=u.spectral_density(x * u.um))
    return x, np.array(y)

# plotting stuff
if len(input_file) == 1:
    fig, ax1 = plt.subplots(1, 1, sharex=True, sharey=True, figsize=(8, 10))
elif len(input_file) == 2:
    fig, axs = plt.subplots(2, 1, sharex=True, sharey=True, figsize=(8, 10))
elif len(input_file) == 3:
    fig, axs = plt.subplots(3, 1, sharex=True, sharey=True, figsize=(8, 10))
else:
    fig, axs = plt.subplots(math.ceil(len(input_file)/3), 3, sharex=True, sharey=True, figsize=(8, 10))
    axs = axs.ravel()


for counter, target in enumerate(input_file):
    # gets data for plotting
    target_name = (target['target_name']).replace('.csv', '')
    x_data, y_data = get_data(target['data_file'])
    x_model, y_model = grid_dusty[target['index']]
    y_model = y_model * input_file[counter]['norm']

    # logscale
    x_model = np.log10(x_model)
    y_model = np.log10(y_model)
    x_data = np.log10(x_data)
    y_data = np.log10(y_data)

    # plotting
    if len(input_file) == 1:
        ax1.set_xlim(0.21, 1.79)
        ax1.set_ylim(-14.2, -10.51)
        ax1.plot(x_model, y_model, c='k', linewidth=0.7, linestyle='--', zorder=2)
        ax1.plot(x_data, y_data, c='blue')
        ax1.annotate(target_name.replace('-', r'\textendash'), (0.8, 0.8), xycoords='axes fraction', fontsize=14)
        ax1.get_xaxis().set_tick_params(which='both', direction='in', labelsize=15)
        ax1.get_yaxis().set_tick_params(which='both', direction='in', labelsize=15)
    else:
        axs[counter].set_xlim(0.21, 1.79)
        axs[counter].set_ylim(-14.2, -10.51)
        axs[counter].plot(x_model, y_model, c='k', linewidth=0.7, linestyle='--', zorder=2)
        axs[counter].plot(x_data, y_data, c='blue')
        axs[counter].annotate(target_name.replace('-', r'\textendash'), (0.8, 0.8), xycoords='axes fraction', fontsize=14)
        axs[counter].get_xaxis().set_tick_params(which='both', direction='in', labelsize=15)
        axs[counter].get_yaxis().set_tick_params(which='both', direction='in', labelsize=15)
        axs[counter].set_xlabel('log $\lambda$ ($\mu m$)', labelpad=10)
        axs[counter].set_ylabel("log $\lambda$ F$_{\lambda}$ "+"(W m$^{-2}$)", labelpad=10)

plt.subplots_adjust(wspace=0, hspace=0)
# fig.text(0.5, 0.1, 'log $\lambda$ ($\mu m$)', ha='center', fontsize=16)
# fig.text(0.1, 0.5, "log $\lambda$ F$_{\lambda}$ "+"(W m$^{-2}$)", va='center', rotation='vertical', fontsize=16)
fig.savefig('../output_seds.png', dpi=500, bbox_inches='tight')


a = Table.read('../fitting_results.csv')

