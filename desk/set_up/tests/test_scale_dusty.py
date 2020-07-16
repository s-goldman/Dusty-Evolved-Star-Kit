import numpy as np
from desk.set_up import scale_dusty


def test_scale_vexp():
    vexps = [5, 5, 5]
    lums = [1000, 5000, 10000]
    scaled_vexps = scale_dusty.scale_vexp(vexps, lums)
    expected = np.array([2.8117066259517456, 4.204482076268572, 5.0])
    np.testing.assert_allclose(
        scaled_vexps, expected, err_msg=("Expansion velocity scaling error")
    )


def test_scale_mdot():
    mdots = [1e-4, 5e-6, 7e-7]
    lums = [1000, 5000, 10000]
    scaled_mdots = scale_dusty.scale_mdot(mdots, lums)
    expected = np.array([1.77827941e-05, 2.97301779e-06, 7.00000000e-07])
    np.testing.assert_allclose(
        scaled_mdots, expected, err_msg=("Mass-loss rate scaling error")
    )


# # def test_scale_dusty():
#     luminosities = [1e4, 5e4]
#     grid_outputs = Table(
#         [[4, 4, 4], [1e-5, 1e-6, 7e-7], [1, 1, 1]], names=("vexp", "mdot", "norm")
#     )
#     models = Table(
#         [
#             [[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6]],
#             [
#                 [0.1, 0.1, 0.2, 0.2, 0.2, 0.6],
#                 [0.001, 0.005, 0.1, 0.0, 1, 9],
#                 [1, 0.0003, 0.1, 0.0, 1, 9],
#             ],
#         ],
#         names=("wavelength_um", "flux_wm2"),
#     )
#     scaling_factor = 7.7e16
#     scaled_outputs, scaled_models = scale_dusty.scale(
#         grid_outputs, models, luminosities, scaling_factor
#     )
#     expected_outputs = Table(
#         [
#             [1.2987012987012988e-17] * 6,  # norm
#             [10000, 10000, 10000, 50000, 50000, 50000],  # lum
#             [  # scaled_vexp
#                 4,
#                 4,
#                 4,
#                 5.981395124884882,
#                 5.981395124884882,
#                 5.981395124884882,
#             ],
#             [  # scaled mdot
#                 1e-5,
#                 1e-6,
#                 7e-7,
#                 3.3437015248821105e-05,
#                 3.3437015248821097e-06,
#                 2.340591067417477e-06,
#             ],
#         ],
#         names=("norm", "lum", "scaled_vexp", "scaled_mdot"),
#     )
#     assert np.array_equal(scaled_outputs, expected_outputs)
