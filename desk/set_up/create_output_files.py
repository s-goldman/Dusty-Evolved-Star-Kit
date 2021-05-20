# Steve Goldman, Space Telescope Science Institute, sgoldman@stsci.edu
import os
from desk.set_up import config


def remove_old_output_files():
    """Removes results file from previous run."""
    if os.path.exists("fitting_results.txt"):
        os.remove("fitting_results.txt")


def make_output_files_dusty(fit_params):
    """Creates results csv file.

    Parameters
    ----------
    fit_params : Class
        Single source class with models, data, and specified options.

    Returns
    -------
    csv
        Csv file with the first row (header).

    """
    # Removes and then creates output file for run
    remove_old_output_files()

    with open("fitting_results.csv", "w") as f:
        f.write(
            "source, "
            + (", ".join(fit_params.full_outputs.colnames))
            + ", file_name"
            + ", distance\n"
        )
        f.close()
