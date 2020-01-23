import time, os, glob, ipdb
import pytest
import numpy as np
from desk import parameter_ranges
from astropy.table import Table


def test_create_par():
    # checks to see if png was created or modified within time_check_threshold
    input_file = "fitting_plotting_outputs.csv"
    if os.path.isfile(input_file):
        time_check_threshold = 10  # seconds
        results = Table.read(input_file)
        grid_name = results["grid_name"][-1]
        parameter_ranges.create_par()
        time_created = os.path.getmtime("parameter_ranges_" + grid_name + ".png")
        current_time = time.time()
        assert time_created - current_time < time_check_threshold
    else:
        pass
