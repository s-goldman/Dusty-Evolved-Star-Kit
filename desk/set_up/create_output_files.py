# Steve Goldman, Space Telescope Science Institute, sgoldman@stsci.edu
import os


def remove_old_output_files():
    if os.path.exists("fitting_results.txt"):
        os.remove("fitting_results.txt")
    if os.path.exists("fitting_plotting_outputs.txt"):
        os.remove("fitting_plotting_outputs.txt")


def make_output_files_dusty():
    remove_old_output_files()
    with open("fitting_results.csv", "w") as f:
        f.write("source,L,vexp_predicted,teff,tinner,odep,mdot\n")
        f.close()
    with open("fitting_plotting_outputs.csv", "w") as f:
        f.write("target_name,data_file,norm,index,grid_name,teff,tinner,odep\n")
        f.close()
