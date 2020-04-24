import ipdb
import numpy as np
import matplotlib.pyplot as plt
from desk.set_up import config
from astropy.table import Table
from sklearn.neighbors import KernelDensity


def prior(data, par, bandwidth, sampling=500):
    """
    Script to create prior distribution given dataset.

    Parameters
    ----------
    data : astropy Table
        Data used to create prior distribution
    par : str
        column name of parameter to determine distribution.
    bandwidth : float
        bin width of kde/histogram.
    sampling : int
        spacing of parameter to determine distribution.

    Returns
    -------
    png figure
    csv table of distribution

    """
    # instantiate and fit the KDE model
    kde = KernelDensity(bandwidth=bandwidth, kernel="gaussian")
    kde.fit(data[par][:, None])

    # x range
    x_d = np.linspace(np.min(data[par]), np.max(data[par]), sampling)

    # score_samples returns the log of the distribution
    logprob = kde.score_samples(x_d[:, None])

    y_vals = np.exp(logprob)

    # normalized
    y_vals /= np.sum(y_vals)

    out = Table((x_d, y_vals), names=("x", "y"))
    out.write(
        config.path + "probabilities/priors/prior_" + par + ".csv",
        format="csv",
        overwrite=True,
    )

    # create figure
    fig = plt.figure(figsize=(4, 4))
    ax1 = fig.add_subplot(1, 1, 1)

    # labels
    ax1.set_ylabel(r"$N$ (normalized)")
    ax1.set_xlabel(par)

    # plot kdefunction
    ax1.fill_between(x_d, y_vals, alpha=0.5)

    # save and close figure
    plt.subplots_adjust(wspace=0, hspace=0)
    fig.savefig(
        config.path + "probabilities/priors/prior_" + par + ".png",
        dpi=200,
        bbox_inches="tight",
        overwrite=True,
    )
    plt.close()


#
# data = Table.read("priors/LMC_tables_H11_all.dat", format="ascii")
#
# prior(data, "dmdt", 2e-6)
# prior(data, "tau10", 0.75)
