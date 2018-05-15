import os,shutil,pylab,math,subprocess
import numpy as np
import astropy.units as u
import matplotlib.pyplot as plt
from fnmatch import fnmatch
from multiprocessing import cpu_count, Pool
from functools import partial
from astropy.units import astrophys
from astropy.table import Table,Column,vstack
from matplotlib import rc
from scipy import interpolate
import glob

spectra_files = []

for root, dirs, files in os.walk("./year4"):
   for name in files:
      if fnmatch(str(name),'*.s*'):
          spectra_files.append(os.path.join(root, name))


output_files = []

for root, dirs, files in os.walk("./year4"):
   for name in files:
      if fnmatch(str(name),'*.out'):
          output_files.append(os.path.join(root, name))


dusty_spectra = []
for item in spectra_files:
    a = np.loadtxt(item, usecols=[0, 1], unpack=True)
    dusty_spectra.append(a)

b = Table(np.array(dusty_spectra))
b.write('dusty_models.fits', format='fits', overwrite=True)

output_array=Table()
for item in output_files:
    output_table = Table(np.genfromtxt(item, dtype=[('number',np.int16),('odep',np.float64),('c',np.float64),('d',np.float64),('e',np.float64),('f',np.float64),('g',np.float64),('h',np.float64),('mdot',np.float64),('vexp',np.float64),('i',np.float64)], comments ="*" , delimiter='', skip_header=46, skip_footer=15))
    array_info = item.split('/')[2].split('_')
    grid_name = Column([str(array_info[0])]*len(output_table), name='grid_name')
    teff = Column([int(array_info[1])]*len(output_table), name='teff')
    tinner = Column([int(array_info[2])]*len(output_table), name='tinner')
    output_table.add_columns((grid_name, teff, tinner), indexes=[0, 0, 0])
    print(output_table)
    output_array = vstack([output_array,output_table])

output_array.write('dusty_outputs.fits', format='fits', overwrite=True)


