# Steve Goldman, Space Telescope Science Institute, sgoldman@stsci.edu
# Script adapted from the BEAST (https://github.com/BEAST-Fitting)
import ipdb
import numpy as np
import math

from desk.outputs import plot_pdf


class pdf1d:
    def __init__(self, gridvals, nbins, logspacing=False, minval=None, maxval=None):
        """
        Create an object which can be used to efficiently generate a 1D pdf for an observed object.

        Parameters
        ----------

        gridvals: array-like
            values of the quantity for all the grid points

        nbins: int
            number of bins to use for the 1D pdf

        logspacing: bool
            whether to use logarithmic spacing for the bins

        minval, maxval: float (optional)
            override the range for the bins. this can be useful to make
            sure that the pdfs for different runs have the same bins
        """
        self.nbins = nbins
        self.n_gridvals = len(gridvals)
        self.logspacing = logspacing

        # grab copy of gridvals that can be edited without messing with original
        tgridvals = np.array(gridvals)
        self.n_indxs = len(gridvals)

        if len(tgridvals) <= 0:
            # this is a hack to just get the code to work when
            # all the possible values are negative and the requested
            # pdf is for log x values
            self.bad = True
            self.bin_vals = np.linspace(0.0, 1.0, num=self.nbins)
        else:
            self.bad = False
            # set bin ranges
            self.min_val = tgridvals.min() if minval is None else minval
            self.max_val = tgridvals.max() if maxval is None else maxval

            # if log spacing requested, make the transformation
            if logspacing:
                self.min_val = math.log10(self.min_val)
                self.max_val = math.log10(self.max_val)
                tgridvals = np.log10(tgridvals)

            # set bin widths
            if self.nbins > 1:
                self.bin_delta = (self.max_val - self.min_val) / (self.nbins - 1)
            else:
                self.bin_delta = 1

            # set values for the bin middles/edges
            self.bin_vals = self.min_val + np.arange(self.nbins) * self.bin_delta
            self.bin_edges = (
                self.min_val + (np.arange(self.nbins + 1) - 0.5) * self.bin_delta
            )

            # get PDF bin associated with each grid val
            pdf_bin_num = np.digitize(tgridvals, self.bin_edges)

            # array to hold indices for each bin
            # (like the IDL version returned by the histogram function)
            pdf_bin_indxs = []

            for i in range(nbins):
                # find the indicies for the current bin
                cur_bin_indxs, = np.where(pdf_bin_num == (i + 1))

                # save them
                pdf_bin_indxs.append(cur_bin_indxs)

            # transform the bin edges back to linear spacing if log spacing
            #  was asked for
            if logspacing:
                self.bin_vals = np.power(10.0, self.bin_vals)
                self.bin_edges = np.power(10.0, self.bin_edges)

            self.pdf_bin_indxs = pdf_bin_indxs

    def gen1d(self, gindxs, weights):
        """
        Determines the probabilities for each bin in weights.

        Parameters
        ----------
        gindxs : array
            Array of indices excluding those with weights below threshold.
        weights : array
            grid_weights * priors * log_liklihoods

        Returns
        -------
        self.bin_vals: array
            parameter bins
        _vals_1d: array
            sums of probabilities for each bin
        """

        if self.bad:
            return (self.bin_vals, np.zeros((self.nbins)))
        else:
            _tgrid = np.zeros(self.n_gridvals)
            _tgrid[gindxs] = weights
            _vals_1d = np.zeros(self.nbins)
            for i in range(self.nbins):
                if len(self.pdf_bin_indxs[i]) > 0:
                    _vals_1d[i] = np.sum(_tgrid[self.pdf_bin_indxs[i]])

            return (self.bin_vals, _vals_1d)


def par_pdf(par, full_outputs, probs):
    # create 1d-pdfs
    pdf = pdf1d(full_outputs[par], 50, logspacing=True)

    # calculates probabilities for each bin (bin width set by dif in bins)
    bins, bin_total_prob = pdf1d.gen1d(pdf, np.arange(0, len(full_outputs)), probs)

    # most likely value
    best = bins[np.argmax(bin_total_prob)]

    # plot probability function
    plot_pdf.plot(par, pdf, bin_total_prob, best)
    return best
