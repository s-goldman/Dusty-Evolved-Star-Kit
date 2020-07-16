import numpy as np
from desk.set_up import full_grid


def test_generate_model_luminosities():
    lums = full_grid.generate_model_luminosities(3)
    expected = [1000.0, 12247.44871392, 150000.0]
    np.testing.assert_allclose(lums, expected, err_msg=("Luminosity generation error"))
