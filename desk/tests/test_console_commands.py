from astropy.table import Table
from PIL import Image, ImageChops
from desk import console_commands
import numpy as np


def test_grids(capfd):
    console_commands.grids()
    out, _ = capfd.readouterr()
    np.testing.assert_allclose(len(out), 250, err_msg=("Print grids error"))


# @pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)])
# def test_get_model(test_input, expected):
# 	assert
def create_sample_data(directory, sample_id):
    target_filename = "sample_target_" + str(sample_id) + ".csv"
    target_file_path = directory.join(target_filename)
    file = open(target_file_path, "w")
    file.write("3.55,0.389\n4.49,0.357\n5.73,0.344\n7.87,0.506\n23.7,0.676")
    file.close()
    return target_file_path


def test_single_fit(tmpdir):
    example_filename = create_sample_data(tmpdir, 1)
    console_commands.fit(source=str(example_filename))
    results = Table.read("fitting_results.csv")
    expected_results = Table.read("desk/tests/expected_fitting_results_1.csv")
    cols = results.colnames
    np.testing.assert_allclose(
        np.array(results[cols[2:-1]]).tolist(),
        np.array(expected_results[cols[2:-1]]).tolist(),
        err_msg=("Fitting results error"),
    )


def test_single_sed(tmpdir):
    console_commands.sed()
    sed = Image.open("output_sed.png")
    expected_sed = Image.open("desk/tests/expected_sed_1.png")
    assert ImageChops.difference(sed, expected_sed).getbbox() is None


def test_multiple_fit(tmpdir):
    create_sample_data(tmpdir, 1)
    create_sample_data(tmpdir, 2)
    console_commands.fit(source=str(tmpdir))
    results = Table.read("fitting_results.csv")
    expected_results = Table.read("desk/tests/expected_fitting_results_2.csv")
    cols = results.colnames
    np.testing.assert_allclose(
        np.array(results[cols[2:-1]]).tolist(),
        np.array(expected_results[cols[2:-1]]).tolist(),
        err_msg=("Fitting results error"),
    )


def test_multiple_sed(tmpdir):
    console_commands.sed()
    sed = Image.open("output_sed.png")
    expected_sed = Image.open("desk/tests/expected_sed_2.png")
    np.testing.assert_string_equal(
        str(ImageChops.difference(sed, expected_sed).getbbox()), "None"
    )
