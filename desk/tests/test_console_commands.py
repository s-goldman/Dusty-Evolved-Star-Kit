import pytest
import numpy as np
from astropy.table import Table
from desk import console_commands
from desk.set_up import config


def test_grids(capfd):
    console_commands.grids()
    out, _ = capfd.readouterr()
    np.testing.assert_allclose(len(out), 223, err_msg=("Print grids error"))


def create_sample_data(directory, dataset):
    """Creates sample datasets for testing and saves it to a two column csv.

    Parameters
    ----------
    directory : str
        Directory to write csv file to.
    dataset : int
        The integer associated with each sample testing dataset.

    Returns
    -------
    type : csv file
        two column csv file with wavelength (um) and flux (Jy).

    """
    target_filename = "sample_target_" + str(dataset) + ".csv"
    target_file_path = str(directory.join(target_filename))
    file = open(target_file_path, "w")
    # simple dataset
    if dataset == 1:
        file.write("3.55,0.389\n4.49,0.357\n5.73,0.344\n7.87,0.506\n23.7,0.676")
    # longer dataset
    if dataset == 2:
        file.write("1.2,0.4\n1.5,0.1\n1.6,0.1\n1.7,0.2\n2,0.7\n5,1.0\n40,0.676")
    # out of order and bad fluxes
    if dataset == 3:
        file.write("1,0.389\n4,0.357\n3,0.344\n10,0\n40,-90")
    # # not enough sources (failure)
    # if dataset == 4:
    #     file.write("1,0.389\n4,0.357")
    file.close()
    return target_file_path


@pytest.mark.parametrize("dataset", [1, 2, 3])
@pytest.mark.parametrize("testing_grid", config.grids)
def test_single_fit(tmpdir, testing_grid, dataset):
    # tests single fit for each sample dataset and each grid
    example_filename = create_sample_data(tmpdir, dataset)
    console_commands.fit(
        source=str(example_filename),
        grid=testing_grid,
        n=2,
        multiprocessing=False,
        testing=True,
    )


def test_single_fit_options(tmpdir):
    # testing single fit user options
    example_filename = create_sample_data(tmpdir, 2)
    console_commands.fit(
        source=str(example_filename),
        distance=0.1,
        grid="oxygen",
        n=2,
        min_wavelength=1,
        max_wavelength=100,
        testing=True,
    )


def test_single_sed(tmpdir):
    # test for single SED figure
    console_commands.sed()


def test_multiple_fit(tmpdir):
    # test for multiple SED fit with SED figure
    create_sample_data(tmpdir, 1)
    create_sample_data(tmpdir, 2)
    create_sample_data(tmpdir, 3)
    console_commands.fit(source=str(tmpdir))
    console_commands.sed()
