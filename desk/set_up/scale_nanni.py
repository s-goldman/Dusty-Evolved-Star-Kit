import numpy as np
from astropy.table import Column, vstack


def scale(_outputs, _models, scaling_factor):
    # scale fluxes and normalization value
    scaled_models = vstack(_models["flux_wm2"] / scaling_factor)
    _outputs["norm"] = np.log10(_outputs["norm"] / scaling_factor)
    _outputs.add_column(
        Column(np.arange(1, len(_outputs) + 1), name="model_id"), index=0
    )
    _outputs.rename_columns(
        ["L", "vexp", "mdot"], ["lum", "scaled_vexp", "scaled_mdot"]
    )
    return _outputs, scaled_models
