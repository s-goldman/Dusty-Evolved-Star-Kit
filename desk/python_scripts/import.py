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
from matplotlib import rc
from scipy import interpolate
'''
Steve Goldman
Space Telescope Science Institute
May 17, 2018
sgoldman@stsci.edu

This script is for plotting the outputs of the sed_fitting script.
'''

def csv(input_csv):
	if input_csv.split(.)[-1] == 'csv':
		a = Table.read(input_csv)
	else:
		raise ValueError('Not a csv file!')
	return a


def csv(directory_name):
	for file in 
	a = Table.read(input_csv)
	return a