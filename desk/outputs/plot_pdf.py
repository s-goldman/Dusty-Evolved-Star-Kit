import ipdb
import numpy as np
import matplotlib.pyplot as plt
from desk.set_up import config


def plot(par, pdf, bin_total_prob, best):
    """
    Creates png with probability distribution of given parameter.

    Parameters
    ----------
    par: str
        paramter name
    pdf : class
        probability distribtion function from create_pdf.
    bin_total_prob : 1D array
        Description of parameter `bin_total_prob`.
    best: float
        best value

    Returns
    -------
    creates png
        probability plot.

    """
    label = par.replace("_", " ")
    trimmed_idx = np.where(bin_total_prob > 0)
    prob_norm = bin_total_prob[trimmed_idx] / np.sum(bin_total_prob[trimmed_idx])

    fig = plt.figure(figsize=(4, 4))
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.fill_between(
        pdf.bin_vals[trimmed_idx], prob_norm, alpha=0.2, color="b", zorder=10
    )
    ax1.axvline(x=best, linestyle="--", c="k", lw=0.5)
    # labels
    ax1.set_ylabel("Probability")
    ax1.set_xlabel(label)

    # save and close figure
    fig.savefig(
        config.path + "outputs/pdf_" + par + ".png",
        dpi=200,
        bbox_inches="tight",
        overwrite=True,
    )
    plt.close()
