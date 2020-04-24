import ipdb
import numpy as np
from desk.set_up import config
from astropy.table import Table
from scipy.interpolate import interp1d


def resamp(model, model_par, prior_par):
    """
    Resamples input prior probabilities to interpolated values of model grid.

    Parameters
    ----------
    model : astropy table
        model outputs
    model_par : str
        name of column in model outputs.
    prior : array
        prior probabilities.
    prior_par : str
        prior parameter name.

    Returns
    -------
    type
        Description of returned object.

    """
    prior = Table.read(config.path + "probabilities/priors/prior_" + prior_par + ".csv")

    # get index of data in range
    idx_model_in_prior = np.where(
        (model[model_par] > np.min(prior["x"]))
        & (model[model_par] < np.max(prior["x"]))
    )[0]

    # and out of range
    idx_model_out_prior = np.where(
        (model[model_par] < np.min(prior["x"]))
        | (model[model_par] > np.max(prior["x"]))
    )[0]

    model_in = model[model_par][idx_model_in_prior]
    model_out = model[model_par][idx_model_out_prior]

    # set up interpolation function
    f = interp1d(prior["x"], prior["y"], kind="cubic")

    # return warning of % of model values outside of prior range
    if len(model_out) > 0:
        missed_percentage = int((len(model_out) / len(model)) * 100)
        print(
            "Warning: "
            + "Model outside of "
            + model_par
            + " prior range. Model grid limited by "
            + str(missed_percentage)
            + "%."
        )

    # interpolate new values
    x_new = np.sort(np.unique(list(model_in)))
    y_new = f(x_new)

    # re-normalize
    y_new /= np.sum(y_new)

    # resampled priors
    resamp_priors = Table((x_new, y_new), names=("par_val", "prob"))

    prior = np.zeros(len(model))
    for i, item in enumerate(resamp_priors):
        idx = np.where(model[model_par] == item["par_val"])
        prior[idx] = resamp_priors["prob"][i]
    return prior


# # import data
# model = Table.read("../../models/Oss-Orich-bb_outputs.csv")
# model_par = "mdot"
# prior = Table.read("priors/prior_dmdt.csv")
# prior_par = "dmdt"
#
# p = resamp(model, model_par, prior, prior_par)
#
# # import data
# model = Table.read("../../models/Oss-Orich-bb_outputs.csv")
# model_par = "odep"
# prior = Table.read("priors/prior_tau10.csv")
# prior_par = "tau10"
#
# t = resamp(model, model_par, prior, prior_par)
