import os
import math
import subprocess
import pdb
import shutil
import numpy as np
import astropy.units as u
import matplotlib.pyplot as plt
from glob import glob
from astropy.io import ascii
from fnmatch import fnmatch
from multiprocessing import cpu_count, Pool
from functools import partial
from astropy.table import Table, Column
from desk import config
from matplotlib import rc
from scipy import interpolate

'''
Steve Goldman
Space Telescope Science Institute
May 17, 2018
sgoldman@stsci.edu

This script is for plotting the outputs of the sed_fitting script.
'''


def create_fig():
    """
    :return: Runs plotting script
    """
    rc('text', usetex=True)
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['mathtext.fontset'] = 'dejavuserif'
    plt.rcParams['text.usetex'] = True
    plt.rcParams['text.latex.unicode'] = True

    full_path = str(__file__.replace('plotting_seds.py', ''))
    # pdb.set_trace()
    input_file = Table.read('fitting_plotting_outputs.csv')
    grid_dusty = Table.read(full_path + 'models/' + str(input_file['grid_name'][0]) + '_models.fits')

    def get_data(filename):
        """
        :param filename: filename of input data. Should be csv with Column 0: wavelength in um and Col 1: flux in Jy
        :return: two arrays of wavelength (x) and flux (y) in unit specified in config.py
        """
        table = ascii.read(filename, delimiter=',')
        table.sort(table.colnames[0])
        x = np.array(table.columns[0])
        y = np.array(table.columns[1])
        if config.output['output_unit'] == 'Wm^-2':
            y = y * u.Jy
            y = y.to(u.W / (u.m * u.m), equivalencies=u.spectral_density(x * u.um))
        elif config.output['output_unit'] == 'Jy':
            pass
        else:
            raise ValueError("Unit in config.py not 'Wm^-2' or 'Jy'")
        return x, np.array(y)

    # setting axes
    if len(input_file) == 1:
        fig, ax1 = plt.subplots(1, 1, sharex=True, sharey=True, figsize=(8, 5))
    elif len(input_file) == 2:
        fig, axs = plt.subplots(2, 1, sharex=True, sharey=True, figsize=(8, 10))
    elif len(input_file) == 3:
        fig, axs = plt.subplots(3, 1, sharex=True, sharey=True, figsize=(8, 10))
    else:
        fig, axs = plt.subplots(math.ceil(len(input_file) / 3), 3, sharex=True, sharey=True, figsize=(8, 10))
        axs = axs.ravel()

    for counter, target in enumerate(input_file):
        # gets data for plotting
        target_name = (target['target_name']).replace('.csv', '').replace('_', ' ')
        x_data, y_data = get_data(target['data_file'])
        x_model, y_model = grid_dusty[target['index']]
        x_model = x_model[np.where(y_model != 0)]
        y_model = y_model[np.where(y_model != 0)] * input_file[counter]['norm']
        if config.output['output_unit'] == 'Wm^-2':
            axislabel = "log $\lambda$ F$_{\lambda}$ (W m$^{-2}$)"
        elif config.output['output_unit'] == 'Jy':
            y_model = y_model * u.W / (u.m * u.m)
            y_model = y_model / ((x_model * u.um).to(u.Hz, equivalencies=u.spectral()))
            y_model = y_model.to(u.Jy).value
            axislabel = "log F$_{\lambda}$ (Jy)"
        else:
            raise ValueError("Unit in config.py not 'Wm^-2' or 'Jy'")

        # logscale
        x_model = np.log10(x_model)
        y_model = np.log10(y_model)
        x_data = np.log10(x_data)
        y_data = np.log10(y_data)

        # out = Table((x_model,y_model), names=('wave', 'lamflam'))
        # out.write('crystalline_fit.csv', format='csv')
        # pdb.set_trace()
        # plotting
        if len(input_file) == 1:
            ax1.set_xlim(-0.99, 2.49)
            ax1.set_ylim(np.median(y_model) - 2, np.median(y_model) + 2)
            ax1.scatter(x_data, y_data, c='blue', label='data')
            ax1.plot(x_model, y_model, c='k', linewidth=0.5, linestyle='--', zorder=2, label='model')
            ax1.annotate(target_name.replace('-', r'\textendash'), (0.07, 0.85), xycoords='axes fraction', fontsize=14)
            ax1.get_xaxis().set_tick_params(which='both', direction='in', labelsize=15)
            ax1.get_yaxis().set_tick_params(which='both', direction='in', labelsize=15)
            ax1.set_xlabel('log $\lambda$ ($\mu m$)', labelpad=10)
            ax1.set_ylabel("log $\lambda$ F$_{\lambda}$ " + "(W m$^{-2}$)", labelpad=10)
        else:
            axs[counter].set_xlim(-0.99, 2.49)
            axs[counter].set_ylim(np.median(y_model) - 2, np.median(y_model) + 2)
            axs[counter].plot(x_model, y_model, c='k', linewidth=0.4, linestyle='--', zorder=2)
            axs[counter].scatter(x_data, y_data, c='blue')
            axs[counter].annotate(target_name.replace('-', r'\textendash'), (0.7, 0.8), xycoords='axes fraction',
                                  fontsize=14)
            axs[counter].get_xaxis().set_tick_params(which='both', direction='in', labelsize=15)
            axs[counter].get_yaxis().set_tick_params(which='both', direction='in', labelsize=15)
            axs[counter].set_xlabel('log $\lambda$ ($\mu m$)', labelpad=10)
            axs[counter].set_ylabel(axislabel, labelpad=10)

        # pdb.set_trace()
    plt.subplots_adjust(wspace=0, hspace=0)
    fig.savefig('output_sed.png', dpi=200, bbox_inches='tight')
