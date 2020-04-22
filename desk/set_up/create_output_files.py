# Steve Goldman, Space Telescope Science Institute, sgoldman@stsci.edu
import os


def remove_old_output_files():
    if os.path.exists("fitting_results.txt"):
        os.remove("fitting_results.txt")


def make_output_files_dusty():
    remove_old_output_files()
    with open("fitting_results.csv", "w") as f:
        f.write("source,grid,teff,tinner,model_id,odep,norm,L,vexp,mdot,file_name\n")
        f.close()
