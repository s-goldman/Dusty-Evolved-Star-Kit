import ipdb
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from astropy.table import Table, Column, vstack, hstack

__all__ = ["create_pdfs"]

# most_likely = {
# "mass_loss_rate":
# }


def create_pdfs(full_outputs, probabilities, n_bins):
    def create_1D_pdf(param, most_likely, stds):
        def get_prob_bins():
            param_array = full_outputs[param]
            min_bin_range = np.min(param_array)
            max_vin_range = np.max(param_array)
            bins = np.linspace(min_bin_range, max_vin_range, n_bins)

            # Return the indices of the bins to which each value in input array belongs.
            digitized = np.digitize(param_array, bins)

            bin_sums = [param_array[digitized == i].sum() for i in range(1, len(bins))]
            bin_sums /= np.sum(bin_sums)
            return bins, bin_sums

        def most_likely_and_std(bins, bin_sums):
            most_likely_value = bins[np.argmax(bin_sums)]
            std_value = np.std(bin_sums)
            return most_likely_value, std_value

        def assign_most_likely(param, value, most_likely):
            most_likely[param] = value

        _bins, _bin_sums = get_prob_bins()
        likely_val, std_val = most_likely_and_std(_bins, _bin_sums)
        most_likely[str(param)] = likely_val
        stds[str(param)] = std_val
        return most_likely

    most_likely = {}
    stds = {}
    create_1D_pdf("teff", most_likely, stds)
    create_1D_pdf("tinner", most_likely, stds)
    create_1D_pdf("odep", most_likely, stds)
    create_1D_pdf("lum", most_likely, stds)
    create_1D_pdf("scaled_vexp", most_likely, stds)
    create_1D_pdf("scaled_mdot", most_likely, stds)

    return most_likely, stds
