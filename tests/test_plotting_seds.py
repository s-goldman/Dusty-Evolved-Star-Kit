#!/usr/bin/env python
# -*- coding: utf-8 -*-

import desk, time, os, glob
import pytest
import numpy as np
from desk import plotting_seds
from astropy.table import Table


def test_create_fig():
    # checks to see if png was created or modified within time_check_threshold
    time_check_threshold = 10  # seconds
    plotting_seds.create_fig()
    time_created = os.path.getmtime("output_sed.png")
    current_time = time.time()
    assert time_created - current_time < time_check_threshold


def test_single_figures():
    created_times = []
    time_check_threshold = 10  # seconds
    plotting_seds.single_figures()
    input_file = Table.read("fitting_plotting_outputs.csv")
    n_files = len(input_file)
    target_files = glob.glob("*output_sed_*")
    current_time = time.time()
    for file in target_files:
        time_created = os.path.getmtime(file)
        created_times.append(time_created)
    assert n_files == len(target_files)
    assert all(x > time_check_threshold for x in created_times)
