from astropy.table import Table

# from PIL import Image, ImageChops
import desk
from desk import console_commands
from desk.set_up import config
import numpy as np
import pytest


def test_grids(capfd):
    console_commands.grids()
    out, _ = capfd.readouterr()
    np.testing.assert_allclose(len(out), 183, err_msg=("Print grids error"))


# @pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)])
# def test_get_model(test_input, expected):
# 	assert
def create_sample_data(directory, set):
    target_filename = "sample_target_" + str(set) + ".csv"
    target_file_path = directory.join(target_filename)
    file = open(target_file_path, "w")
    # simple set
    if set == 1:
        file.write("3.55,0.389\n4.49,0.357\n5.73,0.344\n7.87,0.506\n23.7,0.676")
    # longer set
    if set == 2:
        file.write("1.2,0.4\n1.5,0.1\n1.6,0.1\n1.7,0.2\n2,0.7\n5,1.0\n40,0.676")
    # out of order and bad fluxes
    if set == 3:
        file.write("1,0.389\n4,0.357\n3,0.344\n10,0\n40,-90")
    # # not enough sources (failure)
    # if set == 4:
    #     file.write("1,0.389\n4,0.357")
    file.close()
    return target_file_path


# tests single fit for each sample set and each grid
@pytest.mark.parametrize("set", [1, 2, 3])
@pytest.mark.parametrize("testing_grid", config.grids)
def test_single_fit(tmpdir, testing_grid, set):
    example_filename = create_sample_data(tmpdir, set)
    console_commands.fit(
        source=str(example_filename), grid=testing_grid, n=2, testing=True
    )
    # results = Table.read("fitting_results.csv")
    # assert len(results) == 1


# def test_single_sed(tmpdir):
#     console_commands.sed()
#     sed = Image.open("output_sed.png")
#     expected_sed = Image.open("desk/tests/expected_sed_1.png")
#     assert ImageChops.difference(sed, expected_sed).getbbox() is None
#
#
# def test_multiple_fit(tmpdir):
#     create_sample_data(tmpdir, 1)
#     create_sample_data(tmpdir, 2)
#     console_commands.fit(source=str(tmpdir))
#     results = Table.read("fitting_results.csv")
#     expected_results = Table.read("desk/tests/expected_fitting_results_2.csv")
#     cols = results.colnames
#     np.testing.assert_allclose(
#         np.array(results[cols[2:-1]]).tolist(),
#         np.array(expected_results[cols[2:-1]]).tolist(),
#         err_msg=("Fitting results error"),
#     )
#
#
# def test_multiple_sed(tmpdir):
#     console_commands.sed()
#     sed = Image.open("output_sed.png")
#     expected_sed = Image.open("desk/tests/expected_sed_2.png")
#     np.testing.assert_string_equal(
#         str(ImageChops.difference(sed, expected_sed).getbbox()), "None"
#     )
