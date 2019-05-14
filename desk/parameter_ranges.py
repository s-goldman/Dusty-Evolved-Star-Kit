import pylab, os, fnmatch, shutil, time, math, copy, collections, importlib, pdb
import numpy as np
import astropy.units as u
import matplotlib.pyplot as plt
from fnmatch import fnmatch
from astropy.units import astrophys
from astropy.table import Table, Column, vstack
from numpy import ndarray
from desk import config

plt.rc('text', usetex=True)
plt.rcParams['font.family'] = 'serif'
plt.rcParams['mathtext.fontset'] = 'dejavuserif'


def create_par():
    counter = 0
    model = config.fitting['model_grid']
    full_path = str(__file__.replace('parameter_ranges.py', ''))

    par = Table.read(full_path + '/models/' + model + '_outputs.csv')

    for i in par.colnames:
        if par[i].dtype.str == '<U12':
            par.remove_column(i)

    fig, axs = plt.subplots(math.ceil(len(par.colnames)), 1, figsize=(8, 10))
    axs = axs.ravel()

    axs[0].set_title('Model grid: ' + model, size=20)

    for col in par.colnames:
        par_min = np.min(par[col])
        par_max = np.max(par[col])
        axs[counter].scatter(par[col], [0] * len(par), marker='|', alpha=0.3, c='royalblue')
        axs[counter].set_xlim(par_min - ((par_max - par_min) * 0.1), par_max * 1.1)
        # print(str(par_min) + ' : ' + str(par_max))
        axs[counter].set_ylabel(col)
        axs[counter].set_yticklabels([])
        axs[counter].set_yticks([])
        counter += 1
    plt.subplots_adjust(wspace=0, hspace=0.5)
    fig.savefig('parameter_ranges_' + model + '.png', dpi=200, bbox_inches='tight')
