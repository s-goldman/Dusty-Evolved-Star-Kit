# import time, os, glob
# import pytest
# import numpy as np
# from desk import console_commands, plotting_seds
# from astropy.table import Table


# def test_create_fig():
#     # checks to see if png was created or modified within time_check_threshold
#     time_check_threshold = 10  # seconds
#     console_commands.fit()
#     time_created = os.path.getmtime("output_sed.png")
#     current_time = time.time()
#     assert time_created - current_time < time_check_threshold
#
#
# def test_single_figures():
#     # checks if the number of files created matches the number of files fit.
#     # Also checks to see if all pngs created within time_check_threshold.
#     input_file = "fitting_plotting_outputs.csv"
#     if os.path.isfile(input_file):
#         created_times = []
#         time_check_threshold = 10  # seconds
#         console_commands.fit()
#         plotting_seds.single_figures()
#         input_file = Table.read(input_file)
#         n_files = len(input_file)
#         target_files = glob.glob("*output_sed_*")
#         current_time = time.time()
#         for file in target_files:
#             time_created = os.path.getmtime(file)
#             created_times.append(time_created)
#         assert n_files == len(target_files)
#         assert all(x > time_check_threshold for x in created_times)
#     else:
#         pass
