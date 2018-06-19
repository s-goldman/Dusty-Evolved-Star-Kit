import os
import shutil
import pylab
import math
import subprocess
import numpy as np
import astropy.units as u
import matplotlib.pyplot as plt
from fnmatch import fnmatch
from multiprocessing import cpu_count, Pool
from functools import partial
from astropy.units import astrophys
from astropy.table import Table, Column, vstack
from matplotlib import rc
from scipy import interpolate
import glob

"""
This script converts a directory of DUSTY grids from Elitzur & Ivezic (2001) to a single table fits file

https://github.com/ivezic/dusty

"""
teff_sampling = 20
tinner_sampling = 20
tau_sampling = 150


mc_index = 0
print()
for item in os.listdir('../models/'):
    if not fnmatch(item, '*.*'):
        print(item)
print()

directory_name = input('directory name: ')

spectra_files = []

for root, dirs, files in os.walk("./"+directory_name):
    for name in files:
        if fnmatch(str(name), '*.s*'):
            spectra_files.append(os.path.join(root, name))


output_files = []

for root, dirs, files in os.walk("./"+directory_name):
    for name in files:
        if fnmatch(str(name), '*.out'):
            output_files.append(os.path.join(root, name))


dusty_spectra = []

for item in spectra_files:
    a = np.loadtxt(item, usecols=[0, 1], unpack=True)
    dusty_spectra.append(a)

grid_dusty = Table(np.array(dusty_spectra))
grid_dusty.write(directory_name+'_models.fits', format='fits', overwrite=True)
waves = grid_dusty[0][0]

output_array = Table()
for item in output_files:
    output_table = Table(np.genfromtxt(item, dtype=[('number', np.int16), (
        'odep', np.float64), ('c', np.float64), ('d', np.float64), ('e', np.float64), ('f', np.float64), (
        'g', np.float64), ('h', np.float64), ('mdot', np.float64), ('vexp', np.float64), (
        'i', np.float64)], comments="*", delimiter='', skip_header=46, skip_footer=15))
    array_info = item.split('/')[-1].split("_")
    grid_name = Column([str(array_info[0])]*len(output_table), name='grid_name')
    teff = Column([int(array_info[1])]*len(output_table), name='teff')
    tinner = Column([int(array_info[2].split('.')[0])]*len(output_table), name='tinner')
    output_table.add_columns((grid_name, teff, tinner), indexes=[0, 0, 0])
    print(output_table)
    output_array = vstack([output_array, output_table])

# create interpolator
tau = np.unique(output_array['odep'])
teff = np.unique(output_array['teff'])
tinner = np.unique(output_array['tinner'])

array = np.zeros((len(teff), len(tinner), len(tau), len(waves)))
mass_loss_array = np.zeros((len(teff), len(tinner), len(tau)))
expansion_velocity_array = np.zeros((len(teff), len(tinner), len(tau)))


for i in range(0, len(teff)):
    for j in range(0, len(tinner)):
        for k in range(0, len(tau)):
            mc_index = np.where((teff[i] == output_array['teff']) & (tinner[j] == output_array['tinner'])
                                & (tau[k] == output_array['odep']))
            if np.any(mc_index):
                array[i][j][k] = grid_dusty[mc_index[0][0]][1]
                mass_loss_array[i][j][k] = output_array['mdot'][mc_index]
                expansion_velocity_array[i][j][k] = output_array['vexp'][mc_index]
# data_array = Table(array)
interpolator = interpolate.RegularGridInterpolator((teff, tinner, tau, waves), array)
mdot_interpolator = interpolate.RegularGridInterpolator((teff, tinner, tau), mass_loss_array)
vexp_interpolator = interpolate.RegularGridInterpolator((teff, tinner, tau), expansion_velocity_array)

interp_array = []
interp_dusty = []
new_teff = np.linspace(teff.min(), teff.max(), teff_sampling)
new_tinner = np.linspace(tinner.min(), tinner.max(), tinner_sampling)
new_tau = np.linspace(tau.min(), tau.max(), tau_sampling)

counter = 1
for i in new_teff:
    for j in new_tinner:
        for k in new_tau:
            y_new = []
            for wavelength in waves:
                y_new.append(interpolator([i, j, k, wavelength])[0])
            interp_dusty.append([waves, y_new])
            mass_loss_rate = mdot_interpolator([i, j, k])[0]
            expansion_velocity = vexp_interpolator([i, j, k])[0]
            interp_array.append([directory_name, i, j, counter, k, mass_loss_rate, expansion_velocity])
            counter = counter + 1

print()
print('previous sampling')
print((len(teff), len(tinner), len(tau)))
print()
print('interpolated sampling')
print((len(new_teff), len(new_tinner), len(new_tau)))
print()

file_a = Table(np.array(interp_dusty), names=('wavelength', 'flux'))
file_a.write('../'+directory_name+'_models.fits', format='fits', overwrite=True)

file_b = Table(np.array(interp_array), names=('grid_name', 'teff', 'tinner', 'number', 'odep', 'mdot', 'vexp'),
               dtype=('U25', 'f8', 'f8', 'i4', 'f8', 'f8', 'f8'))
file_b.write('../'+directory_name+'_outputs.fits', format='fits', overwrite=True)
